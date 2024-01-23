from common.base import session
import pandas as pd
from common.base import session, engine
from common.table import Submit, Base

last_record_id = -1
objects = []

Base.metadata.create_all(engine)
def readLogFile():
    global last_record_id
    with open('Scripts/common/logfile.txt', 'r') as log:
        data = log.readlines()
        last_record_id = int(data[-1].strip())


def readCleanData():
    df = pd.read_csv('Data/TransformedData/clean_data.csv')
    global objects
    for index, row in df.iterrows():
        if row.submit_id == last_record_id:
            break
        else:
            #objects.append(Submit(submit_id=123124, date='2023-10-12', time='17:47:31', student_id='B21DCAT024', student_name='Hồ Phan Đức Anh', exercise='TÍNH TIỀN PHÒNG',result='AC', run_time=0.17, memory_in_kb=4444, language='java'))
            objects.append(Submit(submit_id=row.submit_id, date=row.date, 
                                  time=row.time, student_id=row.student_id, 
                                  student_name=row.student_name, 
                                  exercise=row.exercise,result=row.result, 
                                  run_time=(row.run_time if not pd.isna(row.run_time) else None), 
                                  memory_in_kb=(row.memory if not pd.isna(row.memory) else None), 
                                  language=row.language))


def insertData():
    if objects:
        aa = str(objects[0].submit_id)
        session.add_all(objects)
        session.commit()
        session.close()
        with open('Scripts/common/logfile.txt', '+a') as log:
            log.write(aa + '\n')


def main():
    print('Loading')
    readLogFile()
    readCleanData()
    insertData()
    print('Success')

if __name__ == '__main__':
    main()