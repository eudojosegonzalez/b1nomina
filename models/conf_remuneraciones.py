'''
Modelo que define a la tabla de Datos de configuraciones de remuneraciones
Created 2024-05
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, ForeignKey,TEXT, BOOLEAN,INTEGER, NUMERIC

# Definicion de la tabla de Sociedades
class ConfRemuneraciones(Base):
    '''
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `sociedad_id` bigint(20) NOT NULL,
    `sueldo_minimo` float (18,4) not null default '0',
    `gratificacion_minimo` float (5,2) not null default '0' comment 'Porcentaje de gratificacion mínimo',
    `tope_gratificacion` float (5,2) not null default '0' comment 'Porcentaje de gratificacion maximo',
    `dias_vacaciones` integer not null default '1',
    `horas_legales` integer not null default '8',
    `retencion_honorarios` float (5,2) not null default '0' comment 'Porcentaje de retención de honorarios',
    `created` datetime NOT NULL COMMENT 'fecha en que fue creado el registro',
    `updated` datetime NOT NULL COMMENT 'fecha en que fue actualizado el registro',
    `creator_user` bigint(20) NOT NULL COMMENT 'usuario que creó el parametro',
    `updater_user` bigint(20) NOT NULL COMMENT 'usuario que actualizó el parametro',
    PRIMARY KEY (`id`),
    CONSTRAINT `FK_Sociedad_ConfRemuneraciones` FOREIGN KEY (`sociedad_id`) 
    REFERENCES `Sociedad` (`id`) ON UPDATE CASCADE
    '''
    __tablename__="ConfRemuneraciones"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    sociedad_id = Column (BIGINT, ForeignKey("Sociedad.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)        
    sueldo_minimo= Column(NUMERIC(18,4), nullable=False)
    gratificacion_minimo= Column(NUMERIC(5,2), nullable=False)
    tope_gratificacion= Column(NUMERIC(5,2), nullable=False)
    dias_vacaciones= Column(INTEGER, nullable=False)
    horas_legales= Column(INTEGER, nullable=False)
    retencion_honorarios= Column(NUMERIC(5,2), nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,

    # metodo que permite devolver un diccionario de los datos del registro
    def to_dict(self):
        result={
            "id":self.id,
            "sociedad_id":self.id,
            "sueldo_minimo":self.sueldo_minimo,
            "gratificacion_minimo":self.gratificacion_minimo,
            "tope_gratificacion":self.tope_gratificacion,
            "dias_vacaciones":self.dias_vacaciones,
            "horas_legales":self.horas_legales,
            "retencion_honorarios":self.retencion_honorarios,
            "created": self.created,
            "updated ":self.updated,
            "creator_user": self.creator_user,
            "updater_user": self.updater_user
        }

        return (result)