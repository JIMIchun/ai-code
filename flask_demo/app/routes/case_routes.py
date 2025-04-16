# 定义患者相关的路由,解析请求数据

from flask import Blueprint, request, jsonify
from app.services.case_service import  get_case_by_id, get_cases_by_patient_id

case_bp = Blueprint('case', __name__)

'''根据病历ID获取患者病历信息'''
@case_bp.route('/cases/<int:case_id>', methods=['GET'])
def get_case(case_id):
    try:
        case = get_case_by_id(case_id)
        return jsonify(case.to_dict())
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

'''根据患者ID获取患者所有病历信息'''
@case_bp.route('/cases_by_patient/<int:patient_id>', methods=['GET'])
def get_cases(patient_id):
    try:
        cases = get_cases_by_patient_id(patient_id)
        return jsonify([case_.to_dict() for case_ in cases])
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
