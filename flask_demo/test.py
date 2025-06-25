from app import create_app
import json

from app.models.patient import Patient
from app.models.hospital_record import HospitalRecord
from app.models.examination import Examination
from app.models.medical_test import MedicalTest
from app.models.operation import Operation
from app.models.physical_sign import PhysicalSign
from app.models.medication import Medication
from app.models.diagnosis import Diagnosis

from app.services.query import *
from app.services.chat_service import send_message


def test_db():
    app = create_app()
    with app.app_context():
        queryAll('926845', 1)
        
        # 清空表
        # MedicalTest.query.delete()
        # db.session.commit()
        
        # initHospitalRecords()
        # print(len(HospitalRecord.query.all()))
        
        # initExaminations()
        # print(len(Examination.query.all()))
        
        # initOperations()
        # print(len(Operation.query.all()))
        # initPhysicalSigns()
        # print(len(PhysicalSign.query.all()))
        
        # initMedicalTest()
        # print(len(MedicalTest.query.all()))
        
        # initMedication()
        # print(len(Medication.query.all()))
        
        # initDiagnosis()
        # print(len(Diagnosis.query.all()))
        

        
def queryAll(patient_id, order):
    patient=get_patient_by_id(patient_id)
    hospitalRecord=get_hosrecords_by_order_id(order)
    physicalSigns = get_physical_signs(patient_id, order)
    examinations = get_examinations(patient_id, order)
    medicalTests = get_medical_tests(patient_id, order)
    operations = get_operations(patient_id, order)
    medications = get_medications(patient_id, order)
    diagnoses = get_diagnoses(patient_id, order)
    
    generate_progress_note(patient, physicalSigns, examinations, medicalTests,diagnoses,medications,operations)
    
    # print('患者信息：')
    # print(patient.to_dict())
    # print('体征数据：')
    # print([physign.to_dict() for physign in physicalSigns])
    # print('检查数据：')
    # print([exam.to_dict() for exam in examinations])
    # print('检验数据：') 
    # print([test.to_dict() for test in medicalTests])
    # print('手术数据：')
    # print([op.to_dict() for op in operations])
    # print('用药数据：')
    # print([med.to_dict() for med in medications])
    # print('诊断数据：')
    # print([dia.to_dict() for dia in diagnoses])
    
    
def generate_progress_note(patient, physicalSigns, examinations, medicalTests,diagnoses,medications,operations): 
    """ 生成新的病程记录 """ 
    input_data =f""" 现有患者资料： {patient.to_dict()} 
        体征数据：{[physign.to_dict() for physign in physicalSigns]}
        检查结果：{[exam.to_dict() for exam in examinations]}
        检验数据：{[test.to_dict() for test in medicalTests]}
        诊断结果：{[dia.to_dict() for dia in diagnoses]}
        用药记录：{[med.to_dict() for med in medications]}
        手术记录：{[op.to_dict() for op in operations]}
        请基于以上信息生成一份完整的病程记录，保持格式规范。 """ 
    # 发送请求到大模型 
    try:
        response = send_message(input_data)
        return response
    except:
        return "模型出错，请稍后再试"

# def optimize_progress_note(progress_note): 
#     """ 优化 AI 生成的病程记录 """ 
#     optimized_note = clean_text(progress_note) # 清理冗余信息
#     optimized_note = improve_sentence_flow(optimized_note) # 使句子更流畅 
#     optimized_note = format_standardization(optimized_note) # 确保格式符合病历规范 
#     return optimized_note
        
        


from app.services.patient_service import create_patient, get_all_patients
from app.services.case_service import create_case, get_all_cases
from app.services.knowledge_service import create_knowledge, get_all_knowledges
from app.services.cea_service import create_cea
from app import db
from datetime import datetime

import pandas as pd


# 写入patient数据
def initPatients():
    file_path = "./app/assets/基本信息.csv"
    try:
        df = pd.read_csv(file_path, encoding="GBK")  # 读取 CSV 数据
        for index, row in df.iterrows():
            # 查询Patient表中是否存在该patient_id
            patient = Patient.query.filter_by(patient_id=row['PATIENT_ID']).first()
            if patient:
                continue
            create_patient(
                patient_id = row['PATIENT_ID'], 
                name=row["SUBSTR(P.NAME,1,1)||'**'"], 
                gender=row['性别'],
                birth_date=row['生日'],
                # 根据birth_date计算年龄age
                age=datetime.now().year-int(row['生日'][:4]),
                registration_date=datetime.strftime(datetime.now(), '%Y/%m/%d %H:%M:%S'),
                nationality=row['民族']
            )
    except Exception as e:
        print(e)
        return

# 写入住院记录数据
def initHospitalRecords():
    file_path = "./app/assets/基本信息.csv"
    try:
        df = pd.read_csv(file_path, encoding="GBK")  # 读取 CSV 数据
        for index, row in df.iterrows():
            hosRecord = HospitalRecord(
                patient_id=row['PATIENT_ID'],
                order=row['住院次数'],
                admission_department = row['入院院科室'],
                discharge_department = row['出院科室'],
                admission_time = row['入院时间'],
                discharge_time = row['出院时间'],
            )
            db.session.add(hosRecord)
            db.session.commit()
    except Exception as e:
        print(e)
        return

