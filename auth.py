from datetime import timedelta
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy, scoped_session
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['JWT_SECRET_KEY'] = 'jwt_secret_key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

db = SQLAlchemy(app)
database_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=db.engine))
jwt_manager = JWTManager(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password_hash(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

@app.before_first_request
def initialize_database():
    db.create_all()

@app.teardown_appcontext
def cleanup_database_session(exception=None):
    database_session.remove()

@app.route('/register', methods=['POST'])
def user_registration():
    user_data = request.get_json()
    username = user_data.get('username')
    password = user_data.get('password')
    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "Username already exists"}), 409
    new_user = User(username=username)
    new_user.set_password_hash(password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User successfully created"}), 201

@app.route('/login', methods=['POST'])
def user_login():
    credentials = request.get_json()
    username = credentials.get('username')
    password = credentials.get('password')
    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return jsonify({"message": "Invalid username or password"}), 401
    user_access_token = create_access_token(identity=username)
    user_refresh_token = create_refresh_token(identity=username)
    return jsonify(access_token=user_access_token, refresh_token=user_refresh_token), 200

@app.route('/protected', methods=['GET'])
@jwt_required()
def access_protected_resource():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

if __name__ == '__main__':
    app.run(debug=True)