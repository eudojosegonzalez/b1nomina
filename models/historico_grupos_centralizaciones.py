'''
Modelo que define a la tabla de Datos Historico de Grupos de Centralizacion
Created 2023-12
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, TEXT, INTEGER, NUMERIC

# Definicion de la tabla de Sociedades
class HistoricoGrupoCentralizaciones(Base):
    '''
	`id` bigint auto_increment not null,
	`grupo_centralizacion_id` bigint  not null,        
	`sociedad_id` bigint  not null,        
	`es_honorario` bool not null default '0',
	`nombre` varchar(200) NOT NULL,
	`monto_max_prestamo` numeric(18,4) NULL,
	`cuotas_max_prestamo` int null,
	`porcentaje_tope_cuota_prestamo` numeric(18,4) NULL,
	`monto_max_anticipo` numeric(18,4) NULL,
	`porcentaje_maximo_anticipo` numeric(18,4) NULL,
	`calcular_porcentaje_segun` varchar(10) NULL,
	`factura_mas_pago` integer DEFAULT 0 NOT NULL,
	`cuenta_factura_proveedor` varchar(20) NULL,
	`cuenta_pago_factura` varchar(20) NULL,
	`cuenta_remunera_deb` varchar(20) NULL,
	`cuenta_AFP_deb` varchar(20) NULL,
	`cuenta_salud_deb` varchar(20) NULL,
	`cuenta_gratificacion_deb` varchar(20)  NULL,
	`cuenta_horas_ext_deb` varchar(20) NULL,
	`cuenta_seg_AFC_deb` varchar(20) NULL,
	`cuenta_mov_deb` varchar(20) NULL,
	`cuenta_col_deb` varchar(20) NULL,
	`cuenta_otra_asig_deb` varchar(20) NULL,
	`cuenta_SIS_deb` varchar(20) NULL,
	`cuenta_mut_deb` varchar(20) NULL,
	`cuenta_impuesto_unico_deb` varchar(20) NULL,
	`cuenta_asignacion_fami_deb` varchar(20) NULL,
	`cuenta_Afc_empresa_cred` varchar(20) NULL,
	`cuenta_asignacion_familiar_cred` varchar(20) NULL,
	`cuenta_impuesto_unico_cred` varchar(20) NULL,
	`cuenta_sueldo_pagar_cred` varchar(20) NULL,
	`created` datetime NOT NULL,
	`updated` datetime NOT NULL,
	`creator_user` bigint(20) NOT NULL,
	`updater_user` bigint(20) NOT NULL,  
	`fecha_registro` datetime NOT NULL,
	`observaciones` text DEFAULT NULL,    
	primary key (id)
    '''
    __tablename__="HistoricoGrupoCentralizaciones"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    grupo_centralizacion_id= Column(BIGINT, nullable=False)
    sociedad_id = Column (BIGINT, nullable=False)      
    es_honorario = Column(INTEGER, nullable=False)
    nombre = Column(VARCHAR(200), nullable=False)
    monto_max_prestamo=Column(NUMERIC(18,4), nullable=True) 
    cuotas_max_prestamo=Column(INTEGER, nullable=True)
    porcentaje_tope_cuota_prestamo=Column(INTEGER, nullable=True)
    monto_max_anticipo=Column(INTEGER, nullable=True)
    porcentaje_maximo_anticipo=Column(INTEGER, nullable=True)
    calcular_porcentaje_segun=Column(VARCHAR(10), nullable=True)
    factura_mas_pago=Column(INTEGER, nullable=True)
    cuenta_factura_proveedor=Column(VARCHAR(10), nullable=True)
    cuenta_pago_factura=Column(VARCHAR(10), nullable=True)
    cuenta_remunera_deb=Column(VARCHAR(10), nullable=True)
    cuenta_AFP_deb=Column(VARCHAR(10), nullable=True)
    cuenta_salud_deb=Column(VARCHAR(10), nullable=True)
    cuenta_gratificacion_deb=Column(VARCHAR(10), nullable=True)
    cuenta_horas_ext_deb=Column(VARCHAR(10), nullable=True)
    cuenta_seg_AFC_deb=Column(VARCHAR(10), nullable=True)
    cuenta_mov_deb=Column(VARCHAR(10), nullable=True)
    cuenta_col_deb=Column(VARCHAR(10), nullable=True)
    cuenta_otra_asig_deb=Column(VARCHAR(10), nullable=True)
    cuenta_SIS_deb=Column(VARCHAR(10), nullable=True)
    cuenta_mut_deb=Column(VARCHAR(10), nullable=True)
    cuenta_impuesto_unico_deb=Column(VARCHAR(10), nullable=True)
    cuenta_asignacion_fami_deb=Column(VARCHAR(10), nullable=True)
    cuenta_Afc_empresa_cred=Column(VARCHAR(10), nullable=True)
    cuenta_asignacion_familiar_cred=Column(VARCHAR(10), nullable=True)
    cuenta_impuesto_unico_cred=Column(VARCHAR(10), nullable=True)
    cuenta_sueldo_pagar_cred=Column(VARCHAR(10), nullable=True)  
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
    fecha_registro = Column (DateTime, nullable=False) #datetime NOT NULL,      
    observaciones = Column(TEXT, nullable= True)     
