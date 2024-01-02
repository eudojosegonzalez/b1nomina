import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# se coloca con ../ para que la cree en la raiz del directorio
sqlite_file_name="../database.sqlite"
# lee el directorio actual
base_dir=os.path.dirname(os.path.realpath(__file__))
# se crea una direccion dinámicamente a la base de datos
database_url=f"sqlite:///{os.path.join(base_dir,sqlite_file_name)}"

#enlazamos el motor de la BD a un instancia
engine= create_engine(database_url,echo=True)

# enlazamos una sesion al motor de la BD
Session=sessionmaker(bind=engine)

#instanciamos la Base de datos
Base = declarative_base()


