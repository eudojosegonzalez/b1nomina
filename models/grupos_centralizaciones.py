'''
Modelo que define a la tabla de Datos de Grupos de Centralizacion
Created 2023-12
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, ForeignKey, INTEGER, NUMERIC

# Definicion de la tabla de Grupos de Centralización
class GrupoCentralizaciones(Base):
    '''
	`id` bigint auto_increment not null,
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
	primary key (id),
    constraint `FK_Sociedad_GrupoCentralizaciones` foreign key (`sociedad_id`) references `Sociedad` (`id`)
    on update cascade on delete restrict
    '''
    __tablename__="GrupoCentralizaciones"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    sociedad_id = Column (BIGINT, ForeignKey("Sociedad.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)      
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

    # funcion para converir en un diccionario 
    # 2024-04
    def to_dict(self):
        {
            "id":self.id,    
            "sociedad_id": self.sociedad_id,
            "es_honorario": self.es_honorario,
            "nombre":self.nombre,
            "monto_max_prestamo" : self.monto_max_prestamo,
            "cuotas_max_prestamo" : self.monto_max_prestamo,
            "porcentaje_tope_cuota_prestamo" : self.porcentaje_tope_cuota_prestamo,
            "monto_max_anticipo" : self.monto_max_anticipo,
            "porcentaje_maximo_anticipo" : self.porcentaje_maximo_anticipo,
            "calcular_porcentaje_segun" : self.calcular_porcentaje_segun,
            "factura_mas_pago" : self.factura_mas_pago,
            "cuenta_factura_proveedor"  : self.cuenta_factura_proveedor,
            "cuenta_pago_factura"  : self.cuenta_pago_factura,
            "cuenta_remunera_deb"   : self.cuenta_remunera_deb,
            "cuenta_AFP_deb"   : self.cuenta_AFP_deb,
            "cuenta_salud_deb"   : self.cuenta_salud_deb,
            "cuenta_gratificacion_deb"   : self.cuenta_gratificacion_deb,
            "cuenta_horas_ext_deb"   : self.cuenta_horas_ext_deb,
            "cuenta_seg_AFC_deb"   : self.cuenta_seg_AFC_deb,
            "cuenta_mov_deb"   : self.cuenta_mov_deb,
            "cuenta_col_deb"   : self.cuenta_col_deb,
            "cuenta_otra_asig_deb"   : self.cuenta_otra_asig_deb,
            "cuenta_SIS_deb"   : self.cuenta_SIS_deb,
            "cuenta_mut_deb"   : self.cuenta_mut_deb,
            "cuenta_impuesto_unico_deb"   : self.cuenta_impuesto_unico_deb,
            "cuenta_asignacion_fami_deb"   : self.cuenta_asignacion_fami_deb,
            "cuenta_Afc_empresa_cred"   :self.cuenta_Afc_empresa_cred,
            "cuenta_asignacion_familiar_cred"   : self.cuenta_asignacion_familiar_cred,
            "cuenta_impuesto_unico_cred"   : self.cuenta_impuesto_unico_cred,
            "cuenta_sueldo_pagar_cred"   : self.cuenta_sueldo_pagar_cred,
            "created": self.created,
            "updated":self.updated,
            "creator_user":self.creator_user,
            "updater_user":self.updater_user               
        }
        