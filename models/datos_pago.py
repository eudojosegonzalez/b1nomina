'''
Modelo que define a la tabla de Datos de pago del Empleado
Created 2024-02
'''
from config.database import Base
from sqlalchemy import Column, BIGINT, DateTime, ForeignKey,INTEGER, VARCHAR

# Definicion de la tabla de Datos laborales
class DatosPago(Base):
    '''
	`id` bigint NOT NULL AUTO_INCREMENT,
	`user_id` bigint NOT NULL,
	`medio` int NOT NULL comment '1 Transfernecia, 2 Cheque, 3 contado',
	`banco_id` bigint NULL,    
	`tipo_cuenta` int NULL comment '1 Corriente 2 Ahorro', 
    `numero_cuenta` varchar(100) DEFAULT NULL ,      
	`created` datetime NOT NULL,
	`updated` datetime NOT NULL,
	`creator_user` bigint(20) NOT NULL,
	`updater_user` bigint(20) NOT NULL, 
	primary key(`id`),    
    constraint `FK_Usuario_DatosPago` foreign key (`user_id`) references `Usuario` (`id`) 
    on update cascade on delete restrict
    '''
    __tablename__="DatosPago"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column (BIGINT, ForeignKey("Usuario.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)            
    medio = Column(INTEGER, nullable=False)
    banco_id = Column(BIGINT,  nullable=True)
    tipo_cuenta = Column(INTEGER, nullable=True)
    numero_cuenta = Column(VARCHAR(100), nullable=True)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
