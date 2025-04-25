# 实现cea指标相关的业务逻辑

from app.models.cea_level import CEALevel
from app import db

def create_cea(patient_id, time_point, ceal_level):
    cea = CEALevel(
        patient_id = patient_id,
        time_point = time_point,
        ceal_level = ceal_level
    )
    db.session.add(cea) #将patient对象添加到数据库会话（session）中，表示这个对象即将被保存到数据库里，但此时还没有真正写入数据库
    db.session.commit() #提交当前会话中的所有变更到数据库
    return cea

def get_cea_level_by_patient_id(patient_id):
    return CEALevel.query.filter_by(patient_id=patient_id).all()