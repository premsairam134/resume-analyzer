from flask import Flask, render_template, request, jsonify, send_file
import os
import shutil
from werkzeug.utils import secure_filename
from resume_parser import resume_parser
from skill_extractor import extract_skills
from job_recommender import recommend_jobs
from scoring_model import calculate_score
import pandas as pd

app = Flask(__name__)
# Absolute base path for the project
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "resumes.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this in production

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import redirect, url_for, flash
from datetime import datetime
import json

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    resumes = db.relationship('Resume', backref='user', lazy=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    score = db.Column(db.Integer, nullable=False)
    skills = db.Column(db.Text, nullable=False)  # Stored as JSON string
    recommended_jobs = db.Column(db.Text, nullable=False) # Stored as JSON string
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) # Check logic for nullable

    def __repr__(self):
        return f'<Resume {self.filename}>'

with app.app_context():
    db.create_all()

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
RESULTS_FOLDER = os.path.join(BASE_DIR, 'results')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Ensure results directory exists for export
if not os.path.exists(RESULTS_FOLDER):
    os.makedirs(RESULTS_FOLDER)

@app.route('/')
@login_required
def index():
    return render_template('index.html', name=current_user.username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists')
        else:
            new_user = User(username=username, password=generate_password_hash(password, method='scrypt'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # 1. Parse Resume
        text = resume_parser(filepath)
        if not text:
             return jsonify({'error': 'Failed to extract text. Ensure file is valid PDF/DOCX.'})

        # 2. Extract Skills
        skills = extract_skills(text)

        # 3. Job Recommendation
        recommended_jobs = recommend_jobs(skills)

        # 4. Resume Score
        score, feedback = calculate_score(text, skills, recommended_jobs)

        # Prepare response
        result = {
            'score': score,
            'skills': skills,
            'jobs': recommended_jobs,  # contains missing skills too
            'feedback': feedback
        }

        # Save to Database
        try:
            new_resume = Resume(
                filename=filename,
                score=score,
                skills=json.dumps(skills),
                recommended_jobs=json.dumps(recommended_jobs),
                user_id=current_user.id
            )
            db.session.add(new_resume)
            db.session.commit()
        except Exception as e:
            print(f"Error saving to database: {e}")

        return jsonify(result)

@app.route('/export', methods=['POST'])
def export_data():
    """Exports analysis data to CSV for Power BI."""
    data = request.json
    
    try:
        df = pd.DataFrame(data)
        csv_path = os.path.join(RESULTS_FOLDER, 'analysis_export.csv')
        df.to_csv(csv_path, index=False)
        return send_file(csv_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
