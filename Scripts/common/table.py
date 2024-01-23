from common.base import Base
from sqlalchemy import Column, DATE, TIME, Float, INTEGER, VARCHAR, NVARCHAR


class Submit(Base):
    __tablename__ = 'submit_records'
    submit_id = Column(INTEGER, primary_key=True)
    date = Column(DATE, nullable=False)
    time = Column(TIME, nullable=False)
    student_id = Column(VARCHAR(30), nullable=False)
    student_name = Column(NVARCHAR(35), nullable=False)
    exercise = Column(NVARCHAR(70), nullable=False)
    result = Column(VARCHAR(5), nullable=False)
    run_time = Column(Float(5), nullable=True)
    memory_in_kb = Column(INTEGER, nullable=True)
    language = Column(VARCHAR(15), nullable=False)