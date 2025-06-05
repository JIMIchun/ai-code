# 实现session相关的业务逻辑

from app.models.session import Session
from datetime import datetime
from app import db


def create_session(user_id, patient_id):
    session = Session(user_id = user_id, patient_id = patient_id, created_time=datetime.now())
    db.session.add(session)
    db.session.commit()
    return session