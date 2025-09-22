from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    qualification = db.Column(db.String(100), nullable=True)
    dob = db.Column(db.String(50), nullable=True)
    role = db.Column(db.String(10), default='user')

class Subject(db.Model):
    __tablename__ = "Subject"
    id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(150), unique=True, nullable=False)
    description = db.Column(db.String(300), nullable=True)
    chapter = db.relationship('Chapter', backref='subject')

class Chapter(db.Model):
    __tablename__ = "Chapter"
    id = db.Column(db.Integer, primary_key=True)
    chapter_name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(300), nullable=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('Subject.id'), nullable=False)

class Quiz(db.Model):
    __tablename__ = "Quiz"
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('Chapter.id'), nullable=False)
    date_of_quiz = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    remarks = db.Column(db.String(300), nullable=True)
    chapter = db.relationship('Chapter', backref='quiz')
    questions = db.relationship('Question', backref='quiz')

class Question(db.Model):
    __tablename__ = "Question"
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('Quiz.id'), nullable=False)
    statement = db.Column(db.String(500), nullable=False)
    option1 = db.Column(db.String(200), nullable=False)
    option2 = db.Column(db.String(200), nullable=False)
    option3 = db.Column(db.String(200), nullable=False)
    option4 = db.Column(db.String(200), nullable=False)
    correct_option = db.Column(db.Integer, nullable=False)

class Score(db.Model):
    __tablename__ = "Score"
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('Quiz.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    time_taken = db.Column(db.Integer, nullable=False)
    total_score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    quiz = db.relationship('Quiz', backref='score')
    user = db.relationship('User', backref='score')