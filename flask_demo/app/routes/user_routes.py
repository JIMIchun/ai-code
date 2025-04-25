from flask import Blueprint, request, jsonify

from app.services.user_service import register_user, login_user, get_all_users
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity 
)

user_bp = Blueprint('user', __name__)

# 注册用户
@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    try:
        user = register_user(data['username'], data['password'])
        if user:
            return jsonify({"msg": "注册成功！"}), 200
        else:
            return jsonify({"msg": "用户已存在！"}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 404

# 用户登录
@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = login_user(username, password)
    if not user:
        return jsonify({"msg": "Invalid credentials"}), 401
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

@user_bp.route('/get_users', methods=['GET'])
def get_users():
    users = get_all_users()
    return jsonify([user.to_dict() for user in users]), 200

# @user_bp.route('/protected', methods=['GET'])
# @jwt_required()
# def protected():
#     current_user = get_jwt_identity()
#     return jsonify(logged_in_as=current_user), 200