from app.models.patient import Patient
from app.models.hospital_record import HospitalRecord
from app.models.physical_sign import PhysicalSign
from app.models.examination import Examination
from app.models.medical_test import MedicalTest
from app.models.diagnosis import Diagnosis
from app.models.operation import Operation
from app.models.medication import Medication


def get_patient_by_id(patient_id):
    return Patient.query.get(patient_id)

def get_hosrecords_by_patient_id(patient_id):
    return HospitalRecord.query.filter_by(patient_id=patient_id).all()

def get_hosrecords_by_order_id(order_id):
    return HospitalRecord.query.filter_by(order=order_id).first()

def get_physical_signs(patient_id, order):
    return PhysicalSign.query.filter_by(patient_id=patient_id, hospital_order=order).all()

def get_examinations(patient_id, order):
    return Examination.query.filter_by(patient_id=patient_id, order=order).all()

def get_medical_tests(patient_id, order):
    return MedicalTest.query.filter_by(patient_id=patient_id, order=order).all()

def get_diagnoses(patient_id, order):
    return Diagnosis.query.filter_by(patient_id=patient_id, hospital_order=order).all()

def get_operations(patient_id, order):
    return Operation.query.filter_by(patient_id=patient_id, hospital_order=order).all()

def get_medications(patient_id, order):
    return Medication.query.filter_by(patient_id=patient_id, hospital_order=order).all()

