# 定义患者相关的路由,解析请求数据

from flask import Blueprint, request, jsonify
from app.services.case_service import  get_case_by_id

case_bp = Blueprint('case', __name__)

'''根据患者ID获取患者信息'''
@case_bp.route('/cases/<int:case_id>', methods=['GET'])
def get_case(case_id):
    try:
        case = get_case_by_id(case_id)
        return jsonify(case.to_dict())
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
