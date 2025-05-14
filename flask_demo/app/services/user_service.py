# 实现user相关的业务逻辑

from app.models.user import User
from app import db
from flask import jsonify

# 注册用户
def register_user(username, password):
    if User.query.filter_by(username=username).first():
        return None
    
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user

# 用户登录
def login_user(username, password):
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return None
    return user

# 获取用户信息
def get_user_info(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        return None
    return user

# 获取所有用户
def get_all_users():
    return User.query.all()