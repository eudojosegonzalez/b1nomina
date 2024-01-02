# Este archivo contiene las funciones básicas para el crud del Usuario
# Estructura del Modelo usuario
'''
    id : int = Field (ge=1, lt= 2000)
    rut = Column(VARCHAR(100), nullable=False) #VARCHAR(100) NOT NULL,
    rut_provisorio  = Column(VARCHAR(100), nullable=True) #VARCHAR(100) NULL,
    nombres = Column (VARCHAR(100), nullable=False) #VARCHAR(100) NOT NULL,
    apellido_paterno  = Column (VARCHAR(100), nullable=False) #paterno VARCHAR(100) NOT NULL,
    apellido_materno = Column (VARCHAR(100),nullable=True )  #VARCHAR(100) NULL,
    fecha_nacimiento = Column(DATE, nullable=False) #DATE NOT NULL,
    sexo_id = Column(BIGINT, nullable=False) #BIGINT NOT NULL,
    estado_civil_id = Column(BIGINT, nullable=False) #BIGINT NOT NULL,    
    nacionalidad_id = Column(BIGINT, nullable=False) #BIGINT NOT NULL, 
    username = Column(VARCHAR(250), nullable=False) #varchar(250) NOT NULL,    
    password = Column(VARCHAR(250), nullable=False) #NOT NULL,  
    activo = Column(Boolean, nullable=False) #boolean NOT NULL comment 'campo para activar o no al usuario 0 Inactivo 1 Activo',           
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL, 
'''


from models.user import Usuario as UsuarioModel
from schemas.user import User

from datetime import date, datetime

# importamos la utilidad para generar el hash del password
from utils.hasher import hash_password,verify_password


# esto representa los metodos implementados en la tabla
class userController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db

    # metodo para consultar todos los usuarios
    def get_users(self):
        result= self.db.query(UsuarioModel).all()
        return result
    
    # metodo para consultar por Id
    def get_user(self, id):
        result= self.db.query(UsuarioModel).filter(UsuarioModel.id==id).first()
        return result   
    
    #metodo para insertar datos    
    def create_user(self, usuario:User):
        new_user=UsuarioModel(**user.dict())
        self.db.add(new_user)
        self.db.commit()
        return
    
    #metodo para actualizar datos
    def update_user (self, userId: int, data : User ):
        user = self.db.query(UsuarioModel).filter(UsuarioModel.id==id).first()
        user.rut=data.rut
        user.rut_provisorio=data.rut_provisorio,
        user.apellido_materno=data.apellido_materno
        user.nombres=data.nombres
        user.fecha_nacimiento=data.fecha_nacimiento
        user.sexo_id=data.sexo_id
        user.estado_civil_id=data.estado_civil_id
        user.nacionalidad_id=data.nacionalidad_id
        user.username=data.username
        user.password=hash_password(data.password)
        user.activo=True
        user.created=datetime.datetime.now()
        user.updated=datetime.datetime.now()
        creator_user=userId
        updater_user=userId

        self.db.commit()
        return
    
    # metodo para eliminar un usuario
    # NO USADO
    def delete_user (self, id : int):
        #forma 1
        # result= self.db.query(UsuarioModel).filter(UsuarioModel.id==id).first()
        # self.db.delete(result)

        #forma 2
        result= self.db.query(UsuarioModel).filter(UsuarioModel.id==id).delete()
        self.db.commit()
        return
        


    