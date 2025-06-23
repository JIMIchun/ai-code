# 定义对话信息相关的路由

from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt, jwt_required
from app.models.session import Session
from app.services.session_service import *
from app.models.enums import MessageType, IdentityType


session_bp = Blueprint("session", __name__)


# 新建会话, 传入参数{patient_id:xxx, title:xxx}
@session_bp.route("/new_session", methods=["POST"])
@jwt_required()
def new_session():
    data = request.get_json()
    claims = get_jwt()
    try:
        session = create_session(claims["user_id"], data["patient_id"], data["title"])
        return jsonify(session.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# 修改session标题title
@session_bp.route("/update_session_title", methods=["POST"])
@jwt_required()
def update_session_title():
    data = request.get_json()
    try:
        session = change_session_title(data["session_id"], data["title"])
        return jsonify(session.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# 获取会话列表
@session_bp.route("/get_sessions/<int:patient_id>", methods=["GET"])
@jwt_required()
def get_sessions(patient_id):
    claims = get_jwt()
    try:
        sessions = get_sessions_by_user_patient(claims["user_id"], patient_id)
        return jsonify([session.to_dict() for session in sessions]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# 新建消息, 传入参数{session_id:xxx, message_type:xxx, identity_type:xxx, content:xxx, inference:xxx}
@session_bp.route("/new_message", methods=["POST"])
@jwt_required()
def new_message():
    data = request.get_json()
    try:
        message = create_message(
            data["session_id"],
            data["identity_type"],
            data["message_type"],
            data["content"],
            data["inference"],
        )
        update_sission_time(data["session_id"])
        return jsonify(message.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# 获取特定会话的消息列表，传入参数{session_id:xxx}
@session_bp.route("/get_messages/<int:session_id>", methods=["GET"])
@jwt_required()
def get_messages(session_id):
    try:
        messages = get_messages_by_session_id(session_id)
        return jsonify([message.to_dict() for message in messages]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
    
# 删除会话
@session_bp.route("/delete_session/<int:session_id>", methods=["DELETE"])
@jwt_required()
def delete_session(session_id):
    try:
        delete_session_by_session_id(session_id)
        return jsonify({"message": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
