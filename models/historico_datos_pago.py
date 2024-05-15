'''
Modelo que define a la tabla de Historico Datos de Pago del Empleado
Created 2024-02
'''
from config.database import Base
from sqlalchemy import Column, BIGINT, DateTime, INTEGER, TEXT, VARCHAR

# Definicion de la tabla de Datos laborales
class HistoricoDatosPago(Base):
    '''
	`id` bigint NOT NULL AUTO_INCREMENT,
	`datos_pago_id` bigint NOT NULL,    
	`user_id` bigint NOT NULL,
	`medio` int NOT NULL comment '1 Transferencia, 2 Cheque, 3 Contado',
	`banco_id` bigint NULL,    
	`tipo_cuenta` int NULL comment '1 Corriente 2 Ahorro', 
    `numero_cuenta` varchar(100) DEFAULT NULL ,    
	`created` datetime NOT NULL,
	`updated` datetime NOT NULL,
	`creator_user` bigint(20) NOT NULL,
	`updater_user` bigint(20) NOT NULL, 
	`fecha_registro` datetime NOT NULL,
    `observaciones` text NOT NULL,    
	primary key(`id`)         
    '''
    __tablename__="HistoricoDatosPago"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    datos_pago_id =Column(BIGINT, nullable=False)
    user_id = Column (BIGINT, nullable=False)            
    medio = Column(INTEGER, nullable=False)
    banco_id = Column(BIGINT,  nullable=True)
    tipo_cuenta = Column(INTEGER, nullable=True)
    numero_cuenta = Column(VARCHAR(100), nullable=True)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
    fecha_registro = Column (DateTime, nullable=False) #datetime NOT NULL,      
    observaciones = Column(TEXT, nullable= True)   