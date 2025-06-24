from app import db

# 字段名           数据类型         描述        是否必填
# sign_id         int             体征记录id   Y(主键)
# patient_id      str(10)         病人id      Y
# hospital_order  int             住院次数 Y
# sign_item       str(50)         记录项目    Y
# sign_value      str(50)         记录数据      Y
# sign_unit       str(20)         体征单位    N
# record_time     str(20)         记录时间    Y

class PhysicalSign(db.Model):
    sign_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(10), db.ForeignKey('patient.patient_id'))
    hospital_order=db.Column(db.Integer, db.ForeignKey('hospital_record.order'))
    sign_item=db.Column(db.String(50), nullable=False)
    sign_value=db.Column(db.String(50), nullable=False)
    sign_unit=db.Column(db.String(20))
    record_time=db.Column(db.String(20), nullable=False)
    
    
    def to_dict(self):
        return {
            'sign_id': self.sign_id,
            'patient_id': self.patient_id,
            'hospital_order': self.hospital_order,
            'sign_item': self.sign_item,
            'sign_value': self.sign_value,
            'sign_unit': self.sign_unit,
            'record_time': self.record_time
        }