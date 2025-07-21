from app import create_app
import json
import os
import datetime

from app.models.patient import Patient
from app.models.hospital_record import HospitalRecord
from app.models.examination import Examination
from app.models.medical_test import MedicalTest
from app.models.operation import Operation
from app.models.physical_sign import PhysicalSign
from app.models.medication import Medication
from app.models.diagnosis import Diagnosis

from app.services.query import *
from app.services.chat_service import chat_with_model


def test_db():
    app = create_app()
    with app.app_context():
        queryAll('926845', 1)
        # process_pdf('./app/assets/knowledge.pdf')

# 查询数据并生成病历
def queryAll(patient_id, order):
    patient=get_patient_by_id(patient_id)
    hospitalRecord=get_hosrecords_by_order_id(order)
    physicalSigns = get_physical_signs(patient_id, order)
    examinations = get_examinations(patient_id, order)
    medicalTests = get_medical_tests(patient_id, order)
    operations = get_operations(patient_id, order)
    medications = get_medications(patient_id, order)
    diagnoses = get_diagnoses(patient_id, order)
    
    # 生成病历
    gen_note = generate_progress_note(patient, hospitalRecord, physicalSigns, examinations, medicalTests, diagnoses, medications, operations)
    
    # 查看/generate_file/下的文件数量
    file_list = os.listdir('./generate_file/')
    file_num = len(file_list)
    # 将结果写入/generate_file/下的病历.md文件中
    with open('./generate_file/病历'+str(file_num+1)+'_'+datetime.now().strftime('%m%d%H%M')+'.md', 'w', encoding='utf-8') as f:
        f.write(gen_note)
        f.close()

        
    
    # patient_info = '姓名：'+patient.name+',性别：'+patient.gender+',年龄：'+str(patient.age)+',住院次数：'+str(order)
    # physign_info = '体征数据：'+str([physign.sign_item+'：'+physign.sign_value+'('+physign.sign_unit if physign.sign_unit is not None else '' +');' for physign in physicalSigns])
    # exam_info = '检查结果：'+str([exam.exam_type+'：'+exam.impression+' 临床诊断：'+exam.clinical_diagnosis  +';' for exam in examinations])
    # test_info = '检验数据：'+str([test.report_item+'：'+test.result+'('+test.unit if test.unit is not None else '' +');' for test in medicalTests])
    # diagnosis_info = '诊断结果：'+str([str(dia.diagnosis_order)+'.'+dia.diagnosis_name+','+dia.diagnosis_result+','+dia.diagnosis_date +';' for dia in diagnoses])
    # medication_info = '用药记录：'+str([med.medication_name+'：'+med.dosage+' '+med.dosage_unit+'，'+med.usage+'，'+med.start_date+'-'+med.end_date+'，'+med.frequency if med.frequency is not None else '' +';' for med in medications])
    # operation_info = '手术记录：'+str([str(op.operation_order)+'：' +op.operation_name+'，'+op.operation_time+';' for op in operations])
    
    # input = patient_info +'\n'+ physign_info +'\n'+ exam_info +'\n'+ test_info +'\n'+ diagnosis_info +'\n'+ medication_info +'\n'+ operation_info
    # print(input)
    
    
def generate_progress_note(patient, hospitalRecord, physicalSigns, examinations, medicalTests, diagnoses, medications, operations): 
    """ 生成新的病程记录 """ 
    input_data =f""" 现有患者信息： {patient.to_dict()} 
        住院记录：{hospitalRecord.to_dict()}  
        体征数据：{[physign.to_dict() for physign in physicalSigns]}
        检查结果：{[exam.to_dict() for exam in examinations]}
        检验数据：{[test.to_dict() for test in medicalTests]}
        诊断结果：{[dia.to_dict() for dia in diagnoses]}
        用药记录：{[med.to_dict() for med in medications]}
        手术记录：{[op.to_dict() for op in operations]}
        请严格基于以上信息生成一份完整的住院病程记录，保持格式规范。 格式如下：
        首先给出患者的基本信息和本次住院的基本情况，下面用一条横线表示分隔，
        然后依次记录主诉、现病史、既往史、个人史、婚育史、家族史，下面用横线分隔，
        然后依次记录体格检查、专科检查、辅助检查的内容，并注明时间、检查项目、检查结果、诊断结果、用药情况、手术情况等，
        最后给出智能助手建议，提醒需要注意的事项。      
        以上内容请严格按照所给数据进行记录，未提供数据的部分可以用“暂无”替代。
        """ 
    # 发送请求到大模型 
    try:
        response = chat_with_model(input_data)
        return response
    except:
        return "模型出错，请稍后再试"

# def optimize_progress_note(progress_note): 
#     """ 优化 AI 生成的病程记录 """ 
#     optimized_note = clean_text(progress_note) # 清理冗余信息
#     optimized_note = improve_sentence_flow(optimized_note) # 使句子更流畅 
#     optimized_note = format_standardization(optimized_note) # 确保格式符合病历规范 
#     return optimized_note
        

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
import os

# 初始化
# shibing624/text2vec-base-chinese: 基于Text2Vec的中文语义表示模型
embeddings = HuggingFaceEmbeddings(
    model_name="shibing624/text2vec-base-chinese",
    model_kwargs={'device': 'cpu'},  # 'cuda'
    encode_kwargs={'normalize_embeddings': True}
)

# 处理PDF文件->向量存储
def process_pdf(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    # 文本分割
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,       # 每个文本块的字符数
        chunk_overlap=200,     # 相邻文本块的重叠字符数
        length_function=len    # 计算长度的函数
    )
    texts = text_splitter.split_documents(documents)

    # text = "糖尿病患者的血糖控制标准"
    # vector = embeddings.embed_query(text)
    # print(f"向量维度：{len(vector)}")
    
    # 创建向量存储
    vectordb = Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory=os.path.join('uploads', 'chroma_db')
    )
    vectordb.persist()
    
    return vectordb


if __name__ == "__main__":
    test_db()
