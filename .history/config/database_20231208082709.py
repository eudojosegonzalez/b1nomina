from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

host = "localhost"
username = "root"
password = "Ruvaeq200"
database = "b1"

engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}/{database}")
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#instanciamos la Base de datos
Base = declarative_base()


