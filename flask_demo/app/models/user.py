
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

# 定义User模型，每个模型对应数据库中的一张表
# 字段名    数据类型    描述   是否必填
# user_id    INT	    用户唯一标识符（主键）  是
# username   VARCHAR(80)   用户名   是
# password_hash   VARCHAR(256)  用户密码哈希值  是

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            "username": self.username
        }