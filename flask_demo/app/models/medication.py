from app import db

# 字段名           数据类型         描述        是否必填
# medication_id   int             药品id      Y
# patient_id      varchar(10)     病人id      Y
# hospital_order  int             住院次数     Y
# medication_name varchar(255)    用药名称     Y
# dosage          varchar(10)     剂量        Y
# dosage_unit     varchar(10)     剂量单位     Y
# usage           varchar(10)     用药方式     Y
# start_date      varchar(20)     开始日期     N
# end_date        varchar(20)     结束日期     N
# frequency       varchar(10)     用药频率     N
# note            varchar(200)    备注        N

class Medication(db.Model):
    medication_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(10), db.ForeignKey('patient.patient_id'), nullable=False)
    hospital_order = db.Column(db.Integer, db.ForeignKey('hospital_record.order'), nullable=False)
    medication_name = db.Column(db.String(255), nullable=False)
    dosage = db.Column(db.String(10), nullable=False)
    dosage_unit = db.Column(db.String(10), nullable=False)
    usage = db.Column(db.String(10), nullable=False)
    start_date = db.Column(db.String(20), nullable=True)
    end_date = db.Column(db.String(20), nullable=True)
    frequency = db.Column(db.String(10), nullable=True)
    note = db.Column(db.String(200), nullable=True)

    def to_dict(self):
        return {
            "medication_id": self.medication_id,
            "patient_id": self.patient_id,
            "hospital_order": self.hospital_order,
            "medication_name": self.medication_name,
            "dosage": self.dosage,
            "dosage_unit": self.dosage_unit,
            "usage": self.usage,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "frequency": self.frequency,
            "note": self.note
        }