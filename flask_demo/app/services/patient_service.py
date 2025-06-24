# 实现patient相关的业务逻辑

from app.models.patient import Patient
from datetime import datetime
from app import db

# 传入参数必须是(形参=实参, ...)
def create_patient(**kwargs):
    patient = Patient(**kwargs
        # name=kwargs.name,
        # gender=kwargs.gender,
        # doctor_id=kwargs.doctor_id if kwargs.doctor_id else None,
        # age=kwargs.age,
        # contact=kwargs.contact if kwargs.contact else None,
        # address=kwargs.address if kwargs.address else None,
        # registration_date=datetime.now(),
        # birth_date=kwargs.birth_date,
    )
    db.session.add(patient) #将patient对象添加到数据库会话（session）中，表示这个对象即将被保存到数据库里，但此时还没有真正写入数据库
    db.session.commit() #提交当前会话中的所有变更到数据库
    return patient


def get_patient_by_id(patient_id):
    return Patient.query.get(patient_id)

def get_patients_by_user(user_id):
    return Patient.query.filter_by(doctor_id=user_id).all()


def get_all_patients():
    return Patient.query.all()
