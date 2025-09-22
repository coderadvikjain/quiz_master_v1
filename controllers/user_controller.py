from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import *
from datetime import datetime

user = Blueprint('user', __name__)

@user.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        full_name = request.form['full_name']
        qualification = request.form['qualification']
        dob = request.form['dob']

        if len(dob) > 10:
            flash("Please Enter correct DOB", "danger")
            return redirect(url_for('user.register'))

        if User.query.filter_by(username=username).first():
            flash("Username already exists", "danger")
            return redirect(url_for('user.register'))
        
        new_user = User(username=username, password=password, full_name=full_name, qualification=qualification, dob=dob)

        db.session.add(new_user)
        db.session.commit()

        flash("✔ Registration successful!", "success")
        return redirect(url_for('user.login'))
    return render_template('register.html')

@user.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:
            if user.role == 'admin':
                session['admin_logged_in'] = True
                session['user_id'] = user.id
                return redirect(url_for('admin.admin_dashboard'))
            elif user.role == 'user':
                session['user_logged_in'] = True
                session['user_id'] = user.id
                session['full_name'] = user.full_name
                return redirect(url_for('user.user_dashboard'))
        else:
            flash("Invalid login credentials", "danger")
    return render_template('login.html')

@user.route('/dashboard', methods=['GET','POST'])
def user_dashboard():
    if not session.get('user_logged_in'):
        return redirect(url_for('user.login'))
    
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    quizzes = Quiz.query.all()
    if user:
        full_name = user.full_name

    return render_template("dashboard.html", full_name=full_name, quizzes=quizzes)

