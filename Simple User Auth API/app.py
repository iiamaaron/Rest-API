from flask import Flask, request, jsonify  # Core Flask framework + request handling + JSON responses
from flask_sqlalchemy import SQLAlchemy # ORM for database management
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity  # JWT authentication manager
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)# Initialize the Flask application

# Configure the database URI (SQLite database stored in 'auth.db')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///auth.db"
# Configure the secret key for JWT (used to sign tokens)
app.config["JWT_SECRET_KEY"] = "xheader453.payload.sign345"

db = SQLAlchemy(app)# Initialize the database object with the Flask app
jwt = JWTManager(app)# Initialize JWT manager with the Flask app

# Define a User model (represents a table in the database)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

# Create all database tables within the application context
with app.app_context():
    db.create_all() # Ensure tables are created

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the login page"})

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json() #Flask parses the raw JSON string into Python objects
    username = data.get("username")
    password = data.get("password")
    if not username:
        return jsonify({"error": "Username not found"}), 400
    if not password:
        return jsonify({"error": "Password not found"}), 400
    else:
        hashed = generate_password_hash(password) # Hash the password
        if User.query.filter_by(username=username).first(): #Check if username already exists
            return jsonify({"error": "Username already exists"}), 400
        # Create new User and save
        user = User(
            username = username,
            password = hashed
        )

        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "user created successfully"}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() #Flask parses the raw JSON string into Python objects
    # Get the username and password
    username = data.get("username")
    password = data.get("password")
    # Validate both fields
    if not username:
        return jsonify({"error": "Username not found"}),  400
    if not password:
        return jsonify({"error": "Password not found"}), 400
    else:
        # Find the user by username in the database
        user = User.query.filter_by(username=username).first()
        # If user does not exist, return an error
        if not user:
            return jsonify({"error": "User not found"}), 404
        # check if password matches user password, else return error
        if not check_password_hash(user.password, password):
            return jsonify({"error": "Wrong password"}), 401
        token = create_access_token(identity=str(user.id)) # Else generate JWT token
        return jsonify({"token": token}) # Return token

@app.route("/profile", methods=["GET"])
@jwt_required() #Protects this route
def profile():
    user_id = get_jwt_identity() #Gets user id from token
    user = User.query.get(int(user_id))
    return jsonify({"id": user_id, "username": user.username})

# Run the Flask application in debug mode
if __name__ == "__main__":
    app.run(debug=True)