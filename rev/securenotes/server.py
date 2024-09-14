import secrets
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from secret import flag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///securenotes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = '789456123'
db = SQLAlchemy(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(500), nullable=False)

@app.route('/register', methods=['POST'])
def register():
    if request.user_agent.string != "Dart/3.3 (dart:io)":
        return '', 403

    data = request.get_json()
    username = data['username']
    password = data['password']

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'message': 'User already exists'}), 400

    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 200

@app.route('/login', methods=['POST'])
def login():
    if request.user_agent.string != "Dart/3.3 (dart:io)":
        return '', 403

    data = request.get_json()
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return jsonify({'message': 'Invalid credentials'}), 400

    access_token = create_access_token(identity=user.id)
    response = jsonify({'message': 'Logged in successfully'})
    response.set_cookie('access_token', access_token, httponly=True)
    return response, 200

@app.route('/create_note', methods=['POST'])
@jwt_required()
def create_note():
    if request.user_agent.string != "Dart/3.3 (dart:io)":
        return '', 403

    user_id = get_jwt_identity()
    data = request.get_json()
    title = data.get('title', '').strip()
    content = data.get('content', '').strip()

    if not title:
        return jsonify({'message': 'Title cannot be empty'}), 400
    if not content:
        return jsonify({'message': 'Content cannot be empty'}), 400

    new_note = Note(user_id=user_id, title=title, content=content)
    db.session.add(new_note)
    db.session.commit()
    return jsonify({'message': 'Note created successfully'}), 200

@app.route('/notes', methods=['GET'])
@jwt_required()
def get_notes():
    if request.user_agent.string != "Dart/3.3 (dart:io)":
        return '', 403

    user_id = get_jwt_identity()
    notes = Note.query.filter_by(user_id=user_id).all()
    notes_data = [{'id': note.id, 'title': note.title, 'content': note.content} for note in notes]
    return jsonify(notes_data), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        existing_admin = User.query.filter_by(is_admin=True).first()

        if not existing_admin:
            admin_username = 'admin'
            admin_password = secrets.token_urlsafe(20)
            admin = User(username=admin_username, is_admin=True)
            admin.set_password(admin_password)
            db.session.add(admin)
            db.session.commit()

            flag_note = Note(user_id=admin.id, title="flag", content=flag)
            db.session.add(flag_note)
            db.session.commit()

    app.run('0.0.0.0', port=5435)