# 实现patient相关的业务逻辑

from app.models.patient import Patient
from datetime import datetime
from app import db

def create_patient(name, gender, age, contact, address):
    patient = Patient(
        name=name,
        gender=gender,
        age=age,
        contact=contact,
        address=address,
        registration_date=datetime.now().date(),
    )
    db.session.add(patient) #将patient对象添加到数据库会话（session）中，表示这个对象即将被保存到数据库里，但此时还没有真正写入数据库
    db.session.commit() #提交当前会话中的所有变更到数据库
    return patient


def get_patient_by_id(patient_id):
    return Patient.query.get(patient_id)


def get_all_patients():
    return Patient.query.all()
