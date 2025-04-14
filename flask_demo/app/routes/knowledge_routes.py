# 定义 医疗知识 相关的路由,解析请求数据

from flask import Blueprint, request, jsonify
from app.services.knowledge_service import create_knowledge, get_knowledge_by_id, get_all_knowledges

knowledge_bp = Blueprint('knowledge', __name__)

'''
@description: 添加knowledge
'''
@knowledge_bp.route('/knowledge', methods=['POST'])
def add_knowledge():
    data = request.json
    try:
        knowledge = create_knowledge(
            disease_name=data['disease_name'],
            description=data['description'],
            symptoms=data['symptoms'],
            treatment_options=data['treatment_options'],
            prevention=data['prevention']
        )
        return jsonify(knowledge.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

'''根据knowledge的ID获取信息'''
@knowledge_bp.route('/knowledge/<int:knowledge_id>', methods=['GET'])
def get_knowledge(knowledge_id):
    try:
        knowledge = get_knowledge_by_id(knowledge_id)
        return jsonify(knowledge.to_dict())
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    

'''获取所有klg信息'''
@knowledge_bp.route('/knowledge', methods=['GET'])
def list_knowledges():
    knowledges = get_all_knowledges()
    return jsonify([knowledge.to_dict() for knowledge in knowledges])