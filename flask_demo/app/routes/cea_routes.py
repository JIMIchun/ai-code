# 定义CEA指标相关的路由,解析请求数据

from flask import Blueprint, request, jsonify
from app.services.cea_service import  get_cea_level_by_patient_id

cea_bp = Blueprint('cea_level', __name__)

'''根据患者ID获取CEA指标信息'''
@cea_bp.route('/cea_level/<int:patient_id>', methods=['GET'])
def get_cea_level(patient_id):
    try:
        cea_level = get_cea_level_by_patient_id(patient_id)
        return jsonify([cea.to_dict() for cea in cea_level]) 
    except ValueError as e:
        return jsonify({'error': str(e)}), 404