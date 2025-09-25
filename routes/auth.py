from flask import Blueprint, request, jsonify
from models.user import User
from extensions import bcrypt   
from flask_jwt_extended import create_access_token, jwt_required, set_access_cookies 
from datetime import timedelta

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        user = User.query.filter_by(email=email).first()
        additional_claims={"role":user.role, "email":user.email, "name":user.name}  
        if user and bcrypt.check_password_hash(user.password, password):

            access_token = create_access_token(identity=str(user.id), additional_claims=additional_claims, expires_delta=timedelta(hours=1))
            response = jsonify({"message": "Login successful"})
            set_access_cookies(response, access_token)
            return response, 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"error": f"Something went wrong: {str(e)}"}), 500

@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    response = jsonify({"message": "Logout successful"})
    response.delete_cookie("access_token_cookie")
    return response, 200    



