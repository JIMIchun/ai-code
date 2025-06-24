from app import db

# 字段名           数据类型         描述        是否必填
# diagnosis_id    int            自增主键     Y
# patient_id      varchar(10)    病人id      Y
# hospital_order    int          住院次数      Y
# diagnosis_order   int          诊断顺序      Y
# diagnosis_name   varchar(50)    诊断名称     Y
# diagnosis_date  varchar(20)    诊断时间     Y
# diagnosis_result varchar(10)    治疗结果     Y

class Diagnosis(db.Model):
    diagnosis_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(10), nullable=False)
    hospital_order = db.Column(db.Integer, nullable=False)
    diagnosis_order = db.Column(db.Integer, nullable=False)
    diagnosis_name = db.Column(db.String(50), nullable=False)
    diagnosis_date = db.Column(db.String(20), nullable=False)
    diagnosis_result = db.Column(db.String(10), nullable=False)


    def to_dict(self):
        return {
            'diagnosis_id': self.diagnosis_id,
            'patient_id': self.patient_id,
            'hospital_order': self.hospital_order,
            'diagnosis_order': self.diagnosis_order,
            'diagnosis_name': self.diagnosis_name,
            'diagnosis_date': self.diagnosis_date,
            'diagnosis_result': self.diagnosis_result
        }