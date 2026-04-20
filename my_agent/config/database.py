from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import sqlite3
from pathlib import Path
import pandas as pd

PATH_CSV='/home/rondi/dev/python_projects/PROJETO-4---SQL_AGENT/my_agent/config/ultimate_student_productivity_dataset_5000.csv'

df = pd.read_csv(PATH_CSV)
# df.info()

ROOT_DIR = Path(__file__).parent
DB_NAME = 'db.sqlite3'
DB_FILE = ROOT_DIR / DB_NAME
TABLE_NAME = 'customers'

connection = sqlite3.connect(DB_FILE)
cursor = connection.cursor()

# cursor.execute(f"""
# SELECT academic_level, AVG(exam_score)
# FROM customers
# GROUP BY academic_level
# ORDER BY AVG(exam_score) DESC;
# """)
# print(cursor.fetchall())

# cursor.execute(f"""
# SELECT 
#     CASE 
#         WHEN sleep_hours < 6 THEN 'Pouco sono'
#         ELSE 'Sono adequado'
#     END AS categoria_sono,
#     AVG(productivity_score)
# FROM customers
# GROUP BY categoria_sono;
# """)
# print(cursor.fetchall())

df.to_sql(TABLE_NAME, connection, if_exists='replace', index=False)

engine = create_engine(f'sqlite:///{DB_FILE}')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def run_db(dbquery: str):
    for db in get_db():
        result = db.execute(text(dbquery))
        return result.fetchall()