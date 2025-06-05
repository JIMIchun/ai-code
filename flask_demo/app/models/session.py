from app import db


class User(db.Model):
    session_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=False)
    message_type = db.Column(db.Integer, nullable=False)
    message_list = db.Column(db.String(10000), nullable=False)
    created_time = db.Column(db.DateTime, nullable=False)
    updated_time = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "patient_id": self.patient_id,
            "message_type": self.message_type,
            "message_list": self.message_list,
            "created_time": self.created_time.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_time": self.updated_time.strftime("%Y-%m-%d %H:%M:%S"),
        }
