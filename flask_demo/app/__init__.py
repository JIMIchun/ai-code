# 目录中有 __init__.py 文件时，这个目录会被 Python 解释器当作一个包来处理
# 可以使用点号（.）来导入包中的模块
# 可以包含初始化代码，会在导入包时自动执行

# __all__ = ['patient', 'case']
# 控制哪些模块可以被 from 包名 import * 导入

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
from app.config import Config
from flask_cors import CORS

from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)  # 创建 Flask 应用实例
    app.config.from_object(config_class)  # 从指定的配置类加载配置


    db.init_app(app)  # 初始化 SQLAlchemy 数据库扩展
    migrate.init_app(app, db)  # 初始化数据库迁移扩展
    jwt = JWTManager(app)  # 初始化 JWT 扩展
    CORS(app)  # 允许所有来源的跨域请求

    # 注册蓝图
    from app.routes.patient_routes import patient_bp
    from app.routes.case_routes import case_bp
    from app.routes.knowledge_routes import knowledge_bp
    from app.routes.cea_routes import cea_bp
    from app.routes.user_routes import user_bp
    from app.routes.chat_routes import chat_bp
    from app.routes.voice_routes import voice_bp

    app.register_blueprint(patient_bp, url_prefix="/")
    app.register_blueprint(case_bp, url_prefix="/")
    app.register_blueprint(knowledge_bp, url_prefix="/")
    app.register_blueprint(chat_bp, url_prefix="/")
    app.register_blueprint(cea_bp, url_prefix="/")
    app.register_blueprint(user_bp, url_prefix="/")
    app.register_blueprint(voice_bp, url_prefix="/")
    
    from app.voice.voice_input import voice_input_bp
    app.register_blueprint(voice_input_bp, url_prefix="/")
    
    

    with app.app_context():
        db.create_all()  # 创建所有未存在的表

    return app
