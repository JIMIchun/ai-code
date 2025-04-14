from app import db
from datetime import datetime

# 定义医疗知识模型
# 字段名    数据类型    描述   是否必填
# knowledge_id    INT    医疗知识ID(主键)   是
# disease_name    VARCHAR(100)    疾病名称    是
# description    TEXT    疾病描述    是
# symptoms    TEXT    症状描述    是
# treatment_options    TEXT    治疗选项    是   
# prevention    TEXT    预防措施    否
# created_date    DATE    创建日期    是

class Knowledge(db.Model):
    knowledge_id = db.Column(db.Integer, primary_key=True)
    disease_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    symptoms = db.Column(db.Text, nullable=False)
    treatment_options = db.Column(db.Text, nullable=False)
    prevention = db.Column(db.Text)
    created_date = db.Column(db.Date, nullable=False)
    
    # 关联病例表
    # cases = db.relationship('Case', backref='knowledge', lazy=True)

    def to_dict(self):
        return {
            'knowledge_id': self.knowledge_id,
            'disease_name': self.disease_name,
            'description': self.description,
            'symptoms': self.symptoms,
            'treatment_options': self.treatment_options,
            'prevention': self.prevention,
            'created_date': self.created_date.isoformat()
        }