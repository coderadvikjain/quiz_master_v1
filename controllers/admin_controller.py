from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import *
from datetime import datetime

admin = Blueprint('admin', __name__)

@admin.route('/admin', methods=['GET'])
@admin.route('/admin/dashboard', methods=['GET'])
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('user.login'))
    
    all_subject = Subject.query.all()
    return render_template("admin_dashboard.html",all_subject=all_subject)
    
@admin.route('/admin/add_subject', methods=['GET','POST'])
def add_subject():
    if not session.get('admin_logged_in'):
        return redirect(url_for('user.login'))
    
    if request.method =='POST':
        subject_name = request.form['subject_name']
        description = request.form['description']

        exist_subject = Subject.query.filter_by(subject_name=subject_name).first()

        if exist_subject:
            flash('⚠ Subject already exist!', 'warning')
            return redirect(url_for('admin.admin_dashboard'))

        if not exist_subject:
            new_subject = Subject(subject_name=subject_name, description=description)

            db.session.add(new_subject)
            db.session.commit()

            flash('✔ Subject added successfully!', 'success')
            return redirect(url_for('admin.admin_dashboard'))
    return redirect(url_for('user.logout'))

@admin.route('/admin/edit_subject/<subject_id>', methods=['GET','POST'])
def edit_subject(subject_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('user.login'))
    
    if request.method =='POST':
        subject = Subject.query.get_or_404(subject_id)
        subject_name = request.form['subject_name']
        description = request.form['description']

        existing_subject = Subject.query.filter_by(subject_name=subject_name).filter(Subject.id != subject_id).first()

        if existing_subject:
            flash('⚠ Subject already exist!', 'warning')
            return redirect(url_for('admin.admin_dashboard'))

        subject.subject_name = subject_name
        subject.description = description

        db.session.commit()

        flash('✔ Subject edited successfully!', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    return redirect(url_for('user.logout'))

@admin.route('/admin/delete_subject/<subject_id>', methods=['GET','POST'])
def delete_subject(subject_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('user.login'))
    
    if request.method =='POST':
        subject = Subject.query.get_or_404(subject_id)

        chapters = Chapter.query.filter_by(subject_id=subject_id).all()

        for chapter in chapters:
            quizzes = Quiz.query.filter_by(chapter_id=chapter.id).all()

            for quiz in quizzes:
                Score.query.filter_by(quiz_id=quiz.id).delete()
                Question.query.filter_by(quiz_id=quiz.id).delete()
                db.session.delete(quiz)

            db.session.delete(chapter)

        db.session.delete(subject)
        db.session.commit()

        flash('✔ Subject deleted successfully!', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    return redirect(url_for('user.logout'))
        
@admin.route('/admin/add_chapter/<subject_id>', methods=['GET','POST'])
def add_chapter(subject_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('user.login'))
    
    if request.method =='POST':
        chapter_name = request.form['chapter_name']
        description = request.form['description']

        existing_chapter = Chapter.query.filter_by(chapter_name=chapter_name,subject_id=subject_id).first()

        if existing_chapter:
            flash('⚠ Chapter already exist!', 'warning')
            return redirect(url_for('admin.admin_dashboard'))
        
        if not existing_chapter:
            new_chapter = Chapter(chapter_name=chapter_name,description=description,subject_id=subject_id)

            db.session.add(new_chapter)
            db.session.commit()

            flash('✔ Chapter added successfully!', 'success')
            return redirect(url_for('admin.admin_dashboard'))
    return redirect(url_for('user.logout'))

@admin.route('/admin/edit_chapter/<int:chapter_id>', methods=['GET','POST'])
def edit_chapter(chapter_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('user.login'))
    
    if request.method =='POST':
        chapter = Chapter.query.get_or_404(chapter_id)
        chapter_name = request.form['chapter_name']
        description = request.form['description']
        subject_id = chapter.subject_id

        exist_chapter = Chapter.query.filter_by(chapter_name=chapter_name, subject_id=subject_id).filter(Chapter.id != chapter_id).first()

        if exist_chapter:
            flash('⚠ Chapter with this name already exists!', 'warning')
            return redirect(url_for('admin.admin_dashboard'))
        
        chapter.chapter_name = chapter_name
        chapter.description = description
        
        db.session.commit()

        flash('✔ Chapter edited successfully!', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    return redirect(url_for('user.logout'))
   
@admin.route('/admin/delete_chapter/<int:chapter_id>', methods=['GET','POST'])
def delete_chapter(chapter_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('user.login'))
    
    if request.method =='POST':    
        chapter = Chapter.query.get_or_404(chapter_id)

        quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()

        for quiz in quizzes:
            Score.query.filter_by(quiz_id=quiz.id).delete()
            Question.query.filter_by(quiz_id=quiz.id).delete()
            db.session.delete(quiz)

        db.session.delete(chapter)
        db.session.commit()

        flash('✔ Chapter deleted successfully!', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    return redirect(url_for('user.logout'))

@admin.route('/admin/chapter/<int:chapter_id>/quizzes', methods=['GET'])
def chapter_quizzes(chapter_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('user.login'))
    
    chapter = Chapter.query.get_or_404(chapter_id)
    quizzes = chapter.quiz
        
    return render_template('chapter_quizzes.html', chapter=chapter, quizzes=quizzes)

@admin.route("/admin/quizzes", methods=['GET'])
def quiz_management():
    if not session.get('admin_logged_in'):
        return redirect(url_for('user.login'))
    
    all_quizzes = Quiz.query.all()
    all_chapters = Chapter.query.all()

    return render_template('quiz_management.html', all_quizzes=all_quizzes, all_chapters=all_chapters)

@admin.route("/admin/create_quiz", methods=['GET','POST'])
def create_quiz():
    if not session.get('admin_logged_in'):
        return redirect(url_for('user.login'))
    
    if request.method == 'POST':
        chapter_id = request.form['chapter_id']
        quiz_date = request.form['date_of_quiz']

        hours = int(request.form['hours'])
        minutes = int(request.form['minutes'])
        total_minutes = (hours * 60) + minutes

        if len(quiz_date) > 10:
            flash("Invalid Date!", "danger")
            return redirect(url_for('user.register'))

        existing_quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
        
        quiz_number = len(existing_quizzes) + 1
        quiz_remark = f"Quiz {quiz_number}"
        
        new_quiz = Quiz(chapter_id=chapter_id, date_of_quiz=quiz_date, duration=total_minutes, remarks=quiz_remark)

        db.session.add(new_quiz)
        db.session.commit()

        flash('✔ Quiz added successfully!', 'success')
        return redirect(url_for('admin.quiz_management'))
    return redirect(url_for('user.logout'))

@admin.route('/admin/edit_quiz/<quiz_id>', methods=['GET','POST'])
def edit_quiz(quiz_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('user.login'))
    
    quiz = Quiz.query.get_or_404(quiz_id)

    if request.method == 'POST':
        quiz_date = request.form['date_of_quiz']
        
        hours = int(request.form['hours'])
        minutes = int(request.form['minutes'])
        total_minutes = (hours * 60) + minutes

        if len(quiz_date) > 10:
            flash("Invalid Date!", "danger")
            return redirect(url_for('admin.edit_quiz', quiz_id=quiz_id))

        quiz.date_of_quiz = quiz_date
        quiz.duration = total_minutes

        db.session.commit()

        flash('✔ Quiz edited successfully!', 'success')
        return redirect(url_for('admin.quiz_management'))

    return redirect(url_for('user.logout'))

@admin.route('/admin/delete_quiz/<quiz_id>', methods=['GET','POST'])
def delete_quiz(quiz_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('user.login'))
    
    if request.method =='POST':
        quiz = Quiz.query.get_or_404(quiz_id)

        Question.query.filter_by(quiz_id=quiz_id).delete()
        Score.query.filter_by(quiz_id=quiz_id).delete()

        db.session.delete(quiz)
        db.session.commit()

        flash('✔ Quiz deleted successfully!', 'success')
        return redirect(url_for('admin.quiz_management'))
    return redirect(url_for('user.logout'))

@admin.route("/admin/add_question/<int:quiz_id>", methods=['GET','POST'])
def add_question(quiz_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('user.login'))
    
    if request.method =='POST':    
        statement = request.form['statement']
        option1 = request.form['option1']
        option2 = request.form['option2']
        option3 = request.form['option3']
        option4 = request.form['option4']
        correct_option = request.form['correct_option']

        existing_question = Question.query.filter_by(statement=statement,quiz_id=quiz_id).first()

        if existing_question:
            flash('⚠ Question already exist!', 'warning')
            return redirect(url_for('admin.quiz_management'))
        
        if not existing_question:
            new_question = Question(statement=statement, option1=option1, option2=option2, option3=option3, option4=option4, correct_option=correct_option, quiz_id=quiz_id)
            
            db.session.add(new_question)
            db.session.commit()

            flash('✔ Question added successfully!', 'success')
            return redirect(url_for('admin.quiz_management'))
    return redirect(url_for('user.logout'))

@admin.route('/admin/edit_question/<int:question_id>', methods=['GET','POST'])
def edit_question(question_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('user.login'))
    
    if request.method =='POST':
        question = Question.query.get_or_404(question_id)
        statement = request.form['statement']
        option1 = request.form['option1']
        option2 = request.form['option2']
        option3 = request.form['option3']
        option4 = request.form['option4']
        correct_option = request.form['correct_option']
        quiz_id = question.quiz_id

        existing_question = Question.query.filter_by(statement=statement,quiz_id=quiz_id).filter(Question.id != question_id).first()

        if existing_question:
            flash('⚠ Question already exists!', 'warning')
            return redirect(url_for('admin.quiz_management'))
        
        question.statement = statement
        question.option1 = option1
        question.option2 = option2
        question.option3 = option3
        question.option4 = option4
        question.correct_option = correct_option

        db.session.commit()

        flash('✔ Question edited successfully!', 'success')
        return redirect(url_for('admin.quiz_management'))
    return redirect(url_for('user.logout'))

@admin.route('/admin/delete_question/<int:question_id>', methods=['GET','POST'])
def delete_question(question_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('user.login'))

    if request.method =='POST':
        question = Question.query.get_or_404(question_id)

        db.session.delete(question)
        db.session.commit()

        flash('✔ Question deleted successfully!', 'success')
        return redirect(url_for('admin.quiz_management'))
    return redirect(url_for('user.logout'))

@admin.route('/admin/search', methods=['GET'])
def search():
    if not session.get('admin_logged_in'):
        return redirect(url_for('user.login'))
    
    query = request.args.get('query', '').strip()
    users = User.query.filter(User.role.ilike(f"%{query}%")).all()
    subjects = Subject.query.filter(Subject.subject_name.ilike(f"%{query}%")).all()
    chapters = Chapter.query.filter(Chapter.chapter_name.ilike(f"%{query}%")).all()

    results = {"Users": users,"Subjects": subjects,"Chapters" : chapters}

    return render_template('search.html', results=results, query=query)

@admin.route('/admin/summary', methods=['GET'])
def summary():
    subjects = Subject.query.all()
    subject_names = [subject.subject_name for subject in subjects]
    subject_quiz_counts = []
    
    for subject in subjects:
        quiz_count = sum(len(chapter.quiz) for chapter in subject.chapter)
        subject_quiz_counts.append(quiz_count)

    quizzes = Quiz.query.all()
    months = ['January', 'Febrary', 'March', 'April', 'May', 'June', 'July', 'August', 'Sepember', 'October', 'November', 'December']
    month_quiz_counts = [0] * 12

    for quiz in quizzes:
        quiz_date = datetime.strptime(quiz.date_of_quiz, '%Y-%m-%d')
        month_quiz_counts[quiz_date.month - 1] += 1

    return render_template('admin_summary.html', subject_names=subject_names, subject_quiz_counts=subject_quiz_counts, months=months, month_quiz_counts=month_quiz_counts)