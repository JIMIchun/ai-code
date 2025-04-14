from app import db
from datetime import datetime

# 定义Case模型
# 字段名    数据类型    描述   是否必填
# case_id    INT    患者病历编号(主键)    是
# patient_id    INT    患者编号(外键)    是
# diagnosis    TEXT    诊断    是
# case_date    TEXT    患者病历日期    是
# treatment    TEXT    治疗方案    否
# follow_up    TEXT    随访内容    否
# knowledge_id    INT    医疗知识库编号(外键)    否

class Case(db.Model):
    case_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'), nullable=False)
    diagnosis = db.Column(db.Text, nullable=False)
    case_date = db.Column(db.Text, nullable=False)
    treatment = db.Column(db.Text)
    follow_up = db.Column(db.Text)
    knowledge_id = db.Column(db.Integer, db.ForeignKey('knowledge.knowledge_id'))

    def to_dict(self):
        return {
            'case_id': self.case_id,
            'patient_id': self.patient_id,
            'diagnosis': self.diagnosis,
            'treatment': self.treatment,
            'case_date': self.case_date,
            'follow_up': self.follow_up,
            'knowledge_id': self.knowledge_id
        }