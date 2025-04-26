from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
from flask_migrate import Migrate
from enum import Enum
from flask import abort
from functools import wraps
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, curren
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)  
CORS(app)  # Enable CORS for all routes
load_dotenv()  # Load environment variables from .env file

app.secret_key = 'your_secret_key_h"
import uuid


app = Flask(__name__)  
app.secret_key = os.getenv("SECRET_KEY", "dev_key")


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure upload folder early
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'jpg', 'png'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # redirects if user not logged in

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


class Role(Enum):
    STUDENT = "student"
    ADMIN = "admin"
    DEV = "dev"

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != role:

                abort(403)  # Forbidden access
            return f(*args, **kwargs)
        return decorated_function
    return decorator

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(100), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    profile_pic = db.Column(db.String(255), nullable=True)
    role = db.Column(db.Enum(Role), default=Role.STUDENT, nullable=False)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    video_link = db.Column(db.String(500), nullable=True)  # Optional Video Link
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    uploader_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    uploader = db.relationship('User', backref='notes')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)  # This logs in the user
            flash("✅ Login successful!", "success")
            return redirect(url_for('home'))
        
        flash("⚠️ Invalid email or password. Try again!", "error")
        return redirect(url_for('login'))

    return render_template('LOGINPAGE.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form.get('password')  # Use .get()
        confirm_password = request.form.get('confirm_password')  # Use .get()

        if not confirm_password:
            flash("⚠️ Confirm Password field is missing!", "error")
            return redirect(url_for('signup'))

        if password != confirm_password:
            flash("⚠️ Passwords do not match! Try again.", "error")
            return redirect(url_for('signup'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("⚠️ Email already exists! Try logging in instead.", "error")
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("✅ Account created successfully! You can now log in.", "success")
        return redirect(url_for('login'))

    return render_template('SIGNUP.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()  # Use Flask-Login's logout_user instead of manually handling session
    flash("You have been logged out.", "success")
    return redirect(url_for('home'))

@app.route('/c_programming')
def c_programming():
    notes = Note.query.filter_by(subject="c_programming").all()
    return render_template('c_programming.html', notes=notes)

@app.route('/operating_system')
def operating_system():
    notes = Note.query.filter_by(subject="operating_system").all()
    return render_template('operating_system.html', notes=notes)

@app.route('/scm')
def scm():
    notes = Note.query.filter_by(subject="scm").all()
    return render_template('scm.html', notes=notes)

@app.route('/deca')
def deca():
    notes = Note.query.filter_by(subject="deca").all()
    return render_template('deca.html', notes=notes)

@app.route('/dent')
def dent():
    notes = Note.query.filter_by(subject="dent").all()
    return render_template('dent.html', notes=notes)

@app.route('/python')
def python():
    notes = Note.query.filter_by(subject="python").all()
    return render_template('python.html', notes=notes)

@app.route('/casa')
def casa():
    notes = Note.query.filter_by(subject="casa").all()
    return render_template('casa.html', notes=notes)

@app.route('/mcp')
def mcp():
    notes = Note.query.filter_by(subject="mcp").all()
    return render_template('mcp.html', notes=notes)

@app.route('/fee')
def fee():
    notes = Note.query.filter_by(subject="fee").all()
    return render_template('fee.html', notes=notes)

@app.route('/404notfound')
def not_found():
    return render_template('404notfound.html')

@app.route('/download/<subject>/<filename>')
def download_notes(subject, filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], subject), filename)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = current_user  # Use Flask-Login's current_user

    if request.method == 'POST':
        user.name = request.form.get('name')
        user.bio = request.form.get('bio')

        file = request.files.get('profile_pic')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'profiles', filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            file.save(filepath)
            user.profile_pic = filename

        db.session.commit()
        flash("✅ Profile updated successfully!", "success")
        return redirect(url_for('profile'))

    return render_template('profile.html', user=user)

@app.route('/upload_notes', methods=['GET', 'POST'])
@login_required
@role_required(Role.ADMIN)  # Only admins can access this
def upload_notes():
    if request.method == 'POST':
        subject = request.form.get('subject')  # Get subject from dropdown
        file = request.files.get('file')
        video_link = request.form.get('video_link')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], subject, filename)

            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            file.save(filepath)

            new_note = Note(
                filename=filename, 
                filepath=filepath, 
                subject=subject, 
                video_link=video_link, 
                uploader_id=current_user.id
            )
            db.session.add(new_note)
            db.session.commit()

            flash(f"✅ Notes uploaded successfully for {subject}!", "success")
            return redirect(url_for('upload_notes'))  # Stay on the same page after upload

        flash("⚠️ Invalid file format!", "error")

    return render_template('upload_notes.html')
# In app.py, after defining app
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER']), exist_ok=True)
for subject in ['c_programming', 'operating_system', 'scm', 'deca', 'dent', 'profiles']:
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], subject), exist_ok=True)

# Ai chat bot
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("WARNING: No GEMINI_API_KEY found in environment variables!")
else:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400

    if not api_key:
        return jsonify({'response': 'Chat service is currently unavailable. API key not configured.'}), 200

    # Keyword filter
    allowed_keywords = ['notes', 'lecture', 'assignment', 'subject', 'topic', 'exam', 'discussion', 'schedule']
    if not any(keyword in user_input.lower() for keyword in allowed_keywords):
        return jsonify({'response': "❌ Please ask something related to your subjects or class content."}), 200

    # Prompt control
    chat_prompt = f"""
    You are CampusConnect AI, a helpful assistant only allowed to respond to queries related to class notes, subjects, schedules, and other academic content from the CampusConnect platform.

    If the question is unrelated (like personal advice, random trivia, jokes, etc.), respond with:
    "I'm here to help only with CampusConnect-related queries. Please ask something relevant to your classes or subjects."
    
    User question: {user_input}
    """
    
    # Keyword filter (optional)
    allowed_keywords = ['notes', 'lecture', 'assignment', 'subject', 'topic', 'exam', 'discussion', 'schedule']
    if not any(keyword in user_input.lower() for keyword in allowed_keywords):
        return jsonify({'response': "❌ Please ask something related to your subjects or class content."}), 200

    # 🧠 Dynamically build the list of subjects from the database
    try:
        subjects = Note.query.with_entities(Note.subject).distinct().all()
        subject_links = "\n".join([f"- {subj[0].capitalize()} notes: /{subj[0]}" for subj in subjects])
    except Exception as e:
        print(f"Error fetching subjects: {str(e)}")
        subject_links = "Sorry, I couldn't load subjects right now."

    try:
        response = model.generate_content(chat_prompt)
        return jsonify({'response': response.text})
    except Exception as e:
        print(f"Error in chat API: {str(e)}")
        return jsonify({'response': 'Sorry, I encountered an error processing your request.'}), 200

# Removed the line as 'file' is undefined in this context and not used elsewhere


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)