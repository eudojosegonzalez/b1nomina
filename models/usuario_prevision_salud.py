'''
Modelo que define a la tabla Usuarios Prevision Salud
Created 2024-03
'''
from config.database import Base
from sqlalchemy import Column,   BIGINT,  DateTime,  ForeignKey,NUMERIC, INTEGER

# Definicion de una tabla
class UsuariosPrevisionSalud(Base):
	'''
	`id` bigint(20) NOT NULL AUTO_INCREMENT,
	`prevision_salud_id` bigint  not null,
	`user_id` bigint  not null,
	`pactado` numeric(18,4)  not null default 0,  
	`tipo_contrato` integer not null ,
	`created` datetime NOT NULL COMMENT 'fecha en que fue creado el UsuariosPrevisionSalud',
	`updated` datetime NOT NULL COMMENT 'fecha en que fue actualizado el UsuariosPrevisionSalud',
	`creator_user` bigint(20) NOT NULL COMMENT 'usuario que creó el UsuariosPrevisionSalud',
	`updater_user` bigint(20) NOT NULL COMMENT 'usuario que actualizó el UsuariosPrevisionSalud',
	PRIMARY KEY (`id`),
	constraint `FK_USER_UsuariosPrevisionSalud` foreign key (`user_id`) references `Usuario` (`id`)
	'''
	__tablename__="UsuariosPrevisionSalud"
	id = Column(BIGINT, primary_key=True, autoincrement=True)
	prevision_salud_id = Column(BIGINT,  ForeignKey("PrevisionSalud.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)
	user_id = Column(BIGINT,  ForeignKey("Usuario.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)    
	pactado= Column(NUMERIC (18,4),nullable=False)   
	tipo_contrato= Column(INTEGER,nullable=False)   
	created = Column (DateTime, nullable=False) #datetime NOT NULL,    
	updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
	creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
	updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,  

