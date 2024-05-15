'''
Modelo que define a la tabla de Datos de los Bancos del Sistema
Created 2024-03
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, ForeignKey, INTEGER

# Definicion de la tabla de Sociedades
class BancariosSociedad(Base):
    '''
 	`id` bigint(20) NOT NULL AUTO_INCREMENT,
	`sociedad_id` bigint(20) NOT NULL,
	`banco_id` bigint(20) NOT NULL,
	`numero_cuenta` varchar(100) not NULL,
	`codigo_convenio` varchar(150)  NULL,
	`giro_empresa` varchar(150)  NULL,
	`razon_social` varchar(150)  NULL,   
	`ocultar_email` boolean null,    
	`created` datetime NOT NULL,
	`updated` datetime NOT NULL,
	`creator_user` bigint(20) NOT NULL,
	`updater_user` bigint(20) NOT NULL,
	PRIMARY KEY (`id`),
	CONSTRAINT `FK_Bancos_BancariosSociedad` FOREIGN KEY (`banco_id`) REFERENCES `Bancos` (`id`) 
    ON UPDATE CASCADE on delete restrict
    '''
    __tablename__="BancariosSociedad"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    sociedad_id = Column (BIGINT, ForeignKey("Sociedad.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)
    banco_id = Column (BIGINT, ForeignKey("Bancos.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)
    numero_cuenta = Column(VARCHAR(100), nullable=False)
    codigo_convenio = Column(VARCHAR(150), nullable=True)
    giro_empresa = Column(VARCHAR(150), nullable=True)
    razon_social = Column(VARCHAR(150), nullable=True)  
    ocultar_email = Column(INTEGER, nullable=True)      
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,


    