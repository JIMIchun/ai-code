import sqlite3
from datetime import datetime

def create_database():
    conn = sqlite3.connect('medical_database.db')
    cursor = conn.cursor()

    # 创建患者基本信息表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        gender TEXT NOT NULL,
        age INTEGER NOT NULL,
        contact TEXT,
        address TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # 创建患者病例信息表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS medical_records (
        record_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        diagnosis_date DATE NOT NULL,
        symptoms TEXT,
        treatment_plan TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
    )
    ''')

    # 创建直肠癌病理信息表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pathology_reports (
        report_id INTEGER PRIMARY KEY AUTOINCREMENT,
        record_id INTEGER NOT NULL,
        tumor_size DECIMAL(5, 2),
        differentiation TEXT,
        lymph_nodes TEXT,
        metastasis TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (record_id) REFERENCES medical_records(record_id)
    )
    ''')

    conn.commit()
    conn.close()
    print("数据库和表结构创建成功！")


if __name__ == '__main__':
    create_database()
