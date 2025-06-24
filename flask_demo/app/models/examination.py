from app import db

# 字段名           数据类型         描述        是否必填
# exam_id       varchar(10)    检查号    Y
# patient_id    varchar(10)    病人编号    Y
# order         int            检查单号    Y
# exam_type     varchar(20)    检查类型    Y
# clinical_impression   varchar(200)    临床印象    N
# impression    varchar(200)    检查印象    N
# related_diagnosis    varchar(200)    相关诊断    N
# clinical_diagnosis     varchar(200)    临床诊断    N
# exam_desc     varchar(500)    检查描述    N


class Examination(db.Model):
    exam_id = db.Column(db.String(10), primary_key=True)
    patient_id = db.Column(db.String(10), db.ForeignKey('patient.patient_id'))
    order = db.Column(db.Integer, db.ForeignKey('hospital_record.order')) 
    exam_type = db.Column(db.String(20), nullable=False)
    clinical_impression = db.Column(db.String(200))
    impression = db.Column(db.String(200))
    related_diagnosis = db.Column(db.String(200))
    clinical_diagnosis = db.Column(db.String(200))
    exam_desc = db.Column(db.String(500))
    
    
    def to_dict(self):
        return {
            'exam_id': self.exam_id,
            'patient_id': self.patient_id,
            'order': self.order,
            'exam_type': self.exam_type,
            'clinical_impression': self.clinical_impression,
            'impression': self.impression,
            'related_diagnosis': self.related_diagnosis,
            'clinical_diagnosis': self.clinical_diagnosis,
            'exam_desc': self.exam_desc
        }