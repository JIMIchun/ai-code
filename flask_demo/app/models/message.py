from app import db
from app.models.enums import MessageType, IdentityType

# 定义Message模型， 记录每个对话消息
# message_id    INT   消息ID  主键
# session_id    INT   会话ID  外键
# identity_type INT   身份类型（IdentityType枚举）  是
# message_type  INT   消息类型（MessageType枚举）  是
# content       TEXT  消息内容  是
# inference     TEXT  推理结果  否
# created_time  DATETIME  创建时间  是


class Message(db.Model):
    message_id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(
        db.Integer, db.ForeignKey("session.session_id"), nullable=False
    )
    message_type = db.Column(db.Enum("TEXT", "IMAGE", "VIDEO"), nullable=False)
    identity_type = db.Column(db.Enum("MODEL", "USER"), nullable=False)
    content = db.Column(db.String(10000), nullable=False)
    inference = db.Column(db.String(10000), nullable=True)
    created_time = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        return {
            "message_id": self.message_id,
            "session_id": self.session_id,
            "message_type": self.message_type,
            "identity_type": self.identity_type,
            "content": self.content,
            "inference": self.inference if self.inference else "",
            "created_time": self.created_time.strftime("%Y-%m-%d %H:%M:%S"),
        }
