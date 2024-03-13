from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

host = "localhost"
username = "root"
password = "Ruvae200"
database = "b1"

engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}/{database}",
    echo=True,   
    pool_size=10,      # Define el tamaño inicial del grupo (10 conexiones)
    max_overflow=20,   # Máximo número de conexiones adicionales (20)                         
)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#instanciamos la Base de datos
Base = declarative_base()


