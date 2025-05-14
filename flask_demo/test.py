from app import create_app
import json


def test_db():
    app = create_app()
    with app.app_context():
        # initPatients()
        # initCases()
        # initKnowledges()
        # initCEA()
        # handleDoctor_id()
        readData()
        


from app.services.patient_service import create_patient, get_all_patients
from app.services.case_service import create_case, get_all_cases
from app.services.knowledge_service import create_knowledge, get_all_knowledges
from app.services.cea_service import create_cea
from app import db


# 写入patient数据
def initPatients():
    file_path = "./app/assets/patients.json"
    with open(file_path, "r", encoding="utf-8") as file:
        patients_data = json.load(file)  # 加载 JSON 数据
        for patient in patients_data:
            create_patient(
                name=patient["name"],
                gender=patient["gender"],
                age=patient["age"],
                contact=patient["contact"],
                address=patient["address"],
            )


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
