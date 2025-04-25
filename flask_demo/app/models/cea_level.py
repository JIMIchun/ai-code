from app import db
from datetime import datetime

# 定义CEA指标模型
# 字段名    数据类型    描述   是否必填
# item_id    int    主键    是
# patient_id    int    外键    是
# time_point    str    时间点    是
# ceal_level    str    CEA指标值    是


class CEALevel(db.Model):
    item_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'), nullable=False)
    time_point = db.Column(db.Text, nullable=False)
    ceal_level = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"CEALevel('{self.item_id}', '{self.patient_id}', '{self.time_point}', '{self.ceal_level}')"

    def to_dict(self):
        return {
            'item_id': self.item_id,
            'patient_id': self.patient_id,
            'time_point': self.time_point,
            'ceal_level': self.ceal_level
        }