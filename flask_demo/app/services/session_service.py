# 实现session相关的业务逻辑

from app.models.session import Session
from app.models.message import Message
from datetime import datetime
from app import db
from app.models.enums import MessageType, IdentityType


def create_session(user_id, patient_id, title):
    session = Session(
        user_id=user_id,
        patient_id=patient_id,
        title=title,
        created_time=datetime.now(),
        updated_time=datetime.now()
    )
    db.session.add(session)
    db.session.commit()
    return session


def change_session_title(session_id, title):
    session = Session.query.filter_by(session_id=session_id).first()
    session.title = title
    db.session.commit()
    return session


def get_sessions_by_user_patient(user_id, patient_id):
    return (
        Session.query.filter_by(user_id=user_id, patient_id=patient_id)
        .order_by(Session.updated_time.desc())
        .all()
    )


def create_message(session_id, identity_type, message_type, content, inference=""):
    message = Message(
        session_id=session_id,
        identity_type=identity_type,
        message_type=message_type,
        content=content,
        inference=inference,
        created_time=datetime.now(),
    )
    db.session.add(message)
    db.session.commit()
    return message


def get_messages_by_session_id(session_id):
    return (
        Message.query.filter_by(session_id=session_id)
        .order_by(Message.created_time.asc())
        .all()
    )


def delete_session_by_session_id(session_id):
    try:
        session = Session.query.filter_by(session_id=session_id).first()
        # 删除session相关的所有消息
        messages = Message.query.filter_by(session_id=session_id).all()
        for message in messages:
            db.session.delete(message)
        db.session.delete(session)
        db.session.commit()
        return session
    except Exception as e:
        raise Exception(f"Database operation failed: {str(e)}")

def update_sission_time(session_id):
    try:
        session = Session.query.filter_by(session_id=session_id).first()
        session.updated_time = datetime.now()
        db.session.commit()
        return session
    except Exception as e:
        raise Exception(f"Database operation failed: {str(e)}")