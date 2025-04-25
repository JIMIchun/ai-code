import os

# 数据库配置
# JWT配置

class Config:
    # 指定数据库的连接地址
    # 查询当前操作系统的环境变量，没有则使用默认的数据库地址
    # mysql://登陆名:密码@地址/数据库名称
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+mysqlconnector://username:password@localhost/medical_db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///medical.db'
    
    # 控制是否跟踪对象的修改并发送信号
    # False：禁用对象修改跟踪，这可以减少内存使用并提高性能
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    #查询时会显示原始SQL语句 
    SQLALCHEMY_ECHO= True
    
    # 生产环境应使用环境变量
    # os.environ.get('JWT_SECRET_KEY', 'default_secret_key')
    JWT_SECRET_KEY= 'your-secret-key-keep-it-safe' 
    # 1小时过期
    JWT_ACCESS_TOKEN_EXPIRES = 3600  
    
    