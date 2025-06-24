from app import db

# 字段名    数据类型    描述   是否必填
# patient_id    int    病人id    是
# order    int    住院次数    是
# admission_department    varchar(100)    入院科室    是
# discharge_department    varchar(100)    出院科室    是
# admission_time    varchar(20)    入院时间    是
# discharge_time    varchar(20)    出院时间    是

class HospitalRecord(db.Model):
    patient_id = db.Column(db.Integer, nullable=False)  
    order = db.Column(db.Integer, nullable=False) 
    admission_department = db.Column(db.String(100), nullable=False)
    discharge_department = db.Column(db.String(100), nullable=False)
    admission_time = db.Column(db.String(20), nullable=False)
    discharge_time = db.Column(db.String(20), nullable=False)
    
    # 复合主键
    __table_args__ = (
        db.PrimaryKeyConstraint('patient_id', 'order'),
    )
    
    def to_dict(self):
        return {
            "patient_id": self.patient_id,
            "order": self.order,
            "admission_department": self.admission_department,
            "discharge_department": self.discharge_department,
            # 将datetime转换为年/月/日 时/分/秒的字符串格式
            "admission_time": self.admission_time,
            "discharge_time": self.discharge_time,
        }