@user.route('/attempt_quiz/<int:quiz_id>', methods=['GET','POST'])
def attempt_quiz(quiz_id):
    if not session.get('user_logged_in'):
        return redirect(url_for('user.login'))
    
    if 'quiz_progress' not in session or session.get('quiz_id') != quiz_id:
        session['quiz_progress'] = 0
        session['score'] = 0
        session['quiz_id'] = quiz_id
        session['quiz_duration'] = Quiz.query.get(quiz_id).duration
        session['quiz_start_time'] = datetime.now().isoformat()

    question_no = session['quiz_progress']
    total_questions = Question.query.filter_by(quiz_id=quiz_id).count()

    if question_no >= total_questions:
        return redirect(url_for('user.quiz_result', quiz_id=quiz_id))

    quiz_start_time = datetime.fromisoformat(session['quiz_start_time'])
    elapsed_time = (datetime.now() - quiz_start_time).total_seconds()

    if elapsed_time >= session['quiz_duration'] * 60:
        return redirect(url_for('user.quiz_result', quiz_id=quiz_id))

    question = Question.query.filter_by(quiz_id=quiz_id).offset(question_no).first()
    quiz = Quiz.query.get(quiz_id)

    if request.method == 'POST':
        if 'previous' in request.form:
            if session['quiz_progress'] > 0:
                session['quiz_progress'] -= 1
            return redirect(url_for('user.attempt_quiz', quiz_id=quiz_id))

        if 'next' in request.form:
            selected_option = request.form.get('answer')
            if selected_option and int(selected_option) == question.correct_option:
                session['score'] += 1

            session['quiz_progress'] += 1

        if session['quiz_progress'] < total_questions:
            return redirect(url_for('user.attempt_quiz', quiz_id=quiz_id))
        else:
            quiz_end_time = datetime.now()
            time_taken_seconds = (quiz_end_time - quiz_start_time).total_seconds()

            minutes = int(time_taken_seconds // 60)
            seconds = int(time_taken_seconds % 60)
            time_taken = f"{minutes}:{seconds:02d}"
            session['time_taken'] = time_taken 
            return redirect(url_for('user.quiz_result', quiz_id=quiz_id))

    return render_template('attempt_quiz.html', quiz=quiz, question=question, q_no=question_no + 1, total=total_questions, show_previous=(question_no > 0), quiz_start_time=session['quiz_start_time'], quiz_duration=session['quiz_duration'])

@user.route('/quiz_result/<int:quiz_id>', methods=['GET'])
def quiz_result(quiz_id):
    if not session.get('user_logged_in'):
        return redirect(url_for('user.login'))

    user_id = session.get('user_id')
    if 'quiz_id' not in session or session.get('quiz_id') != quiz_id:
        return redirect(url_for('user.user_dashboard'))
    
    quiz = Quiz.query.get(quiz_id)
    total_questions = Question.query.filter_by(quiz_id=quiz_id).count()
    correct_answers = session['score']
    wrong_answers = total_questions - correct_answers
    score_percentage = (correct_answers / total_questions) * 100

    existing_score = Score.query.filter_by(quiz_id=quiz_id,user_id=user_id).first()

    if existing_score:
        existing_score.total_score = correct_answers
        existing_score.total_questions = total_questions
        existing_score.time_taken = session.get('time_taken', 0)
    else:
        new_score = Score(quiz_id=quiz_id,user_id=user_id,time_taken=session.get('time_taken'),total_score=correct_answers,total_questions=total_questions)

        db.session.add(new_score)
    db.session.commit()

    session.pop('quiz_progress', None)
    session.pop('score', None)
    session.pop('quiz_id', None)
    session.pop('quiz_start_time', None)
    session.pop('quiz_duration', None)

    return render_template('quiz_result.html', quiz=quiz, correct_answers=correct_answers, wrong_answers=wrong_answers, total_questions=total_questions, score_percentage=score_percentage)

@user.route('/scores', methods=['GET'])
def scores():
    if not session.get('user_logged_in'):
        return redirect(url_for('user.login'))
    
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    scores = Score.query.filter_by(user_id=user_id).all()

    quiz_ids = [score.quiz_id for score in scores]
    quizzes = Quiz.query.filter(Quiz.id.in_(quiz_ids)).all()

    if user:
        full_name = user.full_name

    return render_template('scores.html', scores=scores, full_name=full_name, quizzes=quizzes)

@user.route('/summary', methods=['GET'])
def summary():
    if not session.get('user_logged_in'):
        return redirect(url_for('user.login'))
    
    user_id = session['user_id']
    user = User.query.get(user_id)
    scores = Score.query.filter_by(user_id=user_id).all()

    if user:
        full_name = user.full_name

    quiz_names = []
    quiz_scores = []
    total_questions = []

    for score in scores:
        quiz = score.quiz
        quiz_names.append(f"{quiz.chapter.chapter_name} {quiz.remarks} ({quiz.chapter.subject.subject_name})")
        quiz_scores.append(score.total_score)

        question_count = score.total_questions
        total_questions.append(question_count)

    return render_template('summary.html', full_name=full_name, quiz_names=quiz_names, quiz_scores=quiz_scores, total_questions=total_questions)

@user.route('/search', methods=['GET'])
def searches():
    if not session.get('user_logged_in'):
        return redirect(url_for('user.login'))
    
    user_id = session['user_id']
    user = User.query.get(user_id)

    if user:
        full_name = user.full_name

    query = request.args.get('query', '').strip()
    subjects = Subject.query.filter(Subject.subject_name.ilike(f"%{query}%")).all()
    chapters = Chapter.query.filter(Chapter.chapter_name.ilike(f"%{query}%")).all()

    subject_ids = [subject.id for subject in subjects]
    chapter_ids = [chapter.id for chapter in chapters]

    quizzes = Quiz.query.join(Chapter).join(Subject).filter((Quiz.chapter_id.in_(chapter_ids)) | (Chapter.subject_id.in_(subject_ids))).all()

    results = {"Subjects": subjects,"Chapters": chapters,"Quizzes": quizzes}

    return render_template('searches.html', full_name=full_name, results=results, query=query)

@user.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('home'))