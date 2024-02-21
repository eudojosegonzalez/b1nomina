'''
Modelo que define a la tabla de Historico de Cuentas Contables
Created 2024-02
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, BOOLEAN, ForeignKey,TEXT

# Definicion de la tabla de Contacto de usuarios
class HistoricoCuentasContables(Base):
    '''
    `id` bigint(20) NOT NULL,
    `cuenta_contable_id` bigint(20) NOT NULL,  
    `sociedad_id` bigint(20) NOT NULL,
    `acct_code` varchar(20) NOT NULL,
    `acct_name` varchar(100) NOT NULL,
    `finance` char(1) NOT NULL,
    `created` datetime NOT NULL,
    `updated` datetime NOT NULL,
    `creator_user` bigint(20) NOT NULL,
    `updater_user` bigint(20) NOT NULL, 
    `fecha_registro` bigint(20) NOT NULL,
    `observaciones` text DEFAULT NULL,  
    '''
    __tablename__="HistoricoCuentasContables"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    cuenta_contable_id = Column(BIGINT, nullable=False)
    sociedad_id = Column (BIGINT,nullable=False)
    acct_code = Column(VARCHAR(20),nullable=False)
    acct_name = Column(VARCHAR(100),nullable=False)
    finance = Column(VARCHAR(1),nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
    fecha_registro = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,   
    observaciones = Column(TEXT, nullable= True)     

