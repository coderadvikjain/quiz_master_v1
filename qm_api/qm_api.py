from flask import Blueprint, request
from flask_restful import Api, Resource
from models import *

qm_api = Blueprint('qm_api', __name__)
api = Api(qm_api)

class UserRegisterResource(Resource):
    def post(self):
        data = request.json
        if not data.get("username") or not data.get("password") or not data.get("full_name"):
            return {"message": "Missing required fields (username, password, full_name)"}, 400

        if User.query.filter_by(username=data["username"]).first():
            return {"message": "Username already exists!"}, 409
        
        new_user = User(username=data["username"], password=data["password"], full_name=data["full_name"], qualification=data.get("qualification"), dob=data.get("dob"))

        db.session.add(new_user)
        db.session.commit()

        return {"message": "User registered successfully!"}, 201

class SubjectListResource(Resource):
    def get(self):
        subjects = Subject.query.all()

        if not subjects:
            return {"message": "No subjects found."}, 404
        
        result = [{"id": s.id, "name": s.subject_name, "description": s.description} for s in subjects]
        return result

class ChapterListResource(Resource):
    def get(self, subject_id):

        chapters = Chapter.query.filter_by(subject_id=subject_id).all()

        if not chapters:
            return {"message": "No chapters found for the given subject."}, 404
        
        result = [{"id": c.id, "name": c.chapter_name, "description": c.description} for c in chapters]
        return result

class QuizListResource(Resource):
    def get(self, chapter_id):

        quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
        if not quizzes:

            return {"message": "No quizzes found for the given chapter."}, 404
        
        result = [{"id": q.id, "date_of_quiz": q.date_of_quiz, "duration": q.duration} for q in quizzes]
        return result

class QuestionListResource(Resource):
    def get(self, quiz_id):

        questions = Question.query.filter_by(quiz_id=quiz_id).all()

        if not questions:
            return {"message": "No questions found for the given quiz."}, 404
        
        result = [
            {
                "id": q.id,
                "statement": q.statement,
                "option1": q.option1,
                "option2": q.option2,
                "option3": q.option3,
                "option4": q.option4,
                "correct_option": q.correct_option,
            }
            for q in questions
        ]
        return result

api.add_resource(UserRegisterResource, '/api/register')
api.add_resource(SubjectListResource, '/api/subjects')
api.add_resource(ChapterListResource, '/api/subject/<int:subject_id>/chapters')
api.add_resource(QuizListResource, '/api/chapter/<int:chapter_id>/quizzes')
api.add_resource(QuestionListResource, '/api/quiz/<int:quiz_id>/questions')