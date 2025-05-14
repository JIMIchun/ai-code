# 定义患者相关的路由,解析请求数据

from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt, jwt_required
from app.services.patient_service import create_patient, get_patient_by_id, get_all_patients, get_patients_by_user

patient_bp = Blueprint('patient', __name__)

'''
@description: 添加新患者
'''
@patient_bp.route('/patients', methods=['POST'])
def add_patient():
    data = request.json
    try:
        patient = create_patient(
            name=data['name'],
            gender=data['gender'],
            age=data['age'],
            contact=data['contact'],
            address=data.get('address', '')
        )
        return jsonify(patient.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    

'''根据患者ID获取患者信息'''
@patient_bp.route('/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    try:
        patient = get_patient_by_id(patient_id)
        return jsonify(patient.to_dict())
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

'''根据user_id获取名下所有患者信息'''
@patient_bp.route('/get_patients_by_user', methods=['GET'])
@jwt_required()  # 携带token才能访问
def get_user_patients():
    try:
        claims = get_jwt()
        user_id = claims["user_id"]
        # 查询数据库获取用户名下患者信息
        patients = get_patients_by_user(user_id)
        return jsonify([patient.to_dict() for patient in patients]) 
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
        
        
'''获取所有患者信息'''
@patient_bp.route('/patients', methods=['GET'])
def list_patients():
    patients = get_all_patients()
    return jsonify([patient.to_dict() for patient in patients])