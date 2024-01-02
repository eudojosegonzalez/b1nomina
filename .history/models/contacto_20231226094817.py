from config.database import Base
from sqlalchemy import Column, Integer, String, Float, VARCHAR, BIGINT, DATE, DateTime, Boolean, ForeignKey

# Definicion de la tabla de Contacto de usuarios
class Contacto(Base):
    '''
    `id` BIGINT AUTO_INCREMENT NOT NULL,
    `user_id` BIGINT NULL,    
    `email` varchar(250) NULL,       
    `fijo` varchar(20) NULL,   
    `movil` varchar(20) NULL,       
    PRIMARY KEY (`id`),    
    '''
    __tablename__="Contacto"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    user_id = Column(BIGINT,  ForeignKey("Usuario.id", ondelete="RESTRICT", onupdate="CASCADE"))
    email = Column(VARCHAR(250), nullable=True)
    fijo = Column(VARCHAR(20), nullable=True)
    movil = Column(VARCHAR(20), nullable=True)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL, 

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id ,
            "email": self.email,
            "fijo": self.fijo,
            "movil": self.movil ,
            "created": self.created ,
            "updated": self.updated,
            "creator_user": self.creator_user,
            "updater_user": self.updater_user 
        }    



