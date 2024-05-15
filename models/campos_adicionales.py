'''
Modelo que define a la tabla de Datos de Campsu Adicionales Ususarios
Created 2024-01
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, ForeignKey,INTEGER

# Definicion de la tabla de Cargos
class CamposAdicionales(Base):
    '''
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `sociedad_id` bigint(20) NOT NULL,
    `camuser1` varchar(200) DEFAULT NULL,
    `activo1` bool DEFAULT NULL,
    `camuser2` varchar(200) DEFAULT NULL,
    `activo2`  bool DEFAULT NULL,
    `camuser3` varchar(200) DEFAULT NULL,
    `activo3`  bool DEFAULT NULL,
    `camuser4` varchar(200) DEFAULT NULL,
    `activo4`  bool DEFAULT NULL,
    `camuser5` varchar(200) DEFAULT NULL,
    `activo5`  bool DEFAULT NULL,
    `created` datetime NOT NULL,
    `updated` datetime NOT NULL,
    `creator_user` bigint(20) NOT NULL,
    `updater_user` bigint(20) NOT NULL,
    PRIMARY KEY (`id`),
    CONSTRAINT `FK_Sociedad_CamposAdicionales` FOREIGN KEY (`sociedad_id`) REFERENCES `Sociedad` (`id`) ON UPDATE CASCADE
    '''
    __tablename__="CamposAdicionales"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    sociedad_id = Column (BIGINT, ForeignKey("Sociedad.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False) 
    camuser1 = Column (VARCHAR(200), nullable=True)
    activo1=Column(INTEGER,nullable=False)
    camuser2 = Column (VARCHAR(200), nullable=True)    
    activo2=Column(INTEGER,nullable=False)    
    camuser3 = Column (VARCHAR(200), nullable=True)
    activo3=Column(INTEGER,nullable=False)    
    camuser4 = Column (VARCHAR(200), nullable=True) 
    activo4=Column(INTEGER,nullable=False)       
    camuser5 = Column (VARCHAR(200), nullable=True)
    activo5=Column(INTEGER,nullable=False)    
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,


    def to_dict(self):
        result = {
            "id": self.id,
            "sociedad_id":self.sociedad_id,
            "camuser1":self.camuser1,
            "activo1":self.activo1,
            "camuser2":self.camuser2,
            "activo2":self.activo2,
            "camuser3":self.camuser3,
            "activo3":self.activo3,
            "camuser4":self.camuser4,
            "activo4":self.activo4,
            "camuser5":self.camuser5,
            "activo5":self.activo5,
            "created": self.created.strftime("%Y-%m-%d %H:%M:%S"),  
            "updated":self.updated.strftime("%Y-%m-%d %H:%M:%S"),  
            "creator_user":self.creator_user,
            "updater_user":self.updater_user
        }
        return (result)