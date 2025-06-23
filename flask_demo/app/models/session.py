from app import db
from datetime import datetime,timezone

# 定义Session模型， 记录用户与模型的会话信息,包含多条Message
# 字段名    数据类型    描述   是否必填
# session_id    INT	    会话唯一标识符（主键）  是
# user_id       INT     用户唯一标识符（外键）  是
# patient_id    INT     模型唯一标识符（外键）  是
# title         VARCHAR 会话标题  否
# created_time  DATETIME    创建时间  是
# updated_time  DATETIME    更新时间  否


class Session(db.Model):
    session_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.patient_id"), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    created_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_time = db.Column(db.DateTime, nullable=True)
    
    
    def to_dict(self):
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "patient_id": self.patient_id,
            "title": self.title,
            "created_time": self.created_time.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_time": self.updated_time.strftime("%Y-%m-%d %H:%M:%S") if self.updated_time else None
        }
