from flask import Flask, render_template, g, request, session, redirect, url_for, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash

from db import get_db
from views.auth import admin_required, login_required, expert_required

app_bp = Blueprint('app', __name__)

@app_bp.route('/')
def index():
    db = get_db()
    question_query = db.execute(
        '''
        select questions.question_text, questions.id, questions.answer_text, users.name as asked_by, 
        experts.name as expert from questions 
        join users on users.id = questions.asked_by_id 
        join users as experts on experts.id = questions.expert_id 
        where questions.answer_text is not null
        '''
    )
    questions = question_query.fetchall()
    
    return render_template('home.html', questions=questions)

@app_bp.route('/question/<question_id>')
def question(question_id):
    db = get_db()
    query = db.execute(
        '''
        select questions.question_text, questions.answer_text, users.name as asked_by, experts.name as expert 
        from questions 
        join users on users.id = questions.asked_by_id 
        join users as experts on experts.id = questions.expert_id 
        where questions.id = ?
        ''',
        [question_id]
    )
    question = query.fetchone()
    return render_template('question.html', question=question)

@app_bp.route('/answer/<question_id>', methods=['GET', 'POST'])
@expert_required
def answer(question_id):
    db = get_db()

    if request.method == 'POST':
        answer_text = request.form['answer']
        db.execute('update questions set answer_text = ? where id = ?', [answer_text, question_id])
        db.commit()
        return redirect(url_for('.unanswered'))
    
    question_query = db.execute('select question_text, id from questions where id = ?', [question_id])
    question = question_query.fetchone()
    
    return render_template('answer.html', question=question)

@app_bp.route('/ask', methods=['GET', 'POST'])
@login_required
def ask():
    db = get_db()

    if request.method == 'POST':
        question = request.form['question']
        db.execute('insert into questions (question_text, asked_by_id, expert_id) values (?, ?, ?)', [question, g.user['id'], request.form['expert']])
        db.commit()
        return redirect(url_for('.unanswered'))
    
    expert_query = db.execute('select id, name from users where expert = 1')
    experts = expert_query.fetchall()
    
    return render_template('ask.html', experts=experts)

@app_bp.route('/unanswered')
@expert_required
def unanswered():
    db = get_db()
    question_query = db.execute(
        '''
        select questions.id, questions.question_text, users.name 
        from questions 
        join users on users.id = questions.asked_by_id 
        where questions.answer_text is null 
        and questions.expert_id = ?
        ''',
        [int(g.user['id'])]
    )
    questions = question_query.fetchall()
    return render_template('unanswered.html', questions=questions)

@app_bp.route('/users')
@admin_required
def users():
    db = get_db()
    user_query = db.execute('select name, id, expert, admin from users')
    users = user_query.fetchall()
    
    return render_template('users.html', users=users)

@app_bp.route('/promote')
@admin_required
def promote():
    if not 'user' in g:
        return redirect(url_for('.users'))

    db = get_db()
    db.execute('update users set expert = 1 where id = ?', request.args.get('user'))
    db.commit()
    return redirect(url_for('.users'))
