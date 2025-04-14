# 实现knowledge相关的业务逻辑

from app.models.knowledge import Knowledge
from datetime import datetime
from app import db

def create_knowledge(disease_name, description, symptoms, treatment_options, prevention):
    knowledge = Knowledge(
        disease_name=disease_name,
        description=description,
        symptoms=symptoms,
        treatment_options=treatment_options,
        prevention=prevention,
        created_date=datetime.now().date(),
    )
    db.session.add(knowledge) #将knowledge对象添加到数据库会话（session）中，表示这个对象即将被保存到数据库里，但此时还没有真正写入数据库
    db.session.commit() #提交当前会话中的所有变更到数据库
    return knowledge


def get_knowledge_by_id(knowledge_id):
    return Knowledge.query.get(knowledge_id)


def get_all_knowledges():
    return Knowledge.query.all()
