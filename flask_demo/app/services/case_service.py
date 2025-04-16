# 实现case相关的业务逻辑

from app.models.case import Case
from datetime import datetime
from app import db

def create_case(patient_id, diagnosis,case_date, treatment='', follow_up='', knowledge_id=None):
    case = Case(
        patient_id=patient_id,
        diagnosis=diagnosis,
        case_date=case_date,
        treatment=treatment,
        follow_up=follow_up,
        knowledge_id=knowledge_id,
    )
    db.session.add(case) #将case对象添加到数据库会话（session）中，表示这个对象即将被保存到数据库里，但此时还没有真正写入数据库
    db.session.commit() #提交当前会话中的所有变更到数据库
    return case


def get_case_by_id(case_id):
    return Case.query.get(case_id)

def get_cases_by_patient_id(patient_id):
    return Case.query.filter_by(patient_id=patient_id).order_by(Case.case_date.desc()).all()

def get_all_cases():
    return Case.query.all()