def initExaminations():
    file_path = "./app/assets/检查.csv"
    try:
        df = pd.read_csv(file_path, encoding="GBK")  # 读取 CSV 数据
        for index, row in df.iterrows():
            examination = Examination(
                exam_id=row['检查号'],
                patient_id=row['住院号'],
                order=row['住院次数'],
                exam_type = row['检查类型'],
                clinical_impression = row['临床印象'],
                impression = row['检查印象'],
                related_diagnosis = row['相关诊断'],
                clinical_diagnosis = row['临床诊断'],
                exam_desc = row['检查描述']
            )
            db.session.add(examination)
            db.session.commit()
    except Exception as e:
        print(e)
        return

def initMedicalTest():
    file_path = "./app/assets/检验.csv"
    try:
        df = pd.read_csv(file_path, encoding="GBK")  # 读取 CSV 数据
        
        for index, row in df.iterrows():
            test = MedicalTest(
                test_id=row['检验号'],
                patient_id=row['住院号'],
                order=row['住院次数'],
                test_time = row['检验时间'],
                related_diagnosis = row['相关临床诊断'],
                specimens = row['标本'],                
                report_item = row['报告条目'],
                result = row['结果'],
                unit = row['单位'],
                reference_range = row['正常参考范围'],
                compare_to_range = row['与参考范围相比较']
            )
            db.session.add(test)
            db.session.commit()
    except Exception as e:
        print(e)
        return

def initOperations():
    file_path = "./app/assets/手术.csv"
    try:
        df = pd.read_csv(file_path, encoding="GBK")  # 读取 CSV 数据
        for index, row in df.iterrows():
            operation = Operation(
                patient_id=row['住院号'],
                hospital_order=row['住院次数'],
                operation_order=row['手术顺序'],
                operation_name = row['手术名称'],
                operation_time = row['手术时间'],
                healing_level = row['愈合等级'],
                incision_type = row['切口类型'],
                anesthesia_type = row['麻醉类型'],
                operation_level = row['手术级别']
            )
            db.session.add(operation)
            db.session.commit()
    except Exception as e:
        print(e)
        return

def initPhysicalSigns():
    file_path = "./app/assets/体征.csv"
    try:
        df = pd.read_csv(file_path, encoding="GBK")  # 读取 CSV 数据
        for index, row in df.iterrows():
            sign = PhysicalSign(
                patient_id=row['住院号'],
                hospital_order=row['住院次数'],
                record_time=row['记录时间'],
                sign_item = row['记录项目'],
                sign_value = row['记录数据'],
                sign_unit = row['单位']
            )
            db.session.add(sign)
            db.session.commit()
    except Exception as e:
        print(e)
        return

def initMedication():
    file_path = "./app/assets/用药.csv"
    try:
        df = pd.read_csv(file_path, encoding="GBK")  # 读取 CSV 数据
        for index, row in df.iterrows():
            medication = Medication(
                patient_id=row['住院号'],
                hospital_order=row['住院次数'],
                medication_name = row['用药名称'],
                dosage = row['剂量'],
                dosage_unit = row['剂量单位'],
                usage = row['用药方式'],
                start_date = row['开始时间'],
                end_date = row['结束时间'],
                frequency = row['用药频率'],
                note = row['备注']
            )
            db.session.add(medication)
            db.session.commit()
    except Exception as e:
        print(e)
        return
          
def initDiagnosis():
    file_path = "./app/assets/诊断.csv"
    try:
        df = pd.read_csv(file_path, encoding="GBK")  # 读取 CSV 数据
        for index, row in df.iterrows():
            diagnosis = Diagnosis(
                patient_id=row['住院号'],
                hospital_order=row['住院次数'],
                diagnosis_order=row['诊断顺序'],
                diagnosis_name = row['诊断名称'],
                diagnosis_date = row['诊断时间'],
                diagnosis_result = row['治疗结果']
            )
            db.session.add(diagnosis)
            db.session.commit()
    except Exception as e:
        print(e)    
        return


def initCases():
    file_path = "./app/assets/cases.json"
    with open(file_path, "r", encoding="utf-8") as file:
        cases_data = json.load(file)  # 加载 JSON 数据
        for case in cases_data:
            create_case(
                patient_id=case["patient_id"],
                diagnosis=case["diagnosis"],
                case_date=case["case_date"],
                treatment=case["treatment"],
                follow_up=case["follow_up"],
                knowledge_id=case["knowledge_id"],
            )


def initKnowledges():
    file_path = "./app/assets/knowledge.json"
    with open(file_path, "r", encoding="utf-8") as file:
        knowledge_data = json.load(file)  # 加载 JSON 数据
        for knowledge in knowledge_data:
            create_knowledge(
                disease_name=knowledge["disease_name"],
                description=knowledge["description"],
                symptoms=knowledge["symptoms"],
                treatment_options=knowledge["treatment_options"],
                prevention=knowledge["prevention"],
            )

# 写入cea指标数据
def initCEA():
    file_path = "./app/assets/cea_level.json"
    with open(file_path, "r", encoding="utf-8") as file:
        cea_data = json.load(file)  # 加载 JSON 数据
        for data in cea_data:
            create_cea(
                patient_id=data["patient_id"],
                time_point=data["time_point"],
                ceal_level=data["ceal_level"],
            )


# 读取数据
def readData():
    print("all patients:")
    for p in get_all_patients():
        print(p.to_dict())
    # print("all cases:")
    # for c in get_all_cases():
    #     print(c.to_dict())
    # print("all knowledges:")
    # for k in get_all_knowledges():
    #     print(k.to_dict())


def handleDoctor_id():
    # 给patient中的前五条数据添加doctor_id
    patients = get_all_patients()[:5]
    for patient in patients:
        patient.doctor_id = 1
        db.session.commit()

if __name__ == "__main__":
    test_db()
