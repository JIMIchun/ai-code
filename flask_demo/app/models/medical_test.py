from app import db

# 字段名           数据类型         描述        是否必填
# test_id         varchar(20)     检验编号     Y（主键）
# patient_id      varchar(10)     病人编号     Y 
# order           int             住院序号     Y
# test_time       varchar(20)     检验时间     Y
# related_diagnosis    varchar(200)    相关诊断     N
# specimens       varchar(10)     标本         Y
# report_item    varchar(50)     报告条目   Y
# result          varchar(20)     检验结果     Y
# unit            varchar(10)     检验单位     N
# reference_range    varchar(20)     参考范围     N
# compare_to_range    varchar(1)      对比范围     N

class MedicalTest(db.Model):
    test_id = db.Column(db.String(20), primary_key=True)
    patient_id = db.Column(db.String(10), db.ForeignKey('patient.patient_id'), nullable=False)
    order = db.Column(db.Integer, db.ForeignKey('hospital_record.order'), nullable=False)
    test_time = db.Column(db.String(20), nullable=False)
    related_diagnosis = db.Column(db.String(200))
    specimens = db.Column(db.String(10), nullable=False)
    report_item = db.Column(db.String(20),primary_key=True, nullable=False)
    result = db.Column(db.String(20), nullable=False)
    unit = db.Column(db.String(10))
    reference_range = db.Column(db.String(50))
    compare_to_range = db.Column(db.String(1))
    
    
    def to_dict(self):
        return {
            'test_id': self.test_id,
            'patient_id': self.patient_id,
            'order': self.order,
            'test_time': self.test_time,
            'related_diagnosis': self.related_diagnosis,
            'specimens': self.specimens,
            'report_item': self.report_item,
            'result': self.result,
            'unit': self.unit,
            'reference_range': self.reference_range,
            'compare_to_range': self.compare_to_range
        }
    