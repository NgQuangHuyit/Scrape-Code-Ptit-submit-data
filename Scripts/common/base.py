from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session

engine = create_engine('mssql+pyodbc://sa:Password123@localhost:1433/CodePtit?driver=ODBC+Driver+18+for+SQL+Server'
                       '&TrustServerCertificate=yes')
session = Session(engine)
Base = declarative_base()
