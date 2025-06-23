from flask import Blueprint, request, jsonify
import time
from app.services.chat_service import chat_with_model

chat_bp = Blueprint("chat", __name__)




# 接收前端发送的输入，并返回模型的回答
@chat_bp.route("/send_input", methods=["POST"])
def send_input():
    try:
        user_input = request.get_json()["input_text"]  # 获取前端传来的数据
        print(f"用户输入: {user_input}，时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")

        assistant_reply = chat_with_model(user_input)  # 调用模型进行聊天
        print(f"模型回复: {assistant_reply}")
        # 返回模型的回答
        return jsonify(response=assistant_reply), 200
    except Exception as e:
        return jsonify(error=str(e)), 500


