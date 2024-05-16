'''
Modelo que define a la tabla AFC de Sociedades
Created 2024-05
'''
from config.database import Base
from sqlalchemy import Column,   BIGINT,  DateTime,  ForeignKey, NUMERIC

# Definicion de una tabla
class SociedadesAFC(Base):
    __tablename__="SociedadesAFC"
    '''
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `sociedad_id` bigint(20) NOT NULL,
    `afc_empresa` numeric(5,2) NOT NULL,
    `afc_empleado` numeric(5,2) NOT NULL, 
    `afc_plazo_fijo` numeric(5,2) NOT NULL,  
    `afc_antiguedad` numeric(5,2) NOT NULL,  
    `tope_seguro_afc` numeric(5,2) NOT NULL,  
    `created` datetime NOT NULL COMMENT 'fecha en que fue creado el registro',
    `updated` datetime NOT NULL COMMENT 'fecha en que fue actualizado el registro',
    `creator_user` bigint(20) NOT NULL COMMENT 'usuario que creó el parametro',
    `updater_user` bigint(20) NOT NULL COMMENT 'usuario que actualizó el parametro',
    PRIMARY KEY (`id`),
    CONSTRAINT `FK_Sociedad_SociedadAFC` FOREIGN KEY (`sociedad_id`) REFERENCES `Sociedad` (`id`) ON UPDATE CASCADE
    '''
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    sociedad_id = Column(BIGINT,  ForeignKey("Sociedad.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)    
    afc_empresa = Column (NUMERIC(5,2) ,nullable=False)
    afc_empleado = Column (NUMERIC(5,2) ,nullable=False)
    afc_plazo_fijo = Column (NUMERIC(5,2) ,nullable=False) 
    afc_antiguedad = Column (NUMERIC(5,2), nullable=False)
    tope_seguro_afc= Column (NUMERIC(5,2) ,nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,  

    
    # metodo para convertir el registro en diccionario
    def to_dict(self):
        result={
            "id"  : self.id,
            "sociedad_id"  : self.sociedad_id,
            "afc_empresa"  : self.afc_empresa,
            "afc_empleado"  : self.afc_empleado,
            "afc_plazo_fijo"  : self.afc_plazo_fijo,
            "afc_antiguedad"  : self.afc_antiguedad,
            "tope_seguro_afc"  : self.tope_seguro_afc,
            "created"  : self.created,
            "updated"  : self.updated,
            "creator_user"  : self.creator_user,
            "updater_user" : self.updater_user            
        }
        return (result)