from app import db

# 定义Patient模型，每个模型对应数据库中的一张表
# 字段名    数据类型    描述   是否必填
# patient_id    INT	    患者唯一标识符（主键）  是
# name	   VARCHAR(100)	  患者姓名	          是
# gender	VARCHAR(10)	患者性别（男/女/其他）	是
# age	INT	患者年龄	是
# contact	VARCHAR(100)	患者联系方式	是
# address	VARCHAR(255)	患者地址	否
# registration_date	DATE	患者注册日期	是


class Patient(db.Model):
    patient_id = db.Column(db.Integer, primary_key=True)  # 数据类型为整数，表的主键
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255))
    registration_date = db.Column(db.Date, nullable=False)

    # 关联病例表
    # 定义一对多关系：允许通过 patient.cases 访问某个患者的所有病例
    # backref：允许通过 case.patient 访问某个病例相关的患者
    # lazy=True : 访问 cases 属性时才会加载相关的 Case 实例
    cases = db.relationship("Case", backref="patient", lazy=True)

    # 定义to_dict方法，用于将模型对象转换为字典
    def to_dict(self):
        return {
            "patient_id": self.patient_id,
            "name": self.name,
            "gender": self.gender,
            "age": self.age,
            "contact": self.contact,
            "address": self.address,
            "registration_date": self.registration_date.isoformat(),
        }
