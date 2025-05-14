from flask import Blueprint, request, jsonify

from app.services.user_service import (
    register_user,
    login_user,
    get_all_users,
    get_user_info,
)
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)

user_bp = Blueprint("user", __name__)


# 注册用户
@user_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    try:
        user = register_user(data["username"], data["password"])
        if user:
            return jsonify({"msg": "注册成功！"}), 200
        else:
            return jsonify({"msg": "用户已存在！"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 404


# 用户登录
@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    user = login_user(username, password)
    if not user:
        return jsonify({"msg": "Invalid credentials"}), 401
    additional_claims = {"user_id": user.user_id}
    access_token = create_access_token(
        identity=username, additional_claims=additional_claims
    )
    return jsonify(access_token=access_token), 200


# 获取所有用户信息
@user_bp.route("/get_users", methods=["GET"])
def get_users():
    users = get_all_users()
    return jsonify([user.to_dict() for user in users]), 200


# 根据token获取当前用户信息
@user_bp.route("/user_info", methods=["GET"])
@jwt_required()  # 携带token才能访问
def get_user():
    try:
        # 从JWT token中获取当前用户id
        claims = get_jwt()
        user_id = claims["user_id"]
        username = get_jwt_identity()
        print("current_user:", user_id, username)

        # 查询数据库获取用户信息
        user = get_user_info(user_id)

        if not user:
            return jsonify({"error": "用户不存在"}), 404

        # 返回用户信息（不包括密码哈希）
        return jsonify(user.to_dict()), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# # 退出登录
# @user_bp.route("/logout", methods=["POST"])
# @jwt_required()
# def logout():
#     try:
#         # 获取当前token并将其加入黑名单
#         jti = get_jwt()["jti"]
#         return jsonify({"msg": "退出登录成功"}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# @user_bp.route('/protected', methods=['GET'])
# @jwt_required()
# def protected():
#     current_user = get_jwt_identity()
#     return jsonify(logged_in_as=current_user), 200
