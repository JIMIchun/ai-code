# 目录中有 __init__.py 文件时，这个目录会被 Python 解释器当作一个包来处理
# 可以使用点号（.）来导入包中的模块
# 可以包含初始化代码，会在导入包时自动执行

# __all__ = ['patient', 'case']
# 控制哪些模块可以被 from 包名 import * 导入

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import inspect
from app.config import Config
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)  # 创建 Flask 应用实例
    app.config.from_object(config_class)  # 从指定的配置类加载配置

    db.init_app(app)  # 初始化 SQLAlchemy 数据库扩展
    migrate.init_app(app, db)  # 初始化数据库迁移扩展
    CORS(app)   #允许所有来源的跨域请求
        
    # 注册蓝图
    from app.routes.patient_routes import patient_bp
    from app.routes.case_routes import case_bp
    from app.routes.knowledge_routes import knowledge_bp
    from app.routes.chat_routes import chat_bp

    app.register_blueprint(patient_bp, url_prefix="/")
    app.register_blueprint(case_bp, url_prefix='/')
    app.register_blueprint(knowledge_bp, url_prefix='/')
    app.register_blueprint(chat_bp, url_prefix='/')
        
    with app.app_context():
        db.create_all()  # 创建所有未存在的表
        
        # 创建数据库引擎,使用inspect 获取所有表的名称
        # engine = db.engine
        # inspector = inspect(engine)
        # table_names = inspector.get_table_names()
        # print(f"tables: {table_names}")
        
        
    return app
