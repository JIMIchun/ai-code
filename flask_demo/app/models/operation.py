from app import db

# 字段名           数据类型         描述        是否必填
# operation_id    varchar(10)     手术id     Y
# patient_id      varchar(10)     病人id     Y
# hospital_order  int             住院次数    Y
# operation_order int             手术序号    Y
# operation_name   varchar(50)    手术姓名    Y
# operation_time   varchar(20)    手术时间    Y
# healing_level   varchar(10)     治愈等级    N
# incision_type   varchar(10)     切口类型    N
# anesthesia_type varchar(10)     麻醉类型    N
# operation_level  varchar(10)    手术级别    N


class Operation(db.Model):
    operation_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(10), db.ForeignKey('patient.patient_id'), nullable=False)
    hospital_order = db.Column(db.Integer, db.ForeignKey('hospital_record.order'), nullable=False)
    operation_order = db.Column(db.Integer, nullable=False)
    operation_name = db.Column(db.String(50), nullable=False)
    operation_time = db.Column(db.String(20), nullable=False)
    healing_level = db.Column(db.String(10))
    incision_type = db.Column(db.String(10))
    anesthesia_type = db.Column(db.String(10))
    operation_level = db.Column(db.String(10))
    
    
    def to_dict(self):
        return {
            'operation_id': self.operation_id,
            'patient_id': self.patient_id,
            'order_id': self.order_id,            
            'operation_name': self.operation_name,
            'operation_time': self.operation_time,
            'healing_level': self.healing_level,
            'incision_type': self.incision_type,
            'anesthesia_type': self.anesthesia_type,
            'operation_level': self.operation_level
        }