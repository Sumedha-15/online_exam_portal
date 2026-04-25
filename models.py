from flask_sqlalchemy import SQLAlchemy #tool that let us uses database without writing sql queries
from flask_login import UserMixin #makes our user login ready
from werkzeug.security import generate_password_hash, check_password_hash #password encryption tools
from datetime import datetime

db = SQLAlchemy()

#creates user table in db
class User(UserMixin, db.Model):
    #usermixin adds login functionality and db.model makes it a database model
    """User model for both admin and student roles."""
    id = db.Column(db.Integer, primary_key=True) #auto incrementing unique id for each user
    username = db.Column(db.String(80), unique=True, nullable=False)
    #unique = true no 2 users can have the same username and email and nullable = false means these fields cannot be empty
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False) #stores the hashed password instead of plain text for security
    full_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student') #stores whether user is admin or student default =student
    created_at = db.Column(db.DateTime, default=datetime.utcnow) #automatically saves date and time when user is created 

    # links user table to exam and examAttempt tables 
    #lazy=true  means dont load related data until its actually needed
    exams_created = db.relationship('Exam', backref='creator', lazy=True)
    attempts = db.relationship('ExamAttempt', backref='student', lazy=True)

    def set_password(self, password): #setpassword encrypts and save password when registering

        self.password_hash = generate_password_hash(password)

    def check_password(self, password):#checkpassword compares the entered password with the stored hashed password during login
        return check_password_hash(self.password_hash, password)

#table 2  -exam table to store all details of exams
#links exam to the admin who created it and to the attempts made by students and to the questions in the exam
class Exam(db.Model):
    """Exam model containing exam metadata."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    subject = db.Column(db.String(100), nullable=False, default='General')
    duration_minutes = db.Column(db.Integer, nullable=False)
    total_marks = db.Column(db.Integer, nullable=False)
    passing_percentage = db.Column(db.Integer, default=40)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True) #admin can hide/show exam to students
    proctoring_enabled = db.Column(db.Boolean, default=True)#whether webcam monitoring is on
    max_violations = db.Column(db.Integer, default=5) #number of violations allowed before exam is flagged
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    questions = db.relationship('Question', backref='exam', lazy=True, cascade='all, delete-orphan')
    #if exam is deleted all related questions and attempts will also be deleted to maintain data integrity
    attempts = db.relationship('ExamAttempt', backref='exam', lazy=True)

#table 3 - question table to store all questions for each exam
class Question(db.Model):
    """Question model for exam questions."""
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20), nullable=False)  # 'mcq' or 'short_answer'
    option_a = db.Column(db.String(500))
    option_b = db.Column(db.String(500))
    option_c = db.Column(db.String(500))
    option_d = db.Column(db.String(500))
    correct_answer = db.Column(db.String(500), nullable=False)
    marks = db.Column(db.Integer, nullable=False, default=1)
    order_num = db.Column(db.Integer, default=0) #used to maintain the order of questions in the exam

#table 4 - exam attempt table to track each student's attempt at an exam and their answers and any violations during the exam
class ExamAttempt(db.Model):
    """Tracks each student's exam attempt."""
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    score = db.Column(db.Integer, default=0)
    total_marks = db.Column(db.Integer, default=0)
    percentage = db.Column(db.Float, default=0.0)
    is_flagged = db.Column(db.Boolean, default=False) #true if student crossed max violations
    violation_count = db.Column(db.Integer, default=0) #total number of cheating attempt
    status = db.Column(db.String(20), default='in_progress')

    # Relationships
    answers = db.relationship('Answer', backref='attempt', lazy=True, cascade='all, delete-orphan')
    violations = db.relationship('Violation', backref='attempt', lazy=True, cascade='all, delete-orphan')

#table 5 - answer table to store each student's answer for each question in the exam and whether it is correct or not
class Answer(db.Model):
    """Stores student answers for each question."""
    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('exam_attempt.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    student_answer = db.Column(db.String(500))
    is_correct = db.Column(db.Boolean, default=False)

#table 6 - violation table to log any proctoring violations during the exam such as multiple faces detected, no face detected, suspicious movements etc
class Violation(db.Model):
    """Logs proctoring violations during exams."""
    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('exam_attempt.id'), nullable=False)
    violation_type = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    details = db.Column(db.Text)
