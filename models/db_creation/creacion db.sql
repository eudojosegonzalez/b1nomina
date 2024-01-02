drop DATABASE if exists `b1` ;
CREATE DATABASE if not exists `b1` /*!40100 DEFAULT CHARACTER SET utf8 */;
use b1;

-- *********************************************************************************
-- Tablas de apoyo
-- *********************************************************************************-- --------------------------------------------------------------------------------
-- Prevision Social 
-- --------------------------------------------------------------------------------
-- AFP
CREATE TABLE `AFP` (
	`id`  bigint auto_increment not null,
	`codigo_previred` varchar(50) NULL,
	`nombre` varchar(100) NULL,
	`cotizacion` numeric(18,4) NULL,
	`cuenta_AFP` varchar(150)  NULL,
	`sis` numeric(18,4) NULL,
	`cuenta_sis_cred` varchar(20) NULL,
	`cuenta_ahorro_AFP_cuenta2` varchar(150) NULL,
	`codigo_direccion_trabajo` varchar(10),
    `created` DATETIME NOT NULL COMMENT 'fecha en que fue creado el parametro',
    `updated` DATETIME NOT NULL COMMENT 'fecha en que fue actualizado el parametro',
    `creator_user` BIGINT NOT NULL COMMENT 'usuario que creó el parametro',
    `updater_user` BIGINT NOT NULL COMMENT 'usuario que actualizó el parametro',    
	PRIMARY KEY (`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8 comment 'Tabla para almacenar las cuentas AFP';


INSERT INTO AFP VALUES(1 , '08' , 'Provida', 11.450 , '21050001', 1.540 , '21050001' , '21050001' , '6' , '1990-01-01' , '1990-01-01' , '1' , '1');
INSERT INTO AFP VALUES(2 , '03' , 'Cuprum', 11.440 , '21050001', 1.540 , '21050001' , '21050001' , '13' , '1990-01-01' , '1990-01-01' , '1' , '1');
INSERT INTO AFP VALUES(3 , '05' , 'Habitat', 11.270 , '21050001', 1.540 , '21050001' , '21050001' , '14' , '1990-01-01' , '1990-01-01' , '1' , '1');
INSERT INTO AFP VALUES(4 , '29' , 'Plan Vital          ', 11.160 , '21050001', 1.540 , '21050001' , '21050001' , '11' , '1990-01-01' , '1990-01-01' , '1' , '1');
INSERT INTO AFP VALUES(5 , '33' , 'Capital', 11.440 , '21050001', 1.540 , '21050001' , '21050001' , '31' , '1990-01-01' , '1990-01-01' , '1' , '1');
INSERT INTO AFP VALUES(6 , '34' , 'Modelo', 10.580 , '21050001', 1.540 , '21050001' , '21050001' , '103' , '1990-01-01' , '1990-01-01' , '1' , '1');
INSERT INTO AFP VALUES(7 , '00' , 'No está en AFP', 0.000 , '21050001', 1.540 , '21050001' , '21050001' , '100' , '1990-01-01' , '1990-01-01' , '1' , '1');
INSERT INTO AFP VALUES(8 , '35' , 'Uno', 10.680 , '21050001', 1.540 , '21050001' , '21050001' , '19' , '1990-01-01' , '1990-01-01' , '1' , '1');


-- APVInstituciones
CREATE TABLE APVInstituciones (
	id bigint NOT NULL,
	nombre varchar(30) not NULL,
	nombre_largo varchar(250) not NULL,
	cuenta_contable varchar(100)  NULL,
	codigo_externo varchar(50) NULL,
	 PRIMARY KEY (id)
);INSERT INTO APVInstituciones VALUES(5, 'Habitat', 'Habitat', '21050001', '005');
INSERT INTO APVInstituciones VALUES(1005, 'Capital', 'Capital', '21050001', '033');



-- HistoricoAFP
CREATE TABLE `HistoricoAFP` (
	`id`  bigint auto_increment not null,
	`codigo_previred` varchar(50) NULL,
	`nombre` varchar(100) NULL,
	`cotizacion` numeric(18,4) NULL,
	`cuenta_AFP` varchar(150)  NULL,
	`sis` numeric(18,4) NULL,
	`cuenta_sis_cred` varchar(20) NULL,
	`cuenta_ahorro_AFP_cuenta2` varchar(150) NULL,
	`codigo_direccion_trabajo` varchar(10),
    `created` DATETIME NOT NULL COMMENT 'fecha en que fue creado el AFP',
    `updated` DATETIME NOT NULL COMMENT 'fecha en que fue actualizado el AFP',
    `creator_user` BIGINT NOT NULL COMMENT 'usuario que creó el AFP',
    `updater_user` BIGINT NOT NULL COMMENT 'usuario que actualizó el AFP',   
    `fecha_registro` DATETIME NOT NULL COMMENT 'fecha en que fue creado el registro en el historico',    
	PRIMARY KEY (`id`,`fecha_registro`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8 comment 'Tabla para almacenar el historico de las cuentas AFP';



-- PrevisionSalud
CREATE TABLE `PrevisionSalud` (
	`id`  bigint auto_increment not null,
	`codigo_externo` varchar(50)  NULL,
	`nombre` varchar(100) NULL,
	`prevision_salud_cuenta` varchar(150) NULL,
	`codigo_direccion_trabajo` varchar(10) NULL,
    `created` DATETIME NOT NULL COMMENT 'fecha en que fue creado el AFP',
    `updated` DATETIME NOT NULL COMMENT 'fecha en que fue actualizado el AFP',
    `creator_user` BIGINT NOT NULL COMMENT 'usuario que creó el AFP',
    `updater_user` BIGINT NOT NULL COMMENT 'usuario que actualizó el AFP', 
	PRIMARY KEY (`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8 comment 'Tabla para almacenar los datos de prevision salud';


INSERT INTO PrevisionSalud VALUES(2 , '00' , 'Sin Isapre' , '21050002', NULL , '1990-01-01' , '1990-01-01' , '1' , '1');
INSERT INTO PrevisionSalud VALUES(3 , '01' , 'Banmédica' , '21050002' , '3' , '1990-01-01' , '1990-01-01' , '1' , '1');
INSERT INTO PrevisionSalud VALUES(4 , '02' , 'Consalud' , '21050002' , '9' , '1990-01-01' , '1990-01-01' , '1' , '1');
INSERT INTO PrevisionSalud VALUES(5 , '03' , 'Vida Tres' , '21050002' , '12' , '1990-01-01' , '1990-01-01' , '1' , '1');
INSERT INTO PrevisionSalud VALUES(6 , '04' , 'Colmena' , '21050002' , '4' , '1990-01-01' , '1990-01-01' , '1' , '1');
INSERT INTO PrevisionSalud VALUES(7 , '05' , 'Isapre Cruz Blanca S.A.' , '21050002' , '1' , '1990-01-01' , '1990-01-01' , '1' , '1');
INSERT INTO PrevisionSalud VALUES(8 , '07' , 'Fonasa' , '21050009' , '102' , '1990-01-01' , '1990-01-01' , '1' , '1');
INSERT INTO PrevisionSalud VALUES(9 , '09' , 'Chuquicamata' , '21050002' , '37' , '1990-01-01' , '1990-01-01' , '1' , '1');
INSERT INTO PrevisionSalud VALUES(10 , '000' , 'Ferrosalud' , '21050002', NULL , '1990-01-01' , '1990-01-01' , '1' , '1');
INSERT INTO PrevisionSalud VALUES(11 , '11' , 'Inst. de salud Fusat Ltda.' , '21050002' , '39' , '1990-01-01' , '1990-01-01' , '1' , '1');
INSERT INTO PrevisionSalud VALUES(12 , '12' , 'Isapre Bco. Estado' , '21050002' , '40' , '1990-01-01' , '1990-01-01' , '1' , '1');
INSERT INTO PrevisionSalud VALUES(13 , '10' , 'Nueva Masvida' , '21050002' , '43' , '1990-01-01' , '1990-01-01' , '1' , '1');
INSERT INTO PrevisionSalud VALUES(14 , '20' , 'Río Blanco' , '21050002' , '41' , '1990-01-01' , '1990-01-01' , '1' , '1');
INSERT INTO PrevisionSalud VALUES(15 , '21' , 'San Lorenzo isapre ltda.' , '21050002' , '42' , '1990-01-01' , '1990-01-01' , '1' , '1');
INSERT INTO PrevisionSalud VALUES(16 , '25' , 'Cruz del norte' , '21050002' , '38' , '1990-01-01' , '1990-01-01' , '1' , '1');

-- CajasCompesacion
CREATE TABLE IF NOT EXISTS `CajasCompesacion` (
    `id` BIGINT AUTO_INCREMENT NOT NULL,
    `nombre` VARCHAR(200) NOT NULL,
    `codigo_externo` VARCHAR(50) NOT NULL,
    `cuenta_contable` VARCHAR(50) NOT NULL,
    `codigo_direccion_trabajo` VARCHAR(10) NULL,    
    `created` DATETIME NOT NULL COMMENT 'fecha en que fue creado el parametro',
    `updated` DATETIME NOT NULL COMMENT 'fecha en que fue actualizado el parametro',
    `creator_user` BIGINT NOT NULL COMMENT 'usuario que creó el parametro',
    `updater_user` BIGINT NOT NULL COMMENT 'usuario que actualizó el parametro',
    PRIMARY KEY (`id`)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8 COMMENT 'Tabla para controlarlar las las cajas de compensacion';

INSERT INTO `CajasCompesacion` VALUES(1, 'Sin CCAF', '00', '21050003', '0', '1990-01-01', '1990-01-01', '1', '1');
INSERT INTO `CajasCompesacion` VALUES(2, 'Los Andes', '01', '21050003', '1', '1990-01-01', '1990-01-01', '1', '1');
INSERT INTO `CajasCompesacion` VALUES(3, 'La Araucana', '02', '21050003', '2', '1990-01-01', '1990-01-01', '1', '1');
INSERT INTO `CajasCompesacion` VALUES(4, 'Los Héroes', '03', '21050003', '3', '1990-01-01', '1990-01-01', '1', '1');
INSERT INTO `CajasCompesacion` VALUES(5, 'Gabriela Mistral', '05', '21050003', NULL, '1990-01-01', '1990-01-01', '1', '1');
INSERT INTO `CajasCompesacion` VALUES(6, '18 de Septiembre', '06', '21050003', '4', '1990-01-01', '1990-01-01', '1', '1');


-- Mutuales
create table if not exists `Mutuales` (
	`id` bigint auto_increment not null,
	`nombre` varchar(250) not null,	
	`codigo_externo` varchar(50) not null,	    
	`cuenta_contable` varchar(50) not null,	     
	`created` datetime NOT NULL comment 'fecha en que fue creado el parametro',    
	`updated`  datetime NOT NULL  comment 'fecha en que fue actualizado el parametro',   
    `creator_user` BIGINT NOT NULL  comment 'usuario que creó el parametro',     
    `updater_user` BIGINT NOT NULL  comment 'usuario que actualizó el parametro',     
    primary key (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment 'Tabla para controlarlar las empresas mutuales';

INSERT INTO Mutuales VALUES(7, 'Asociación Chilena de seguridad (ACHS) ','01',  '21050004', '1990-01-01', '1990-01-01', '1', '1');
INSERT INTO Mutuales VALUES(8, 'Mutual de seguridad CCHC', '21050004', '02', '1990-01-01', '1990-01-01', '1', '1');
INSERT INTO Mutuales VALUES(9,  'Instituto de seguridad del trabajo I.S.T ', '03','21050004', '1990-01-01', '1990-01-01', '1', '1');
INSERT INTO Mutuales VALUES(12,  'Sin Mutual - Empresa entrega aporte Accidentes del Trabajo al ISL','00', '21050004', '1990-01-01', '1990-01-01', '1', '1');


-- UnidadesPacto
create table if not exists `UnidadesPacto` (
	`id` bigint auto_increment not null,
	`descripcion` varchar(150) not null,    
	`estado` boolean not null comment '0 Inactivo 1 Activo',      
    primary key (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment 'Tabla para controlar las unidades de pacto de los eventos de nomina';

-- TramosImpuestoUnico
CREATE TABLE `TramosImpuestoUnico` (
	`id` int NOT NULL,
	`tramo` nvarchar(50)  NOT NULL,
	`desde` numeric(18,4) NOT NULL,
	`hasta` numeric(18,4) NOT NULL,
	`factor` numeric(18,4) NULL,
	`rebaja` numeric(18,4) NULL,
	`created` datetime NOT NULL,    
	`updated`  datetime NOT NULL,   
    `creator_user` BIGINT NOT NULL,     
    `updater_user` BIGINT NOT NULL,         
	PRIMARY KEY (`id`)
) ENGINE=INNODB DEFAULT CHARSET=UTF8 comment 'Tabla de TramosImpuestoUnico';

-- TramosAsignacionFamiliar
CREATE TABLE `TramosAsignacionFamiliar` (
	`id` bigint NOT NULL,
	`tramo` nvarchar(5) not NULL,
	`desde` numeric(18,4) NULL,
	`hasta` numeric(18,4) NULL,
	`valor_carga` numeric(18,4) NULL,
	`created` datetime NOT NULL,    
	`updated`  datetime NOT NULL,   
    `creator_user` BIGINT NOT NULL,     
    `updater_user` BIGINT NOT NULL,    
	 PRIMARY KEY (`id`)
) ENGINE=INNODB DEFAULT CHARSET=UTF8 comment 'Tabla de TramosImpuestoUnico';


-- InstitucionesAPV
CREATE TABLE `InstitucionesAPV` (
	`id` bigint auto_increment  NOT NULL,
	`nombre` varchar(30) not NULL,
	`nombre_largo` text  NULL,
	`cuenta_contable` varchar(100)  NULL,
	`codigo_externo` nvarchar(50)  NULL,
	`created` datetime NOT NULL,    
	`updated`  datetime NOT NULL,   
    `creator_user` BIGINT NOT NULL,     
    `updater_user` BIGINT NOT NULL,    
	PRIMARY KEY (`id`)
);
-- --------------------------------------------------------------------------------
-- Geograficas 
-- --------------------------------------------------------------------------------
-- Regiones
create table if not exists `Regiones`(
	`id` bigint auto_increment not null,
	`nombre` varchar(250) not null,
	`orden` int not null,        
    primary key (`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8 comment 'Tabla para almacenar la información geográfica de las Regiones';INSERT INTO `Regiones` VALUES(1, 'Tarapacá', 3);
INSERT INTO `Regiones` VALUES(2, 'Antofagasta', 4);
INSERT INTO `Regiones` VALUES(3, 'Atacama ', 5);
INSERT INTO `Regiones` VALUES(4, 'Coquimbo ', 6);
INSERT INTO `Regiones` VALUES(5, 'Valparaíso ', 7);
INSERT INTO `Regiones` VALUES(6, 'Lib. Gral. B. O''Higgins', 8);
INSERT INTO `Regiones` VALUES(7, 'Maule', 9);
INSERT INTO `Regiones` VALUES(8, 'Bio Bio', 10);
INSERT INTO `Regiones` VALUES(9, 'Araucanía', 11);
INSERT INTO `Regiones` VALUES(10, 'Los Lagos', 12);
INSERT INTO `Regiones` VALUES(11, 'Aysen', 13);
INSERT INTO `Regiones` VALUES(12, 'Magallanes', 14);
INSERT INTO `Regiones` VALUES(13, 'Metropolitana', 1);
INSERT INTO `Regiones` VALUES(14, 'Los Ríos', 16);
INSERT INTO `Regiones` VALUES(15, 'Región de Arica y Parinacota ', 2);

-- Comunas
create table if not exists `Comunas` (
	`id` bigint auto_increment not null,
	`nombre` varchar(150) not null,  
	`region_id` bigint  not null,    
    primary key (`id`),
    constraint `FK_Region_Comuna` foreign key (`region_id`) references `Regiones`(`id`)
    on update cascade on delete restrict
) ENGINE=InnoDB DEFAULT CHARSET=utf8  comment 'Tabla para almacenar la información geográfica de las Comunas';

INSERT INTO `Comunas` Values (1101, 'Iquique', 1);
INSERT INTO `Comunas` Values (1107, 'Alto Hospicio', 1);
INSERT INTO `Comunas` Values (1401, 'Pozo Almonte', 1);
INSERT INTO `Comunas` Values (1402, 'Camiña', 1);
INSERT INTO `Comunas` Values (1403, 'Colchane', 1);
INSERT INTO `Comunas` Values (1404, 'Huara', 1);
INSERT INTO `Comunas` Values (1405, 'Pica', 1);
INSERT INTO `Comunas` Values (2101, 'Antofagasta', 2);
INSERT INTO `Comunas` Values (2102, 'Mejillones', 2);
INSERT INTO `Comunas` Values (2103, 'Sierra Gorda', 2);
INSERT INTO `Comunas` Values (2104, 'Taltal', 2);
INSERT INTO `Comunas` Values (2201, 'Calama', 2);
INSERT INTO `Comunas` Values (2202, 'Ollagüe', 2);
INSERT INTO `Comunas` Values (2203, 'San Pedro de Atacama', 2);
INSERT INTO `Comunas` Values (2301, 'Tocopilla', 2);
INSERT INTO `Comunas` Values (2302, 'María Elena', 2);
INSERT INTO `Comunas` Values (3101, 'Copiapó', 3);
INSERT INTO `Comunas` Values (3102, 'Caldera', 3);
INSERT INTO `Comunas` Values (3103, 'Tierra Amarilla', 3);
INSERT INTO `Comunas` Values (3201, 'Chañaral', 3);
INSERT INTO `Comunas` Values (3202, 'Diego de Almagro', 3);
INSERT INTO `Comunas` Values (3301, 'Vallenar', 3);
INSERT INTO `Comunas` Values (3302, 'Alto del Carmen', 3);
INSERT INTO `Comunas` Values (3303, 'Freirina', 3);
INSERT INTO `Comunas` Values (3304, 'Huasco', 3);
INSERT INTO `Comunas` Values (4101, 'La Serena', 4);
INSERT INTO `Comunas` Values (4102, 'Coquimbo', 4);
INSERT INTO `Comunas` Values (4103, 'Andacollo', 4);
INSERT INTO `Comunas` Values (4104, 'La Higuera', 4);
INSERT INTO `Comunas` Values (4105, 'Paiguano', 4);
INSERT INTO `Comunas` Values (4106, 'Vicuña', 4);
INSERT INTO `Comunas` Values (4201, 'Illapel', 4);
INSERT INTO `Comunas` Values (4202, 'Canela', 4);
INSERT INTO `Comunas` Values (4203, 'Los Vilos', 4);
INSERT INTO `Comunas` Values (4204, 'Salamanca', 4);
INSERT INTO `Comunas` Values (4301, 'Ovalle', 4);
INSERT INTO `Comunas` Values (4302, 'Combarbalá', 4);
INSERT INTO `Comunas` Values (4303, 'Monte Patria', 4);
INSERT INTO `Comunas` Values (4304, 'Punitaqui', 4);
INSERT INTO `Comunas` Values (4305, 'Río Hurtado', 4);
INSERT INTO `Comunas` Values (5101, 'Valparaíso', 5);
INSERT INTO `Comunas` Values (5102, 'Casablanca', 5);
INSERT INTO `Comunas` Values (5103, 'Concón', 5);
INSERT INTO `Comunas` Values (5104, 'Juan Fernández', 5);
INSERT INTO `Comunas` Values (5105, 'Puchuncaví', 5);
INSERT INTO `Comunas` Values (5107, 'Quintero', 5);
INSERT INTO `Comunas` Values (5109, 'Viña del Mar', 5);
INSERT INTO `Comunas` Values (5201, 'Isla de Pascua', 5);
INSERT INTO `Comunas` Values (5301, 'Los Andes', 5);
INSERT INTO `Comunas` Values (5302, 'Calle Larga', 5);
INSERT INTO `Comunas` Values (5303, 'Rinconada', 5);
INSERT INTO `Comunas` Values (5304, 'San Esteban', 5);
INSERT INTO `Comunas` Values (5401, 'La Ligua', 5);
INSERT INTO `Comunas` Values (5402, 'Cabildo', 5);
INSERT INTO `Comunas` Values (5403, 'Papudo', 5);
INSERT INTO `Comunas` Values (5404, 'Petorca', 5);
INSERT INTO `Comunas` Values (5405, 'Zapallar', 5);
INSERT INTO `Comunas` Values (5501, 'Quillota', 5);
INSERT INTO `Comunas` Values (5502, 'Calera', 5);
INSERT INTO `Comunas` Values (5503, 'Hijuelas', 5);
INSERT INTO `Comunas` Values (5504, 'La Cruz', 5);
INSERT INTO `Comunas` Values (5506, 'Nogales', 5);
INSERT INTO `Comunas` Values (5601, 'San Antonio', 5);
INSERT INTO `Comunas` Values (5602, 'Algarrobo', 5);
INSERT INTO `Comunas` Values (5603, 'Cartagena', 5);
INSERT INTO `Comunas` Values (5604, 'El Quisco', 5);
INSERT INTO `Comunas` Values (5605, 'El Tabo', 5);
INSERT INTO `Comunas` Values (5606, 'Santo Domingo', 5);
INSERT INTO `Comunas` Values (5701, 'San Felipe', 5);
INSERT INTO `Comunas` Values (5702, 'Catemu', 5);
INSERT INTO `Comunas` Values (5703, 'Llaillay', 5);
INSERT INTO `Comunas` Values (5704, 'Panquehue', 5);
INSERT INTO `Comunas` Values (5705, 'Putaendo', 5);
INSERT INTO `Comunas` Values (5706, 'Santa María', 5);
INSERT INTO `Comunas` Values (5801, 'Quilpué', 5);
INSERT INTO `Comunas` Values (5802, 'Limache', 5);
INSERT INTO `Comunas` Values (5803, 'Olmué', 5);
INSERT INTO `Comunas` Values (5804, 'Villa Alemana', 5);
INSERT INTO `Comunas` Values (6101, 'Rancagua', 6);
INSERT INTO `Comunas` Values (6102, 'Codegua', 6);
INSERT INTO `Comunas` Values (6103, 'Coinco', 6);
INSERT INTO `Comunas` Values (6104, 'Coltauco', 6);
INSERT INTO `Comunas` Values (6105, 'Doñihue', 6);
INSERT INTO `Comunas` Values (6106, 'Graneros', 6);
INSERT INTO `Comunas` Values (6107, 'Las Cabras', 6);
INSERT INTO `Comunas` Values (6108, 'Machalí', 6);
INSERT INTO `Comunas` Values (6109, 'Malloa', 6);
INSERT INTO `Comunas` Values (6110, 'Mostazal', 6);
INSERT INTO `Comunas` Values (6111, 'Olivar', 6);
INSERT INTO `Comunas` Values (6112, 'Peumo', 6);
INSERT INTO `Comunas` Values (6113, 'Pichidegua', 6);
INSERT INTO `Comunas` Values (6114, 'Quinta de Tilcoco', 6);
INSERT INTO `Comunas` Values (6115, 'Rengo', 6);
INSERT INTO `Comunas` Values (6116, 'Requínoa', 6);
INSERT INTO `Comunas` Values (6117, 'San Vicente', 6);
INSERT INTO `Comunas` Values (6201, 'Pichilemu', 6);
INSERT INTO `Comunas` Values (6202, 'La Estrella', 6);
INSERT INTO `Comunas` Values (6203, 'Litueche', 6);
INSERT INTO `Comunas` Values (6204, 'Marchihue', 6);
INSERT INTO `Comunas` Values (6205, 'Navidad', 6);
INSERT INTO `Comunas` Values (6206, 'Paredones', 6);
INSERT INTO `Comunas` Values (6301, 'San Fernando', 6);
INSERT INTO `Comunas` Values (6302, 'Chépica', 6);
INSERT INTO `Comunas` Values (6303, 'Chimbarongo', 6);
INSERT INTO `Comunas` Values (6304, 'Lolol', 6);
INSERT INTO `Comunas` Values (6305, 'Nancagua', 6);
INSERT INTO `Comunas` Values (6306, 'Palmilla', 6);
INSERT INTO `Comunas` Values (6307, 'Peralillo', 6);
INSERT INTO `Comunas` Values (6308, 'Placilla', 6);
INSERT INTO `Comunas` Values (6309, 'Pumanque', 6);
INSERT INTO `Comunas` Values (6310, 'Santa Cruz', 6);
INSERT INTO `Comunas` Values (7101, 'Talca', 7);
INSERT INTO `Comunas` Values (7102, 'Constitución', 7);
INSERT INTO `Comunas` Values (7103, 'Curepto', 7);
INSERT INTO `Comunas` Values (7104, 'Empedrado', 7);
INSERT INTO `Comunas` Values (7105, 'Maule', 7);
INSERT INTO `Comunas` Values (7106, 'Pelarco', 7);
INSERT INTO `Comunas` Values (7107, 'Pencahue', 7);
INSERT INTO `Comunas` Values (7108, 'Río Claro', 7);
INSERT INTO `Comunas` Values (7109, 'San Clemente', 7);
INSERT INTO `Comunas` Values (7110, 'San Rafael', 7);
INSERT INTO `Comunas` Values (7201, 'Cauquenes', 7);
INSERT INTO `Comunas` Values (7202, 'Chanco', 7);
INSERT INTO `Comunas` Values (7203, 'Pelluhue', 7);
INSERT INTO `Comunas` Values (7301, 'Curicó', 7);
INSERT INTO `Comunas` Values (7302, 'Hualañé', 7);
INSERT INTO `Comunas` Values (7303, 'Licantén', 7);
INSERT INTO `Comunas` Values (7304, 'Molina', 7);
INSERT INTO `Comunas` Values (7305, 'Rauco', 7);
INSERT INTO `Comunas` Values (7306, 'Romeral', 7);
INSERT INTO `Comunas` Values (7307, 'Sagrada Familia', 7);
INSERT INTO `Comunas` Values (7308, 'Teno', 7);
INSERT INTO `Comunas` Values (7309, 'Vichuquén', 7);
INSERT INTO `Comunas` Values (7401, 'Linares', 7);
INSERT INTO `Comunas` Values (7402, 'Colbún', 7);
INSERT INTO `Comunas` Values (7403, 'Longaví', 7);
INSERT INTO `Comunas` Values (7404, 'Parral', 7);
INSERT INTO `Comunas` Values (7405, 'Retiro', 7);
INSERT INTO `Comunas` Values (7406, 'San Javier', 7);
INSERT INTO `Comunas` Values (7407, 'Villa Alegre', 7);
INSERT INTO `Comunas` Values (7408, 'Yerbas Buenas', 7);
INSERT INTO `Comunas` Values (8101, 'Concepción', 8);
INSERT INTO `Comunas` Values (8102, 'Coronel', 8);
INSERT INTO `Comunas` Values (8103, 'Chiguayante', 8);
INSERT INTO `Comunas` Values (8104, 'Florida', 8);
INSERT INTO `Comunas` Values (8105, 'Hualqui', 8);
INSERT INTO `Comunas` Values (8106, 'Lota', 8);
INSERT INTO `Comunas` Values (8107, 'Penco', 8);
INSERT INTO `Comunas` Values (8108, 'San Pedro de la Paz', 8);
INSERT INTO `Comunas` Values (8109, 'Santa Juana', 8);
INSERT INTO `Comunas` Values (8110, 'Talcahuano', 8);
INSERT INTO `Comunas` Values (8111, 'Tomé', 8);
INSERT INTO `Comunas` Values (8112, 'Hualpén', 8);
INSERT INTO `Comunas` Values (8201, 'Lebu', 8);
INSERT INTO `Comunas` Values (8202, 'Arauco', 8);
INSERT INTO `Comunas` Values (8203, 'Cañete', 8);
INSERT INTO `Comunas` Values (8204, 'Contulmo', 8);
INSERT INTO `Comunas` Values (8205, 'Curanilahue', 8);
INSERT INTO `Comunas` Values (8206, 'Los Álamos', 8);
INSERT INTO `Comunas` Values (8207, 'Tirúa', 8);
INSERT INTO `Comunas` Values (8301, 'Los Ángeles', 8);
INSERT INTO `Comunas` Values (8302, 'Antuco', 8);
INSERT INTO `Comunas` Values (8303, 'Cabrero', 8);
INSERT INTO `Comunas` Values (8304, 'Laja', 8);
INSERT INTO `Comunas` Values (8305, 'Mulchén', 8);
INSERT INTO `Comunas` Values (8306, 'Nacimiento', 8);
INSERT INTO `Comunas` Values (8307, 'Negrete', 8);
INSERT INTO `Comunas` Values (8308, 'Quilaco', 8);
INSERT INTO `Comunas` Values (8309, 'Quilleco', 8);
INSERT INTO `Comunas` Values (8310, 'San Rosendo', 8);
INSERT INTO `Comunas` Values (8311, 'Santa Bárbara', 8);
INSERT INTO `Comunas` Values (8312, 'Tucapel', 8);
INSERT INTO `Comunas` Values (8313, 'Yumbel', 8);
INSERT INTO `Comunas` Values (8314, 'Alto Biobío', 8);
INSERT INTO `Comunas` Values (8401, 'Chillán', 8);
INSERT INTO `Comunas` Values (8402, 'Bulnes', 8);
INSERT INTO `Comunas` Values (8403, 'Cobquecura', 8);
INSERT INTO `Comunas` Values (8404, 'Coelemu', 8);
INSERT INTO `Comunas` Values (8405, 'Coihueco', 8);
INSERT INTO `Comunas` Values (8406, 'Chillán Viejo', 8);
INSERT INTO `Comunas` Values (8407, 'El Carmen', 8);
INSERT INTO `Comunas` Values (8408, 'Ninhue', 8);
INSERT INTO `Comunas` Values (8409, 'Ñiquén', 8);
INSERT INTO `Comunas` Values (8410, 'Pemuco', 8);
INSERT INTO `Comunas` Values (8411, 'Pinto', 8);
INSERT INTO `Comunas` Values (8412, 'Portezuelo', 8);
INSERT INTO `Comunas` Values (8413, 'Quillón', 8);
INSERT INTO `Comunas` Values (8414, 'Quirihue', 8);
INSERT INTO `Comunas` Values (8415, 'Ránquil', 8);
INSERT INTO `Comunas` Values (8416, 'San Carlos', 8);
INSERT INTO `Comunas` Values (8417, 'San Fabián', 8);
INSERT INTO `Comunas` Values (8418, 'San Ignacio', 8);
INSERT INTO `Comunas` Values (8419, 'San Nicolás', 8);
INSERT INTO `Comunas` Values (8420, 'Treguaco', 8);
INSERT INTO `Comunas` Values (8421, 'Yungay', 8);
INSERT INTO `Comunas` Values (9101, 'Temuco', 9);
INSERT INTO `Comunas` Values (9102, 'Carahue', 9);
INSERT INTO `Comunas` Values (9103, 'Cunco', 9);
INSERT INTO `Comunas` Values (9104, 'Curarrehue', 9);
INSERT INTO `Comunas` Values (9105, 'Freire', 9);
INSERT INTO `Comunas` Values (9106, 'Galvarino', 9);
INSERT INTO `Comunas` Values (9107, 'Gorbea', 9);
INSERT INTO `Comunas` Values (9108, 'Lautaro', 9);
INSERT INTO `Comunas` Values (9109, 'Loncoche', 9);
INSERT INTO `Comunas` Values (9110, 'Melipeuco', 9);
INSERT INTO `Comunas` Values (9111, 'Nueva Imperial', 9);
INSERT INTO `Comunas` Values (9112, 'Padre Las Casas', 9);
INSERT INTO `Comunas` Values (9113, 'Perquenco', 9);
INSERT INTO `Comunas` Values (9114, 'Pitrufquén', 9);
INSERT INTO `Comunas` Values (9115, 'Pucón', 9);
INSERT INTO `Comunas` Values (9116, 'Saavedra', 9);
INSERT INTO `Comunas` Values (9117, 'Teodoro Schmidt', 9);
INSERT INTO `Comunas` Values (9118, 'Toltén', 9);
INSERT INTO `Comunas` Values (9119, 'Vilcún', 9);
INSERT INTO `Comunas` Values (9120, 'Villarrica', 9);
INSERT INTO `Comunas` Values (9121, 'Cholchol', 9);
INSERT INTO `Comunas` Values (9201, 'Angol', 9);
INSERT INTO `Comunas` Values (9202, 'Collipulli', 9);
INSERT INTO `Comunas` Values (9203, 'Curacautín', 9);
INSERT INTO `Comunas` Values (9204, 'Ercilla', 9);
INSERT INTO `Comunas` Values (9205, 'Lonquimay', 9);
INSERT INTO `Comunas` Values (9206, 'Los Sauces', 9);
INSERT INTO `Comunas` Values (9207, 'Lumaco', 9);
INSERT INTO `Comunas` Values (9208, 'Purén', 9);
INSERT INTO `Comunas` Values (9209, 'Renaico', 9);
INSERT INTO `Comunas` Values (9210, 'Traiguén', 9);
INSERT INTO `Comunas` Values (9211, 'Victoria', 9);
INSERT INTO `Comunas` Values (10101, 'Puerto Montt', 10);
INSERT INTO `Comunas` Values (10102, 'Calbuco', 10);
INSERT INTO `Comunas` Values (10103, 'Cochamó', 10);
INSERT INTO `Comunas` Values (10104, 'Fresia', 10);
INSERT INTO `Comunas` Values (10105, 'Frutillar', 10);
INSERT INTO `Comunas` Values (10106, 'Los Muermos', 10);
INSERT INTO `Comunas` Values (10107, 'Llanquihue', 10);
INSERT INTO `Comunas` Values (10108, 'Maullín', 10);
INSERT INTO `Comunas` Values (10109, 'Puerto Varas', 10);
INSERT INTO `Comunas` Values (10201, 'Castro', 10);
INSERT INTO `Comunas` Values (10202, 'Ancud', 10);
INSERT INTO `Comunas` Values (10203, 'Chonchi', 10);
INSERT INTO `Comunas` Values (10204, 'Curaco de Vélez', 10);
INSERT INTO `Comunas` Values (10205, 'Dalcahue', 10);
INSERT INTO `Comunas` Values (10206, 'Puqueldón', 10);
INSERT INTO `Comunas` Values (10207, 'Queilén', 10);
INSERT INTO `Comunas` Values (10208, 'Quellón', 10);
INSERT INTO `Comunas` Values (10209, 'Quemchi', 10);
INSERT INTO `Comunas` Values (10210, 'Quinchao', 10);
INSERT INTO `Comunas` Values (10301, 'Osorno', 10);
INSERT INTO `Comunas` Values (10302, 'Puerto Octay', 10);
INSERT INTO `Comunas` Values (10303, 'Purranque', 10);
INSERT INTO `Comunas` Values (10304, 'Puyehue', 10);
INSERT INTO `Comunas` Values (10305, 'Río Negro', 10);
INSERT INTO `Comunas` Values (10306, 'San Juan de la Costa', 10);
INSERT INTO `Comunas` Values (10307, 'San Pablo', 10);
INSERT INTO `Comunas` Values (10401, 'Chaitén', 10);
INSERT INTO `Comunas` Values (10402, 'Futaleufú', 10);
INSERT INTO `Comunas` Values (10403, 'Hualaihué', 10);
INSERT INTO `Comunas` Values (10404, 'Palena', 10);
INSERT INTO `Comunas` Values (11101, 'Coyhaique', 11);
INSERT INTO `Comunas` Values (11102, 'Lago Verde', 11);
INSERT INTO `Comunas` Values (11201, 'Aysén', 11);
INSERT INTO `Comunas` Values (11202, 'Cisnes', 11);
INSERT INTO `Comunas` Values (11203, 'Guaitecas', 11);
INSERT INTO `Comunas` Values (11301, 'Cochrane', 11);
INSERT INTO `Comunas` Values (11302, 'O’Higgins', 11);
INSERT INTO `Comunas` Values (11303, 'Tortel', 11);
INSERT INTO `Comunas` Values (11401, 'Chile Chico', 11);
INSERT INTO `Comunas` Values (11402, 'Río Ibáñez', 11);
INSERT INTO `Comunas` Values (12101, 'Punta Arenas', 12);
INSERT INTO `Comunas` Values (12102, 'Laguna Blanca', 12);
INSERT INTO `Comunas` Values (12103, 'Río Verde', 12);
INSERT INTO `Comunas` Values (12104, 'San Gregorio', 12);
INSERT INTO `Comunas` Values (12201, 'Cabo de Hornos (Ex - Navarino)', 12);
INSERT INTO `Comunas` Values (12202, 'Antártica', 12);
INSERT INTO `Comunas` Values (12301, 'Porvenir', 12);
INSERT INTO `Comunas` Values (12302, 'Primavera', 12);
INSERT INTO `Comunas` Values (12303, 'Timaukel', 12);
INSERT INTO `Comunas` Values (12401, 'Natales', 12);
INSERT INTO `Comunas` Values (12402, 'Torres del Paine', 12);
INSERT INTO `Comunas` Values (13101, 'Santiago', 13);
INSERT INTO `Comunas` Values (13102, 'Cerrillos', 13);
INSERT INTO `Comunas` Values (13103, 'Cerro Navia', 13);
INSERT INTO `Comunas` Values (13104, 'Conchalí', 13);
INSERT INTO `Comunas` Values (13105, 'El Bosque', 13);
INSERT INTO `Comunas` Values (13106, 'Estación Central', 13);
INSERT INTO `Comunas` Values (13107, 'Huechuraba', 13);
INSERT INTO `Comunas` Values (13108, 'Independencia', 13);
INSERT INTO `Comunas` Values (13109, 'La Cisterna', 13);
INSERT INTO `Comunas` Values (13110, 'La Florida', 13);
INSERT INTO `Comunas` Values (13111, 'La Granja', 13);
INSERT INTO `Comunas` Values (13112, 'La Pintana', 13);
INSERT INTO `Comunas` Values (13113, 'La Reina', 13);
INSERT INTO `Comunas` Values (13114, 'Las Condes', 13);
INSERT INTO `Comunas` Values (13115, 'Lo Barnechea', 13);
INSERT INTO `Comunas` Values (13116, 'Lo Espejo', 13);
INSERT INTO `Comunas` Values (13117, 'Lo Prado', 13);
INSERT INTO `Comunas` Values (13118, 'Macul', 13);
INSERT INTO `Comunas` Values (13119, 'Maipú', 13);
INSERT INTO `Comunas` Values (13120, 'Ñuñoa', 13);
INSERT INTO `Comunas` Values (13121, 'Pedro Aguirre Cerda', 13);
INSERT INTO `Comunas` Values (13122, 'Peñalolén', 13);
INSERT INTO `Comunas` Values (13123, 'Providencia', 13);
INSERT INTO `Comunas` Values (13124, 'Pudahuel', 13);
INSERT INTO `Comunas` Values (13125, 'Quilicura', 13);
INSERT INTO `Comunas` Values (13126, 'Quinta Normal', 13);
INSERT INTO `Comunas` Values (13127, 'Recoleta', 13);
INSERT INTO `Comunas` Values (13128, 'Renca', 13);
INSERT INTO `Comunas` Values (13129, 'San Joaquín', 13);
INSERT INTO `Comunas` Values (13130, 'San Miguel', 13);
INSERT INTO `Comunas` Values (13131, 'San Ramón', 13);
INSERT INTO `Comunas` Values (13132, 'Vitacura', 13);
INSERT INTO `Comunas` Values (13201, 'Puente Alto', 13);
INSERT INTO `Comunas` Values (13202, 'Pirque', 13);
INSERT INTO `Comunas` Values (13203, 'San José de Maipo', 13);
INSERT INTO `Comunas` Values (13301, 'Colina', 13);
INSERT INTO `Comunas` Values (13302, 'Lampa ', 13);
INSERT INTO `Comunas` Values (13303, 'Tiltil', 13);
INSERT INTO `Comunas` Values (13401, 'San Bernardo', 13);
INSERT INTO `Comunas` Values (13402, 'Buin', 13);
INSERT INTO `Comunas` Values (13403, 'Calera de Tango', 13);
INSERT INTO `Comunas` Values (13404, 'Paine', 13);
INSERT INTO `Comunas` Values (13501, 'Melipilla', 13);
INSERT INTO `Comunas` Values (13502, 'Alhué', 13);
INSERT INTO `Comunas` Values (13503, 'Curacaví', 13);
INSERT INTO `Comunas` Values (13504, 'María Pinto', 13);
INSERT INTO `Comunas` Values (13505, 'San Pedro', 13);
INSERT INTO `Comunas` Values (13601, 'Talagante', 13);
INSERT INTO `Comunas` Values (13602, 'El Monte', 13);
INSERT INTO `Comunas` Values (13603, 'Isla de Maipo', 13);
INSERT INTO `Comunas` Values (13604, 'Padre Hurtado', 13);
INSERT INTO `Comunas` Values (13605, 'Peñaflor', 13);
INSERT INTO `Comunas` Values (14101, 'Valdivia', 14);
INSERT INTO `Comunas` Values (14102, 'Corral', 14);
INSERT INTO `Comunas` Values (14103, 'Lanco', 14);
INSERT INTO `Comunas` Values (14104, 'Los Lagos', 14);
INSERT INTO `Comunas` Values (14105, 'Máfil', 14);
INSERT INTO `Comunas` Values (14106, 'Mariquina', 14);
INSERT INTO `Comunas` Values (14107, 'Paillaco', 14);
INSERT INTO `Comunas` Values (14108, 'Panguipulli', 14);
INSERT INTO `Comunas` Values (14201, 'La Unión', 14);
INSERT INTO `Comunas` Values (14202, 'Futrono', 14);
INSERT INTO `Comunas` Values (14203, 'Lago Ranco', 14);
INSERT INTO `Comunas` Values (14204, 'Río Bueno', 14);
INSERT INTO `Comunas` Values (15101, 'Arica', 15);
INSERT INTO `Comunas` Values (15102, 'Camarones', 15);
INSERT INTO `Comunas` Values (15201, 'Putre', 15);
INSERT INTO `Comunas` Values (15202, 'General Lagos', 15);

-- --------------------------------------------------------------------------------
-- Civiles
-- --------------------------------------------------------------------------------
 -- Nacionalidades
  create table if not exists `Nacionalidad`(
	`id` bigint auto_increment not null,
    `Nacionalidad` varchar(150) not null,
	primary key (`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8  comment 'Tabla para las nacionalidades del usuario';

INSERT INTO `Nacionalidad` VALUES(1, 'CHILENA');
INSERT INTO `Nacionalidad` VALUES(2, 'PERUANA');
INSERT INTO `Nacionalidad` VALUES(3, 'VENEZOLANA');
INSERT INTO `Nacionalidad` VALUES(4, 'ESPAÑOLA');
INSERT INTO `Nacionalidad` VALUES(5, 'COLOMBIANA');
INSERT INTO `Nacionalidad` VALUES(6, 'URUGUAYA');
INSERT INTO `Nacionalidad` VALUES(7, 'BOLIVIANA');
INSERT INTO `Nacionalidad` VALUES(1001, 'CUBANA');


 -- EstadoCivil
 create table if not exists `EstadoCivil`(
	`id` bigint auto_increment not null,
    `descripcion` varchar(50) not null,
	primary key (`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8  comment 'Tabla para el estado civil del usuario';

INSERT INTO `EstadoCivil` VALUES(1, 'Soltero');
INSERT INTO `EstadoCivil` VALUES(2, 'Casado');
INSERT INTO `EstadoCivil` VALUES(3, 'Viudo');
INSERT INTO `EstadoCivil` VALUES(4, 'Divorciado');

-- Sexo
create table if not exists `Sexo` (
	`id` bigint auto_increment not null,
	`descripcion` varchar(150) not null, 
    primary key (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment 'Tabla para el sexo del usuario';

INSERT INTO `Sexo` VALUES('1', 'Hombre');
INSERT INTO `Sexo` VALUES('2', 'Mujer');

-- NivelEstudio
create table if not exists `NivelEstudio` (
	`id` bigint auto_increment not null,
	`descripcion` varchar(150) not null,   
    primary key (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment 'Tabla para controlar los diferentes niveles académicos del usuario';

INSERT INTO  `NivelEstudio` VALUES(1, 'Básica');
INSERT INTO  `NivelEstudio` VALUES(2, 'Media Científico Humanista');
INSERT INTO  `NivelEstudio` VALUES(3, 'Media Técnico Profesional');
INSERT INTO  `NivelEstudio` VALUES(4, 'Superior Técnica (CFT o IP)');
INSERT INTO  `NivelEstudio` VALUES(5, 'Universitaria');

-- ---------------------------------------------------------------------------------
-- Bancarios
-- ---------------------------------------------------------------------------------
-- Bancos
create table if not exists `Bancos` (
	`id` bigint auto_increment not null,
	`codigo` varchar(50) not null,    
	`nombre` varchar(150) not null,   
	`nomina` boolean not null comment '0 No genera Nomina 1 Genera Nomina',  
    `created` DATETIME NOT NULL COMMENT 'fecha en que fue creado el parametro',
    `updated` DATETIME NOT NULL COMMENT 'fecha en que fue actualizado el parametro',
    `creator_user` BIGINT NOT NULL COMMENT 'usuario que creó el parametro',
    `updater_user` BIGINT NOT NULL COMMENT 'usuario que actualizó el parametro',    
    primary key (`id`),
    unique (`codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment 'Tabla para controlar los diferentes bancos en el sistema';

INSERT INTO Bancos  VALUES ('1','001', 'BANCO CHILE Y EDWARDS', 1, '1990-01-01', '1990-01-01', '1', '1');
INSERT INTO Bancos  VALUES ('2','009', 'BANCO INTERNACIONAL', 0, '1990-01-01', '1990-01-01', '1', '1');
INSERT INTO Bancos  VALUES ('3','011', 'DRESDNER BANK LATINOAMERICA', 0, '1990-01-01', '1990-01-01', '1', '1');
INSERT INTO Bancos  VALUES ('4','012', 'ESTADO', 0, '1990-01-01', '1990-01-01', '1', '1');
INSERT INTO Bancos  VALUES ('5','014', 'SCOTIABANK', 0, '1990-01-01', '1990-01-01', '1', '1');
INSERT INTO Bancos  VALUES ('6','016', 'BANCO DE CREDITOS E INVERSIONES ', 1, '1990-01-01', '1990-01-01', '1', '1');
INSERT INTO Bancos  VALUES ('7','017', 'BANCO DO BRASIL S.A.', 0, '1990-01-01', '1990-01-01', '1', '1');
INSERT INTO Bancos  VALUES ('8','027', 'CORP BANCA', 0, '1990-01-01', '1990-01-01', '1', '1');
INSERT INTO Bancos  VALUES ('9','028', 'BANCO BICE', 0, '1990-01-01', '1990-01-01', '1', '1');
INSERT INTO Bancos  VALUES ('10','029', 'BANCO DE A. EDWARDS', 0, '1990-01-01', '1990-01-01', '1', '1');
INSERT INTO Bancos  VALUES ('11','031', 'HSBC BANK CHILE', 0, '1990-01-01', '1990-01-01', '1', '1');
INSERT INTO Bancos  VALUES ('12','032', 'BANK OF AMERICA, NATIONAL ASSOCIATION', 0, '1990-01-01', '1990-01-01', '1', '1');
INSERT INTO Bancos  VALUES ('13','033', 'BANCO CITIBANK N.A.', 0, '1990-01-01', '1990-01-01', '1', '1');
INSERT INTO Bancos  VALUES ('14','036', 'BANCO DO ESTADO DE SAO PAULO', 0, '1990-01-01', '1990-01-01', '1', '1');
INSERT INTO Bancos  VALUES ('15','037', 'BANCO SANTANDER', 0, '1990-01-01', '1990-01-01', '1', '1');
INSERT INTO Bancos  VALUES ('16','039', 'BANCO ITAU', 0, '1990-01-01', '1990-01-01', '1', '1');
INSERT INTO Bancos  VALUES ('17','040', 'BANCO SUDAMERIS', 0, '1990-01-01', '1990-01-01', '1', '1');
INSERT INTO Bancos  VALUES ('18','041', 'JP MORGAN CHASE BANK', 0, '1990-01-01', '1990-01-01', '1', '1');
INSERT INTO Bancos  VALUES ('19','043', 'BANCO DE LA NACION ARGENTINA', 0, '1990-01-01', '1990-01-01', '1', '1');
INSERT INTO Bancos  VALUES ('20','045', 'THE BANK OF TOKYO- MITSUBISHI UFJ, LTD.', 0, '1990-01-01', '1990-01-01', '1', '1');
INSERT INTO Bancos  VALUES ('21','046', 'ABN AMRO BANK (CHILE)', 0, '1990-01-01', '1990-01-01', '1', '1');
INSERT INTO Bancos  VALUES ('22','049', 'BANCO SECURITY', 0, '1990-01-01', '1990-01-01', '1', '1');
INSERT INTO Bancos  VALUES ('23','051', 'BANCO FALABELLA', 0, '1990-01-01', '1990-01-01', '1', '1');
INSERT INTO Bancos  VALUES ('24','052', 'DEUTSCHE BANK (CHILE)', 0, '1990-01-01', '1990-01-01', '1', '1');
INSERT INTO Bancos  VALUES ('25','053', 'BANCO RIPLEY', 0, '1990-01-01', '1990-01-01', '1', '1');
INSERT INTO Bancos  VALUES ('26','054', 'HNS BANCO', 0, '1990-01-01', '1990-01-01', '1', '1');
INSERT INTO Bancos  VALUES ('27','055', 'BANCO MONEX', 0, '1990-01-01', '1990-01-01', '1', '1');
INSERT INTO Bancos  VALUES ('28','056', 'BANCO PENTA', 0, '1990-01-01', '1990-01-01', '1', '1');
INSERT INTO Bancos  VALUES ('29','057', 'BANCO PARIS', 0, '1990-01-01', '1990-01-01', '1', '1');
INSERT INTO Bancos  VALUES ('30','504', '(BBVA) BANCO BILBAO VIZCAYA ARGENTARIA, CHILE', 0, '1990-01-01', '1990-01-01', '1', '1');
INSERT INTO Bancos  VALUES ('31','507', 'BANCO DEL DESARROLLO', 0, '1990-01-01', '1990-01-01', '1', '1');
INSERT INTO Bancos  VALUES ('32','671', 'COOCRETAL', 0, '1990-01-01', '1990-01-01', '1', '1');
INSERT INTO Bancos  VALUES ('33','672', 'COOPEUCH', 0, '1990-01-01', '1990-01-01', '1', '1');
INSERT INTO Bancos  VALUES ('34','734', 'BANCO CONOSUR', 0, '1990-01-01', '1990-01-01', '1', '1');
INSERT INTO Bancos  VALUES ('35','800', 'SANTANDER-STGO', 0, '1990-01-01', '1990-01-01', '1', '1');

-- *********************************************************************************
-- tablas Maestras
-- *********************************************************************************
-- Empresa
-- Representa las Sociedades
/*
se divide la informacion antes contenida en configuraciones del b1 en dos tablas, 
la de datos propiamente dichos de la empresa y la de los parametros que 
configuran el compotamiento de la empresa
*/
create table if not exists `Sociedad` (
	`id` bigint auto_increment not null,
	`rut` varchar(100) not null,	
	`nombre` varchar(200) not null,	
	`direccion` text not null,
	`region_id`  bigint	not null , -- referencua a Regiones	 Listo
	`comuna_id`  bigint	not null , -- referencua a Comunas Listo
	`ciudad` varchar(250) not null,    
	`created` datetime NOT NULL comment 'fecha en que fue creado el registro',    
	`updated`  datetime NOT NULL  comment 'fecha en que fue actualizado el registro',   
    `creator_user` BIGINT NOT NULL  comment 'usuario que creó el parametro',     
    `updater_user` BIGINT NOT NULL  comment 'usuario que actualizó el parametro',      
    primary key (`id`),
    constraint `FK_Regiones_Empresa` foreign key (`region_id`) references `Regiones` (`id`) 
    on  update cascade on delete restrict,
    constraint `FK_Comunas_Empresa` foreign key (`comuna_id`) references `Comunas` (`id`) 
    on  update cascade on delete restrict
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment 'Tabla para controlarla los datos de la empresa (sociedades)';

insert into `Sociedad` values ('1','RutDemo','Demo','Direccion Demo','1','1101','Demo Ciudad','1990-01-01','1990-01-01','1','1');

-- Roles
CREATE TABLE IF NOT EXISTS `Roles` (
    `id` BIGINT AUTO_INCREMENT NOT NULL,
    `sociedad_id` BIGINT NULL,    
    `descripcion` varchar(250) not NULL, 
    `estado` boolean not NULL, 
	`created` datetime NOT NULL,    
	`updated`  datetime NOT NULL,   
    `creator_user` BIGINT NOT NULL,     
    `updater_user` BIGINT NOT NULL,       
    PRIMARY KEY (`id`)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8 comment 'Tabla los roles dentro del sistema';

insert into `Roles` values ('1','1','root','1','1990-01-01','1990-01-01','1','1');
insert into `Roles` values ('2','1','administrador','1','1990-01-01','1990-01-01','1','1');
insert into `Roles` values ('3','1','RRHH Consultor','1','1990-01-01','1990-01-01','1','1');

-- CuentasContables
CREATE TABLE `CuentasContables` (
	`id` bigint  NOT NULL,
	`acct_code` varchar(20)  NOT NULL,
	`sociedad_id` bigint  NOT NULL,
	`acct_name` varchar(100) NOT NULL,
	`finance` char(1) NOT NULL,
	 PRIMARY KEY (`acct_code`),
     unique (`acct_code`),
     constraint `FK_Sociedad_CuentasContables` foreign key (`sociedad_id`) references `Sociedad` (`id`) 
     on update cascade on delete restrict
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment 'Tabla para controlar las cuentas contables';


-- FormasPago
create table if not exists `FormasPago` (
	`id` bigint auto_increment not null,
	`sociedad_id` bigint  NOT NULL,    
	`descripcion` varchar(50) not null,    
    primary key (`id`),
     constraint `FK_Sociedad_FormasPago` foreign key (`sociedad_id`) references `Sociedad` (`id`) 
     on update cascade on delete restrict    
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment 'Tabla para controlar las  diferentes fprmas de pago';

-- ---------------------------------------------------------------------------------
-- Parametrizaciones
-- ---------------------------------------------------------------------------------
-- TiposParametros
create table if not exists `TiposParametros` (
	`id` bigint auto_increment not null,
	`sociedad_id` bigint  NOT NULL,      
	`descripcion` varchar(150) not null,    
	`estado` boolean not null comment '0 Inactivo 1 Activo',      
    primary key (`id`),
     constraint `FK_Sociedad_TiposParametros` foreign key (`sociedad_id`) references `Sociedad` (`id`) 
     on update cascade on delete restrict     
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment 'Tabla para controlar los tipos parametros ';

-- centralizaciones
create table if not exists `Centralizaciones` (
	`id` bigint auto_increment not null,
	`sociedad_id` bigint  NOT NULL,      
	`usa_centros_costos` boolean not null,
	`cuenta_anticipo` varchar(50) null,
	`cuenta_bonos_feriado` varchar(50) null,    
	`cuenta_honoraios` varchar(50) null,
	`cuenta_prestamos_solidarios` varchar(50) null,
	`prestamo_solidario_imponible` boolean not null,    
    primary key (`id`),
     constraint `FK_Sociedad_Centralizaciones` foreign key (`sociedad_id`) references `Sociedad` (`id`) 
     on update cascade on delete restrict     
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment 'Tabla para controlarlas centralizaciones';

-- hay una tabla DetallesCentralizacion
-- ParametrosBasicos
-- esto corrresponde a los elementos que conformarán los calculos
CREATE TABLE IF NOT EXISTS `ParametrosBasicos` (
    `id` BIGINT AUTO_INCREMENT NOT NULL,
    `codigo` varchar(5) NOT NULL comment 'este codigo se utilizará como abreviatura en los cálculos de las formulas',  
	`sociedad_id` bigint  NOT NULL,        
    `concepto` varchar(250) NOT NULL,
    `tipo_parametro_id` bigint NOT NULL,
    `valor` numeric(18,4) NOT NULL,	
    `estado` boolean NOT NULL comment 'especifica si el parametro esta activo o no para el cálculo - 0 Inactivo 1 Activo',	
	`created` datetime NOT NULL comment 'fecha en que fue creado el parametro',    
	`updated`  datetime NOT NULL  comment 'fecha en que fue actualizado el parametro',   
    `creator_user` BIGINT NOT NULL  comment 'usuario que creó el parametro',     
    `updater_user` BIGINT NOT NULL  comment 'usuario que actualizó el parametro',     
    PRIMARY KEY (`id`),
    unique (`codigo`),
     constraint `FK_Sociedad_ParametrosBasicos` foreign key (`sociedad_id`) references `Sociedad` (`id`) 
     on update cascade on delete restrict      
)  ENGINE=INNODB DEFAULT CHARSET=UTF8 comment 'Tabla que permite controlar los parametros basicos de cálculo de remuneraciones';



-- HistoricoParametrosBasicos
CREATE TABLE IF NOT EXISTS `HistoricoParametrosBasicos` (
    `id` BIGINT NOT NULL,
    `codigo` varchar(5) NOT NULL comment 'este codigo se utilizará como abreviatura en los cálculos de las formulas',    
    `concepto` varchar(250) NOT NULL,
    `tipo_parametro_id` bigint NOT NULL,
    `valor` numeric(18,4) NOT NULL,	
    `estado` boolean NOT NULL comment 'especifica si el parametro esta activo o no para el cálculo - 0 Inactivo 1 Activo',	
	`created` datetime NOT NULL comment 'fecha en que fue creado el parametro',    
	`updated`  datetime NOT NULL  comment 'fecha en que fue actualizado el parametro',   
    `creator_user` BIGINT NOT NULL  comment 'usuario que creó el parametro',     
    `updater_user` BIGINT NOT NULL  comment 'usuario que actualizó el parametro'
)  ENGINE=INNODB DEFAULT CHARSET=UTF8 comment 'Tabla que permite controlar los parametros basicos de cálculo de remuneraciones';


-- Formulas
CREATE TABLE IF NOT EXISTS `Formulas` (
	`id` BIGINT AUTO_INCREMENT NOT NULL,
	`sociedad_id` bigint  NOT NULL,     
	`nombre` varchar(250) NOT NULL,
	`expresion` text NOT NULL comment 'contentivo de la formua asociada al cálculo, esta fórmula contiene los codigos de los ParametrosBasicos ejemplo  ((p1*10)/b2)',
	`estado` boolean NOT NULL comment 'especifica si la formula esta activa o no para el cálculo - 0 Inactivo 1 Activo',	    
	`created` datetime NOT NULL comment 'fecha en que fue creado el parametro',    
	`updated`  datetime NOT NULL  comment 'fecha en que fue actualizado el parametro',   
	`creator_user` BIGINT NOT NULL  comment 'usuario que creó el parametro',     
	`updater_user` BIGINT NOT NULL  comment 'usuario que actualizó el parametro',   	
	PRIMARY KEY (`id`),
	constraint `FK_Sociedad_Formulas` foreign key (`sociedad_id`) references `Sociedad` (`id`) 
	on update cascade on delete restrict      
)  ENGINE=INNODB DEFAULT CHARSET=UTF8 comment 'Tabla que permite controlar las fórmulas';


-- HistoricoFormulas
CREATE TABLE IF NOT EXISTS `HistoricoFormulas` (
    `id` BIGINT AUTO_INCREMENT NOT NULL,
    `nombre` varchar(250) NOT NULL,
    `expresion` text NOT NULL comment 'contentivo de la formua asociada al cálculo, esta fórmula contiene los codigos de los ParametrosBasicos ejemplo  ((p1*10)/b2)',
	`estado` boolean NOT NULL comment 'especifica si la formula esta activa o no para el cálculo - 0 Inactivo 1 Activo',	    
	`created` datetime NOT NULL comment 'fecha en que fue creado el parametro',    
	`updated`  datetime NOT NULL  comment 'fecha en que fue actualizado el parametro',   
    `creator_user` BIGINT NOT NULL  comment 'usuario que creó el parametro',     
    `updater_user` BIGINT NOT NULL  comment 'usuario que actualizó el parametro',
	`fecharegistro` datetime NOT NULL,
    primary key (`id`,`fecharegistro`)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8 comment 'Tabla que permite controlar las fórmulas';



-- Configuraciones Esta tabla maneja los aspectos básicoa de la identificacion de la empresa
CREATE TABLE `Configuraciones` (
	`id` bigint auto_increment not null,
	`sociedad_id` bigint not null, -- relacionado con la tabla sociedad    
	`nombre` varchar(150) NOT NULL,
	`valor` numeric(18,4) NOT NULL,
	`detalle` text  NULL,
	`cuenta` varchar(20)  NULL,
	`categoria` varchar(250) NULL,
	`categoria_id` int NULL,
	`ocultar` bit DEFAULT 0 NOT NULL,
	`tipo_validacion` varchar(30)  NULL,
	`orden` int NULL,
	`created` datetime NOT NULL comment 'fecha en que fue creado el registro',    
	`updated`  datetime NOT NULL  comment 'fecha en que fue actualizado el registro',   
    `creator_user` BIGINT NOT NULL  comment 'usuario que creó el parametro',     
    `updater_user` BIGINT NOT NULL  comment 'usuario que actualizó el parametro', 
	primary key (`id`),
    constraint `FK_Sociedad_Configuraciones` foreign key (`sociedad_id`) references `Sociedad` (`id`) 
    on  update cascade on delete restrict    
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment 'Tabla para controlarla los datos de la empresa (sociedades)';


-- HistoricoConfiguraciones
CREATE TABLE `HistoricoConfiguraciones` (
	`id` bigint not null,
	`sociedad_id` bigint not null, 
	`nombre` varchar(150) NOT NULL,
	`valor` numeric(18,4) NOT NULL,
	`detalle` text  NULL,
	`cuenta` varchar(20)  NULL,
	`categoria` varchar(250) NULL,
	`categoria_id` int NULL,
	`ocultar` bit DEFAULT 0 NOT NULL,
	`tipo_validacion` varchar(30)  NULL,
	`orden` int NULL,
	`created` datetime NOT NULL comment 'fecha en que fue creado el registro',    
	`updated`  datetime NOT NULL  comment 'fecha en que fue actualizado el registro',   
    `creator_user` BIGINT NOT NULL  comment 'usuario que creó el parametro',     
    `updater_user` BIGINT NOT NULL  comment 'usuario que actualizó el parametro', 
	`fecha_historico_created` datetime NOT NULL,
	PRIMARY KEY (`fecha_historico_created`,`id`,`sociedad_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment 'Tabla para controlarla los datos de la empresa (sociedades)';


-- GrupoEmpleados
CREATE TABLE `GruposEmpleado` (
	`id` bigint auto_increment not null,
	`sociedad_id` bigint  not null, -- sociedad con la cual esta relacionado el grupo    
	`es_honorario` boolean DEFAULT 0 NOT NULL,
	`nombre` varchar(200)  NOT NULL,
	`monto_max_prestamo` numeric(18,4) NULL,
	`cuotas_max_prestamo` int NULL,
	`porcentaje_tope_cuota_prestamo` numeric(18,4) NULL,
	`monto_max_anticipo` numeric(18,4) NULL,
	`porcentaje_max_anticipo` numeric(18,4) NULL,
	`calcular_porcentaje_segun` varchar(10)  NULL,
	`factura_mas_pago` boolean DEFAULT 0 NOT NULL,
	`cuenta_factura_proveedor` varchar(20),
	`cuenta_pago_factura` varchar(20) NULL,
	`cuenta_remunera_deb` varchar(20) NULL,
	`cuenta_AFP_debitar` varchar(20) NULL,
	`cuenta_salud_Deb` varchar(20) NULL,
	`cuenta_gratificacion_deb` varchar(20) NULL,
	`cuentas_horas_ext_debitar` varchar(20)  NULL,
	`cuenta_seguro_AFC_debitar` varchar(20)  NULL,
	`cuenta_mov_debitar` varchar(20)  NULL,
	`cuenta_colacion_debitar` nvarchar(20)   NULL,
	`cuenta_otras_asignaciones_debitar` varchar(20)  NULL,
	`cuenta_SIS_debitar` varchar(20)  NULL,
	`cuenta_mutual_debitar` nvarchar(20)   NULL,
	`CueImpUnic_Deb` nvarchar(20)   NULL,
	`CueAsigFami_Deb` nvarchar(20)   NULL,
	`CueAfcEmpresa_Cred` nvarchar(20)   NULL,
	`CueAsigFami_Cred` nvarchar(20)   NULL,
	`CueImpUnic_Cred` nvarchar(20)   NULL,
	`CueSueldoxPagar_Cred` nvarchar(20)   NULL,
	`created` datetime NOT NULL comment 'fecha en que fue creado el registro',    
	`updated`  datetime NOT NULL  comment 'fecha en que fue actualizado el registro',   
    `creator_user` BIGINT NOT NULL  comment 'usuario que creó el parametro',     
    `updater_user` BIGINT NOT NULL  comment 'usuario que actualizó el parametro',     
	 PRIMARY KEY (`id`),
    constraint `FK_Sociedad_GruposEmpleado` foreign key (`sociedad_id`) references `Sociedad` (`id`) 
    on  update cascade on delete restrict      
)  ENGINE=INNODB DEFAULT CHARSET=UTF8 comment 'Tabla de grupos de empleados';


-- Cargos
CREATE TABLE `Cargos` (
	`id` bigint auto_increment not NULL,
	`sociedad_id` bigint  not null, -- sociedad con la cual esta relacionado el cargo       
	`nombre` varchar(150) not NULL,
	`nivel_cargo` varchar(10) NULL,
	`created` datetime NOT NULL comment 'fecha en que fue creado el registro',    
	`updated`  datetime NOT NULL  comment 'fecha en que fue actualizado el registro',   
    `creator_user` BIGINT NOT NULL  comment 'usuario que creó el parametro',     
    `updater_user` BIGINT NOT NULL  comment 'usuario que actualizó el parametro',      
	 PRIMARY KEY (`id`),
    constraint `FK_Sociedad_Cargos` foreign key (`sociedad_id`) references `Sociedad` (`id`) 
    on  update cascade on delete restrict        
)  ENGINE=INNODB DEFAULT CHARSET=UTF8 comment 'Tabla de grupos de empleados';


-- se hace una division de los datos en relacion con la tabla original del B1 Nomina
-- se separan datos personales, direccion, contactom datos bancarios
-- se crea una tabla para hacewr la relacion Sociedad_Usuario
-- Usuario
CREATE TABLE IF NOT EXISTS `Usuario` (
    `id` BIGINT AUTO_INCREMENT NOT NULL,
    `rut` VARCHAR(100) NOT NULL,
    `rut_provisorio` VARCHAR(100) NULL,
    `nombres` VARCHAR(100) NOT NULL,
    `apellido_paterno` VARCHAR(100) NOT NULL,
    `apellido_materno` VARCHAR(100) NULL,
    `fecha_nacimiento` DATE NOT NULL,
    `sexo_id` BIGINT NOT NULL,
    `estado_civil_id` BIGINT NOT NULL,    
    `nacionalidad_id` BIGINT NOT NULL, 
    `username` varchar(250) NOT NULL,    
	`password` varchar(250) NOT NULL,  
	`activo` boolean NOT NULL comment 'campo para activar o no al usuario 0 Inactivo 1 Activo',           
	`created` datetime NOT NULL,    
	`updated`  datetime NOT NULL,   
    `creator_user` BIGINT NOT NULL,     
    `updater_user` BIGINT NOT NULL,      
    PRIMARY KEY (`id`),
    unique (`rut`),
    unique (`username`),
    constraint `FK_Nacionalidad_Usuario` foreign key (`nacionalidad_id`) references `Nacionalidad` (`id`) 
    on  update cascade on delete restrict,   
    constraint `FK_Sexo_Usuario` foreign key (`sexo_id`) references `Sexo` (`id`) 
    on  update cascade on delete restrict,    
    constraint `FK_EstadoCivil_Usuario` foreign key (`estado_civil_id`) references `EstadoCivil` (`id`) 
    on  update cascade on delete restrict
)  ENGINE=INNODB DEFAULT CHARSET=UTF8 comment 'Tabla de  usuarios';

-- creamos el root del sistema
insert into `Usuario` values ('1','1','','Admin','Root','','1990-01-01','1','1','1','root','$2b$12$6JXJ6qmx9co08Nk5zTE.aeDIB8ohWUtAiLytiVHmBH9YuKJHCIkUm','1','1990-01-01','1990-01-01','1','1');

-- Contacto


CREATE TABLE IF NOT EXISTS `Contacto` (
    `id` BIGINT AUTO_INCREMENT NOT NULL,
    `user_id` BIGINT NULL,    
    `email` varchar(250) NULL,       
    `fijo` varchar(20) NULL,   
    `movil` varchar(20) NULL, 
	`created` datetime NOT NULL,    
	`updated`  datetime NOT NULL,   
    `creator_user` BIGINT NOT NULL,     
    `updater_user` BIGINT NOT NULL,      
    PRIMARY KEY (`id`),
    constraint `FK_Usuario_Contacto` foreign key (`user_id`) references `Usuario` (`id`) 
    on  update cascade on delete restrict
)  ENGINE=INNODB DEFAULT CHARSET=UTF8 comment 'Tabla de contacto de los usuarios';

-- Ubicación
CREATE TABLE IF NOT EXISTS `Ubicacion` (
    `id` BIGINT AUTO_INCREMENT NOT NULL,
    `user_id` BIGINT NULL, 
    `region_id` BIGINT not NULL,    
    `comuna_id` BIGINT not NULL,    
    `direccion` text not NULL,   
	`created` datetime NOT NULL,    
	`updated`  datetime NOT NULL,   
    `creator_user` BIGINT NOT NULL,     
    `updater_user` BIGINT NOT NULL,     
    PRIMARY KEY (`id`),
    constraint `FK_Usuario_Ubicacion` foreign key (`user_id`) references `Usuario` (`id`) 
    on  update cascade on delete restrict,
    constraint `FK_Region_Ubicacion` foreign key (`region_id`) references `Regiones` (`id`) 
    on  update cascade on delete restrict ,
    constraint `FK_Comuna_Ubicacion` foreign key (`comuna_id`) references `Comunas` (`id`) 
    on  update cascade on delete restrict     
)  ENGINE=INNODB DEFAULT CHARSET=UTF8 comment 'Tabla de ubicación de los usuarios';


-- archivos de usuario
-- Usados para mostrar en el profile del usuario como referencia
CREATE TABLE `FilesUsers` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `url` text NOT NULL,  
  `created` datetime NOT NULL,
  `updated` datetime NOT NULL,
  `creator_user` bigint(20) NOT NULL,
  `updater_user` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  constraint `FK_Usuario_FilesUsers` foreign key (`user_id`) references `Usuario`(`id`)
  on update cascade on delete restrict
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Tabla de archivos de los usuarios';

-- SociedadUsuario
CREATE TABLE IF NOT EXISTS `SociedadUsuario` (
    `id` BIGINT AUTO_INCREMENT NOT NULL,
    `user_id` BIGINT NULL, 
    `sociedad_id` BIGINT not NULL,
	`created` datetime NOT NULL,    
	`updated`  datetime NOT NULL,   
    `creator_user` BIGINT NOT NULL,     
    `updater_user` BIGINT NOT NULL,     
    PRIMARY KEY (`id`),
    constraint `FK_Usuario_SociedadUsuario` foreign key (`user_id`) references `Usuario` (`id`) 
    on  update cascade on delete restrict,
    constraint `FK_Sociedad_SociedadUsuario` foreign key (`sociedad_id`) references `SociedadUsuario` (`id`) 
    on  update cascade on delete restrict
)  ENGINE=INNODB DEFAULT CHARSET=UTF8 comment 'Tabla de Asociación de los usuarios con las sociedades del cliente';


-- FormaPagoUsuario
CREATE TABLE IF NOT EXISTS `FormasPagoUsuario` (
    `id` BIGINT AUTO_INCREMENT NOT NULL,
    `user_id` BIGINT NULL, 
	`forma_pago_id` BIGINT NULL,  
	`created` datetime NOT NULL,    
	`updated`  datetime NOT NULL,   
    `creator_user` BIGINT NOT NULL,     
    `updater_user` BIGINT NOT NULL,     
    PRIMARY KEY (`id`),
    constraint `FK_Usuario_FormaPagoUsuario` foreign key (`user_id`) references `Usuario` (`id`) 
    on  update cascade on delete restrict,
    constraint `FK_FormaPago_FormaPagoUsuario` foreign key (`forma_pago_id`) references `FormasPago` (`id`) 
    on  update cascade on delete restrict    
)  ENGINE=INNODB DEFAULT CHARSET=UTF8 comment 'Tabla de asigancion de formas de pagos del usuario';


-- BancariosUser
CREATE TABLE IF NOT EXISTS `BancariosUser` (
    `id` BIGINT AUTO_INCREMENT NOT NULL,
    `user_id` BIGINT NULL, 
    `banco_id` BIGINT not NULL, 
	`numero_cuenta` varchar(100) not NULL,
	`en_uso` boolean not NULL,    
	`terceros` boolean not NULL,        
	`rut_tercero` varchar(100) NULL,     
	`nombre_tercero` varchar(100) NULL,         
	`email_tercero` varchar(250) NULL,             
	`created` datetime NOT NULL,    
	`updated`  datetime NOT NULL,   
    `creator_user` BIGINT NOT NULL,     
    `updater_user` BIGINT NOT NULL,       
    PRIMARY KEY (`id`),
    constraint `FK_Usuario_BancariosUsuario` foreign key (`user_id`) references `Usuario` (`id`) 
    on  update cascade on delete restrict,
    constraint `FK_Bancos_BancariosUsuario` foreign key (`banco_id`) references `Bancos` (`id`) 
    on  update cascade on delete restrict
)  ENGINE=INNODB DEFAULT CHARSET=UTF8 comment 'Tabla de datos bancarios de pagos del usuario';


-- CargosUsuario
CREATE TABLE IF NOT EXISTS `CargosUsuario` (
    `id` BIGINT AUTO_INCREMENT NOT NULL,
    `sociedad_id` BIGINT NULL,    
    `user_id` BIGINT NULL, 
    `cargo_id` BIGINT NULL, 
	`created` datetime NOT NULL,    
	`updated`  datetime NOT NULL,   
    `creator_user` BIGINT NOT NULL,     
    `updater_user` BIGINT NOT NULL,       
    PRIMARY KEY (`id`),
    constraint `FK_Usuario_CargosUsuario` foreign key (`user_id`) references `Usuario` (`id`) 
    on  update cascade on delete restrict,
    constraint `FK_Cargos_CargosUsuario` foreign key (`cargo_id`) references `Cargos` (`id`) 
    on  update cascade on delete restrict,
    constraint `FK_Sociedad_CargosUsuarios` foreign key (`sociedad_id`) references `Sociedad` (`id`) 
    on  update cascade on delete restrict    
)  ENGINE=INNODB DEFAULT CHARSET=UTF8 comment 'Tabla de datos bancarios de pagos del usuario';


-- tabla de Periodos
CREATE TABLE `Periodos` (
	`id` bigint auto_increment NOT NULL,
	`sociedad_id` bigint  NOT NULL,    
	`anio` int NOT NULL,
	`mes` int NOT NULL,
	`nombre` varchar(200) NOT NULL,
	`observacion` text NULL,
	`utm` numeric(18,4) NULL,
	`uf` numeric(18,4) NULL,   
	`factor_actualizacion` numeric(18,4) NULL,    
	`activo` boolean NOT NULL,
	`created` datetime NOT NULL,    
	`updated`  datetime NOT NULL,   
    `creator_user` BIGINT NOT NULL,     
    `updater_user` BIGINT NOT NULL,       
	PRIMARY KEY (`id`),
    constraint `FK_Sociedad_Periodos` foreign key (`sociedad_id`) references `sociedad` (`id`) 
    on  update cascade on delete restrict
) ENGINE=INNODB DEFAULT CHARSET=UTF8 comment 'Tabla de Periodos';


CREATE TABLE `HistoricoPeriodos` (
	`id` bigint auto_increment NOT NULL,
	`sociedad_id` bigint  NOT NULL,    
	`anio` int NOT NULL,
	`mes` int NOT NULL,
	`nombre` varchar(200) NOT NULL,
	`observacion` text NULL,
	`utm` numeric(18,4) NULL,
	`uf` numeric(18,4) NULL,   
	`factor_actualizacion` numeric(18,4) NULL,    
	`activo` boolean NOT NULL,
	`created` datetime NOT NULL,    
	`updated`  datetime NOT NULL,   
    `creator_user` BIGINT NOT NULL,     
    `updater_user` BIGINT NOT NULL,       
    `fecha_historico_created` datetime NOT NULL,        
	PRIMARY KEY (`id`,`sociedad_id`,`fecha_historico_created`)
) ENGINE=INNODB DEFAULT CHARSET=UTF8 comment 'Tabla de Periodos'; 


-- CentrosDeCostos 
 CREATE TABLE `CentrosDeCostos` (
	`id` bigint auto_increment NOT NULL,
	`sociedad_id` bigint  NOT NULL,    
	`codigo_sap` varchar(50)  NULL,
	`centro_costo` varchar(200)  NULL,
	`dimension_id` int NULL, -- este campo esta relacionado con la tabla dimensiones, sin embargo puede ser null
	 PRIMARY KEY (`id`),
    constraint `FK_Sociedad_CentrosDeCostos` foreign key (`sociedad_id`) references `Sociedad` (`id`) 
    on  update cascade on delete restrict     
)  ENGINE=INNODB DEFAULT CHARSET=UTF8 comment 'Tabla de Centros de costos, basicamente usado para conectarse a los ERP';


-- TiposPrestamos 
CREATE TABLE `TiposPrestamos` (
	`id` bigint auto_increment NOT NULL,
	`sociedad_id` bigint  NOT NULL,     
	`descripcion` varchar(150)  NOT NULL,
	`cuenta` varchar(30)  NULL,
	`CCAF` boolean DEFAULT 0 NOT NULL,
	`caja_compensacion_id` bigint NULL,-- esta columna se relaciona con las cajas de compensacion si y solo si la cuenta es CCAF
	PRIMARY KEY (`id`),
    constraint `FK_Sociedad_TiposPrestamos` foreign key (`sociedad_id`) references `Sociedad` (`id`) 
    on  update cascade on delete restrict         
) ENGINE=INNODB DEFAULT CHARSET=UTF8 comment 'Tabla de tipos de prestamos';


-- Alertas
CREATE TABLE `Alertas` (
	`id` bigint auto_increment NOT NULL,
	`sociedad_id` bigint NOT NULL,    
	`nombre` varchar(250)  NULL,
	`Activa` boolean DEFAULT 0 NULL,
	`tipo_periodo` char(1)  NOT NULL,
	`hora_envio` time NULL,
	`lunes` boolean DEFAULT 0 NULL,
	`martes` boolean DEFAULT 0 NULL,
	`miercoles` boolean DEFAULT 0 NULL,
	`jueves` boolean DEFAULT 0 NULL,
	`viernes` boolean DEFAULT 0 NULL,
	`sabado` boolean DEFAULT 0 NULL,
	`Ddomingo` boolean DEFAULT 0 NULL,
	`dia_mes` int NULL,
	`destinatarios` text NOT NULL,
	`copia_destinatarios` text NULL,
	`p1` varchar(250)  NULL,
	`descripcion_p1` varchar(250)  NULL,
	`p2` varchar(250)  NULL NULL,
	`descripcion_p2` varchar(250) NULL,
	`consulta_reporte` text NULL, -- esta columna almacena una consulta sql
	`p_texto` text NULL,
	`considerar_jefatura` boolean DEFAULT 0 NOT NULL,
	 PRIMARY KEY (`id`),
	constraint `FK_Sociedad_Alertas` foreign key (`sociedad_id`) references `Sociedad` (`id`) 
    on  update cascade on delete restrict       
) ENGINE=INNODB DEFAULT CHARSET=UTF8 comment 'Tabla de Alertas';



-- ---------------------------------------------------------------------------------
-- Tablas para Eventos de Nomina
-- ----------------------------------------------------------------------------------- 
-- ConceptosEventos en el sistema antigua EventosConceptos
-- Esta es la forma como se traducen a la dirección del trabajo los conceptos de los bonos
create table if not exists `ConceptosEventos` (
	`id` bigint auto_increment not null,
	`sociedad_id` bigint not null, -- relacionado con la tabla sociedad        
	`descripcion` varchar(150) not null,    
	`activo` boolean not null comment '0 Inactivo 1 Activo',      
    primary key (`id`),
    constraint `FK_Sociedad_ConceptosEventos` foreign key (`sociedad_id`) references `Sociedad` (`id`) 
    on  update cascade on delete restrict       
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment 'Tabla para controlar los conceptos descriptivos de los eventos en el sistema de nomina';


-- TiposEventos
create table if not exists `TiposEvento` (
	`id` bigint auto_increment not null,
	`sociedad_id` bigint not null, -- relacionado con la tabla sociedad        
	`tipo_evento` varchar(150)  NOT NULL,
	PRIMARY KEY (`id`),
    constraint `FK_Sociedad_TiposEvento` foreign key (`sociedad_id`) references `Sociedad` (`id`) 
    on  update cascade on delete restrict      
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment 'Tabla para controlar los tipos de eventos';


-- EstadoEventos
create table if not exists `EstadosEvento` (
	`id` bigint auto_increment NOT NULL,
	`sociedad_id` bigint not null, -- relacionado con la tabla sociedad    		Listo       
	`descripcion` varchar(150) not NULL,
	PRIMARY KEY (`id`),
	constraint `FK_Sociedad_EventosEstado` foreign key (`sociedad_id`) references `Sociedad` (`id`) 
	on  update cascade on delete restrict     
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment 'Tabla para controlar los estados de los eventos';


-- EventosConfigBase
create table if not exists `EventosConfigBase` (
	`id` bigint auto_increment not NULL,
	`sociedad_id` bigint not null comment 'sociedad a la que pertenece esta configuracion de eventos', -- relacionado con la tabla sociedad    		Listo       
	`concepto_evento_id` bigint not null ,   -- relacion con ConceptosEvento 	Listo
	`tipo_evento_id` bigint NOT NULL, -- relacion con tipo de evento 			listo
	`cuenta_contable` varchar(20) NULL comment 'representa una cuanta en el centro de costos, pero puede ser nulo',
	`nombre_evento` text NOT NULL  comment 'nombre del evento',
	`descripcion` text NULL comment 'cualquier descripcion adicional que quierea colocar el operador',
	`unidad_pacto_id` bigint not null comment 'relacionado con la tabla UnidadesPacto', 
	`autorizacion` boolean not NULL comment 'especifica si el evento requiere o no autorización para el pago',
	`proporcional_mes` boolean DEFAULT 0 NOT NULL comment 'especifica si se trata de un calculo relacionado al pago mensual o es un monto absoluto',
	`template_id` bigint NULL comment 'relacion con la tabla de templates de eventos no obligatoria',
	`activo` boolean not null comment '0 Inactivo 1 Activo', 
	`created` datetime NOT NULL,    
	`updated`  datetime NOT NULL,   
    `creator_user` BIGINT NOT NULL,     
    `updater_user` BIGINT NOT NULL,        
	PRIMARY KEY (`id`),
    constraint `FK_Sociedad_EventosConfigBase` foreign key (`sociedad_id`) references `Sociedad` (`id`) 
    on  update cascade on delete restrict,     
    constraint `FK_ConceptosEvento_EventosConfigBase` foreign key (`concepto_evento_id`) references `ConceptosEventos` (`id`)
		on update cascade on delete restrict,    
    constraint `FK_TipoEvento_EventosConfigBase` foreign key (`tipo_evento_id`) references `TiposEvento` (`id`)
		on update cascade on delete restrict,
    constraint `FK_UnidadesPacto_EventosConfigBase` foreign key (`unidad_pacto_id`) references `UnidadesPacto` (`id`)
		on update cascade on delete restrict        
)  ENGINE=InnoDB DEFAULT CHARSET=utf8 comment 'Tabla para controlar la configuracionde los eventos base';

-- HistoricoEventosConfigBase
create table if not exists `HisoricoEventosConfigBase` (
	`id` bigint not NULL,
	`sociedad_id` bigint not null comment 'sociedad a la que pertenece esta configuracion de eventos', -- relacionado con la tabla sociedad    		Listo       
	`concepto_evento_id` bigint not null comment 'cual es el concepto relacionado, esto es usado en el informe de la DT' ,   -- relacion con ConceptosEvento 	Listo
	`tipo_evento_id` bigint NOT NULL comment 'cual es el concepto relacionado, esto es usado en el informe de la DT', -- relacion con tipo de evento 			listo
	`cuenta_contable` varchar(20) NULL comment 'representa una cuanta en el centro de costos, pero puede ser nulo',
	`nombre_evento` text NOT NULL  comment 'nombre del evento',
	`descripcion` text NULL comment 'cualquier descripcion adicional que quierea colocar el operador',
	`unidad_pacto_id` bigint not null comment 'relacionado con la tabla UnidadesPacto', 
	`autorizacion` boolean not NULL comment 'especifica si el evento requiere o no autorización para el pago',
	`proporcional_mes` boolean DEFAULT 0 NOT NULL comment 'especifica si se trata de un calculo relacionado al pago mensual o es un monto absoluto',
	`template_id` bigint NULL comment 'relacion con la tabla de templates de eventos no obligatoria',
	`activo` boolean not null comment '0 Inactivo 1 Activo', 
	`created` datetime NOT NULL,    
	`updated`  datetime NOT NULL,   
    `creator_user` BIGINT NOT NULL,     
    `updater_user` BIGINT NOT NULL,    
	`fecha_registro_historico` datetime NOT NULL,    
	PRIMARY KEY (`id`,`sociedad_id`,`fecha_registro_historico`)
)  ENGINE=InnoDB DEFAULT CHARSET=utf8 comment 'Tabla para controlar el histórico de la configuracionde los eventos base';


-- Eventos
-- es la preprogramación de lo que va a ocurrir en el momento de la nomina, controlado por la fecha
-- esto generara registros contable y se insertará en la tabla eventoslibro cuando se procese efectivamente
CREATE TABLE `Eventos` (
	`id` bigint auto_increment not NULL,
	`sociedad_id` bigint not null  comment 'sociedad a la que pertenece este eventos', -- relacionado con la tabla sociedad    		Listo           
	`tipo_evento_id` bigint NOT NULL comment 'relacion con la tabla TiposEventos', -- relacion con tipo de evento 			Listo
	`base_evento_id` bigint not NULL  comment 'relacion con la tabla EventosConfigBase',   -- relacion EventosConfigBase			Listo
	`estado_evento_id` bigint not NULL comment 'relacion con la tabla EstadosEventos',   -- relacion EstadosEvento   			Listo
	`periodo_id` bigint not NULL comment 'relacion con la tabla Periodos',   		-- relacion Periodo  	 			Listo    
	`fecha_autorizacion` datetime NULL comment 'Fecha en la que fu confiourado el evento',
	`continuo` boolean DEFAULT 0 NOT NULL comment 'define si el evento es continuo o discontinuo',
	`desde` datetime NULL comment 'fecha en la que comienza el evento',
	`hasta` datetime NULL comment 'fecha en la que termina el evento',
	`nombre_evento` text  NULL comment 'como se llama el evento',
	`observacion` text NULL comment 'cualquier descripcion adicional al evento',
	`centralizacion_id` bigint NULL comment 'relacion con la tabla Centralizaciones si aplica', -- puede o no estar relacionado con la tabla de centralizado 
	`created` datetime NOT NULL,    
	`updated`  datetime NOT NULL,   
    `creator_user` BIGINT NOT NULL,     
    `updater_user` BIGINT NOT NULL,      
	PRIMARY KEY (`id`),
    constraint `FK_Sociedad_Eventos` foreign key (`sociedad_id`) references `Sociedad` (`id`) 
    on  update cascade on delete restrict , 
    constraint `FK_TiposEvento_Eventos` foreign key (`tipo_evento_id`) references `TiposEvento` (`id`) 
    on  update cascade on delete restrict ,
    constraint `FK_EventosConfigBase_Eventos` foreign key (`base_evento_id`) references `EventosConfigBase` (`id`) 
    on  update cascade on delete restrict,
    constraint `FK_EstadosEvento_Eventos` foreign key (`estado_evento_id`) references `EstadosEvento` (`id`) 
    on  update cascade on delete restrict,
    constraint `FK_Periodos_Eventos` foreign key (`periodo_id`) references `Periodos` (`id`) 
    on  update cascade on delete restrict  
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment 'Tabla para controlar los eventos de una sociedad';


-- Historico de Eventos
CREATE TABLE `HistoricoEventos` (
	`id` bigint auto_increment not NULL,
	`sociedad_id` bigint not null  comment 'sociedad a la que pertenece este eventos',
	`tipo_evento_id` bigint NOT NULL comment 'relacion con la tabla TiposEventos', 
	`base_evento_id` bigint not NULL  comment 'relacion con la tabla EventosConfigBase',
	`estado_evento_id` bigint not NULL comment 'relacion con la tabla EstadosEventos',
	`periodo_id` bigint not NULL comment 'relacion con la tabla Periodos',
	`fecha_autorizacion` datetime NULL comment 'Fecha en la que fu confiourado el evento',
	`continuo` boolean DEFAULT 0 NOT NULL comment 'define si el evento es continuo o discontinuo',
	`desde` datetime NULL comment 'fecha en la que comienza el evento',
	`hasta` datetime NULL comment 'fecha en la que termina el evento',
	`nombre_evento` text  NULL comment 'como se llama el evento',
	`observacion` text NULL comment 'cualquier descripcion adicional al evento',
	`centralizacion_id` bigint NULL comment 'relacion con la tabla Centralizaciones si aplica',
	`created` datetime NOT NULL,    
	`updated`  datetime NOT NULL,   
    `creator_user` BIGINT NOT NULL,     
    `updater_user` BIGINT NOT NULL,      
	`fecha_historico_created` datetime NOT NULL,        
	PRIMARY KEY (`id`,`fecha_historico_created`)   
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment 'Tabla para controlar el histiro de eventos de una sociedad';

-- falta el libro de eventos, que es el detalle del pago al usuario, la ejecución del evento como tal
CREATE TABLE `LibroEventos` (
	`id` bigint auto_increment not NULL,
	`evento_id` bigint not NULL  comment 'eentocon el que esta relacionado este renglon',    
	`sociedad_id` bigint not null  comment 'sociedad a la que pertenece este eventos', 
	`tipo_evento_id` bigint NOT NULL  comment 'tipo de evento con el que está relacionado',
	`base_evento_id` bigint not NULL  comment 'EventoConfigBase con el que está relacionado',
	`estado_evento_id` bigint not NULL  comment 'estado del evento', 
	`periodo_id` bigint not NULL  comment 'periodo con el que esta relacionado', 
	`user_id` bigint not NULL  comment 'relacion con el usuario al que se le asignó el evento',     
	`monto` numeric (18,4) not NULL  comment 'monto del evento',
	`autorizado` boolean  NULL  comment 'si el evento requiere autorización se usara para verificasr si esta o no autorizado',    
	`created` datetime NOT NULL,    
	`updated`  datetime NOT NULL,   
    `creator_user` BIGINT NOT NULL,     
    `updater_user` BIGINT NOT NULL,      
	PRIMARY KEY (`id`),
    constraint `FK_Eventos_LibroEventos` foreign key (`sociedad_id`) references `Eventos` (`id`) 
    on  update cascade on delete restrict,      
    constraint `FK_Sociedad_LibroEventos` foreign key (`sociedad_id`) references `Sociedad` (`id`) 
    on  update cascade on delete restrict,    
    constraint `FK_TiposEvento_LibroEventos` foreign key (`tipo_evento_id`) references `TiposEvento` (`id`) 
    on  update cascade on delete restrict,        
    constraint `FK_EventosConfigBase_LibroEventos` foreign key (`base_evento_id`) references `EventosConfigBase` (`id`) 
    on  update cascade on delete restrict, 
    constraint `FK_EstadosEvento_LibroEventos` foreign key (`estado_evento_id`) references `EstadosEvento` (`id`) 
    on  update cascade on delete restrict,
    constraint `FK_Periodos_LibroEventos` foreign key (`periodo_id`) references `Periodos` (`id`) 
    on  update cascade on delete restrict     ,
    constraint `FK_Usuario_LibroEventos` foreign key (`user_id`) references `Usuario` (`id`) 
    on  update cascade on delete restrict      
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment 'Tabla para controlar los eventos de una sociedad';




/*CREATE TABLE B1NTesting.dbo.EventosDetalle (
	IdEvento int NOT NULL,
	UserId uniqueidentifier NOT NULL,
	Lin int NOT NULL,
	FechaCreacionReg datetime NULL,
	UserCrea uniqueidentifier NULL,
	UserUpdate uniqueidentifier NULL,
	FechaUpdate datetime NULL,
	IdCargo int NULL,
	ValorPers numeric(18,4) NULL,
	CuentaContable nvarchar(20)   NULL,
	IdGrupo int NULL,
	IdAutorizacion int NULL,
	IdEtapaAutorizacion int NULL,
	IdEstadoLinea int NULL,
	CONSTRAINT PK_LinEventosUsuario PRIMARY KEY (IdEvento,UserId,Lin)
);
ALTER TABLE B1NTesting.dbo.EventosDetalle ADD CONSTRAINT FK_EventosDetalle_AutorizacionesEtapas 
	FOREIGN KEY (IdAutorizacion,IdEtapaAutorizacion) REFERENCES B1NTesting.dbo.AutorizacionesEtapas(IdAutorizacion,IdEtapa);
ALTER TABLE B1NTesting.dbo.EventosDetalle ADD CONSTRAINT FK_EventosDetalle_EventosEstadoDetalle 
	FOREIGN KEY (IdEstadoLinea) REFERENCES B1NTesting.dbo.EventosEstadoDetalle(IdEstadoLinea);
ALTER TABLE B1NTesting.dbo.EventosDetalle ADD CONSTRAINT FK_LinEventosUsuario_EventosUsuario 
	FOREIGN KEY (IdEvento) REFERENCES B1NTesting.dbo.Eventos(IdEvento);
ALTER TABLE B1NTesting.dbo.EventosDetalle ADD CONSTRAINT FK_LinEventosUsuario_aspnet_ProfileUsers 
	FOREIGN KEY (UserId) REFERENCES B1NTesting.dbo.aspnet_ProfileUsers(UserId);
CREATE TABLE B1NTesting.dbo.EventosDetalleHistoria (
	FechaRegistro datetime NOT NULL,
	IdEvento int NOT NULL,
	UserId uniqueidentifier NOT NULL,
	Lin int NOT NULL,
	FechaCreacionReg datetime NULL,
	UserCrea uniqueidentifier NULL,
	UserUpdate uniqueidentifier NULL,
	FechaUpdate datetime NULL,
	IdCargo int NULL,
	ValorPers numeric(18,4) NULL,
	CuentaContable nvarchar(20)   NULL,
	IdGrupo int NULL,
	IdAutorizacion int NULL,
	IdEtapaAutorizacion int NULL,
	IdEstadoLinea int NULL,
	CONSTRAINT PK_LinEventosHistoria PRIMARY KEY (FechaRegistro,IdEvento,Lin)
);
CREATE TABLE B1NTesting.dbo.EventosEstadoDetalle (
	IdEstadoLinea int NOT NULL,
	EstadoLinea nvarchar(100)   NOT NULL,
	CONSTRAINT PK_EventosEstadoDetalle PRIMARY KEY (IdEstadoLinea)
);
CREATE TABLE B1NTesting.dbo.EventosHistoria (
	FechaRegistro datetime NOT NULL,
	IdEvento int NOT NULL,
	FechaCreacion datetime NOT NULL,
	UsrCreo uniqueidentifier NOT NULL,
	FechaUpdate datetime NULL,
	UsrUpdate uniqueidentifier NULL,
	IdEstadoEvento int NULL,
	UserAutoriza uniqueidentifier NULL,
	FechaAutorizacion datetime NULL,
	IdTipoEvento int NOT NULL,
	Activo bit NOT NULL,
	Continuo bit NOT NULL,
	Desde datetime NULL,
	Hasta datetime NULL,
	NombreEvento nvarchar(500)   NULL,
	IdBaseEvento int NULL,
	Observacion nvarchar(1000)   NULL,
	IdCentralización int NULL,
	PeriodosInvolucrados nvarchar(500)   NULL,
	CONSTRAINT PK_EventosHistoria PRIMARY KEY (FechaRegistro)
);CREATE TABLE B1NTesting.dbo.EventosLibro (
	IdRegistro int IDENTITY(1,1) NOT NULL,
	IdPeriodo int NOT NULL,
	IdSueldo int NOT NULL,
	UserId uniqueidentifier NOT NULL,
	TipoProceso char(1)   NULL,
	IdTipoEvento int NULL,
	Evento int NULL,
	NombreEvento nvarchar(500)   NULL,
	Prestamo int NULL,
	TipoPrestamo nvarchar(500)   NULL,
	IdInstitucionAPV int NULL,
	PagoDirectoIndirecto bit NULL,
	NombreAPV nvarchar(30)   NULL,
	CodExternoAPV nvarchar(5)   NULL,
	Monto numeric(18,4) NULL,
	MontoAPVCEmpleador numeric(18,4) NULL,
	ApvEsColectivo bit NULL,
	Regimen char(1)   NULL,
	IdConcepto int NULL,
	CONSTRAINT PK_EventosLibro PRIMARY KEY (IdRegistro,IdPeriodo,IdSueldo,UserId)
);
 CREATE NONCLUSTERED INDEX NonClusteredIndex-20200514-154241 ON dbo.EventosLibro (  IdRegistro ASC  , IdPeriodo ASC  , IdSueldo ASC  , UserId ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [PRIMARY ] ;
ALTER TABLE B1NTesting.dbo.EventosLibro ADD CONSTRAINT FK_EventosLibro_SueldoHead 
	FOREIGN KEY (IdSueldo) REFERENCES B1NTesting.dbo.SueldoHead(IdSueldo);
CREATE TABLE B1NTesting.dbo.EventosLibroHonorario (
	IdRegistro int IDENTITY(1,1) NOT NULL,
	IdPeriodo int NOT NULL,
	IdSueldoH int NOT NULL,
	UserId uniqueidentifier NOT NULL,
	TipoProceso char(1)   NULL,
	IdTipoEvento int NULL,
	Evento int NULL,
	NombreEvento nvarchar(500)   NULL,
	Prestamo int NULL,
	TipoPrestamo nvarchar(500)   NULL,
	IdInstitucionAPV int NULL,
	PagoDirectoIndirecto bit NULL,
	NombreAPV nvarchar(30)   NULL,
	CodExternoAPV nvarchar(5)   NULL,
	Monto numeric(18,4) NULL,
	CONSTRAINT PK_EventosLibroH PRIMARY KEY (IdRegistro,IdPeriodo,IdSueldoH,UserId)
);
ALTER TABLE B1NTesting.dbo.EventosLibroHonorario ADD CONSTRAINT FK_EventosLibroH_SueldosHonorariosH 
	FOREIGN KEY (IdSueldoH) REFERENCES B1NTesting.dbo.SueldosHonorariosH(IdSueldo);
CREATE TABLE B1NTesting.dbo.EventosLibroTemp (
	IdRegistro int IDENTITY(1,1) NOT NULL,
	IdPeriodo int NOT NULL,
	IdSueldo int NOT NULL,
	UserId uniqueidentifier NOT NULL,
	TipoProceso char(1)   NULL,
	IdTipoEvento int NULL,
	Evento int NULL,
	NombreEvento nvarchar(500)   NULL,
	Prestamo int NULL,
	TipoPrestamo nvarchar(500)   NULL,
	IdInstitucionAPV int NULL,
	PagoDirectoIndirecto bit DEFAULT 1 NULL,
	NombreAPV nvarchar(30)   NULL,
	CodExternoAPV nvarchar(5)   NULL,
	Monto numeric(18,4) NULL,
	MontoAPVCEmpleador numeric(18,4) NULL,
	ApvEsColectivo bit NULL,
	Regimen char(1)   NULL,
	IdConcepto int NULL,
	CONSTRAINT PK_EventosLibroTemp PRIMARY KEY (IdRegistro,IdPeriodo,IdSueldo,UserId)
);CREATE TABLE B1NTesting.dbo.EventosPeriodos (
	IdEvento int NOT NULL,
	IdPeriodo int NOT NULL,
	CONSTRAINT PK_EventosPeriodos PRIMARY KEY (IdEvento,IdPeriodo)
);
ALTER TABLE B1NTesting.dbo.EventosPeriodos ADD CONSTRAINT FK_EventosPeriodos_Eventos 
	FOREIGN KEY (IdEvento) REFERENCES B1NTesting.dbo.Eventos(IdEvento);
ALTER TABLE B1NTesting.dbo.EventosPeriodos ADD CONSTRAINT FK_EventosPeriodos_Periodos 
	FOREIGN KEY (IdPeriodo) REFERENCES B1NTesting.dbo.Periodos(IdPeriodo);
CREATE TABLE B1NTesting.dbo.EventosAutomaticos (
	IdEventoAut int NOT NULL,
	EventoAutomatico nvarchar(300)   NOT NULL,
	Activo bit DEFAULT 0 NOT NULL,
	EsProporcional bit DEFAULT 0 NOT NULL,
	Cuenta nvarchar(50)   NULL,
	MontoEvento int DEFAULT 0 NOT NULL,
	Config_1 int NULL,
	NombreConf_1 nvarchar(50)   NULL,
	Descripcion nvarchar(1000)   NULL,
	CONSTRAINT PK_EventosAutomaticos PRIMARY KEY (IdEventoAut)
);
CREATE TABLE EventosLibro (
	IdRegistro int IDENTITY(1,1) NOT NULL,
	IdPeriodo int NOT NULL,
	IdSueldo int NOT NULL,
	UserId uniqueidentifier NOT NULL,
	TipoProceso char(1) COLLATE Modern_Spanish_CI_AS NULL,
	IdTipoEvento int NULL,
	Evento int NULL,
	NombreEvento nvarchar(500) COLLATE Modern_Spanish_CI_AS NULL,
	Prestamo int NULL,
	TipoPrestamo nvarchar(500) COLLATE Modern_Spanish_CI_AS NULL,
	IdInstitucionAPV int NULL,
	PagoDirectoIndirecto bit NULL,
	NombreAPV nvarchar(30) COLLATE Modern_Spanish_CI_AS NULL,
	CodExternoAPV nvarchar(5) COLLATE Modern_Spanish_CI_AS NULL,
	Monto numeric(18,4) NULL,
	MontoAPVCEmpleador numeric(18,4) NULL,
	ApvEsColectivo bit NULL,
	Regimen char(1) COLLATE Modern_Spanish_CI_AS NULL,
	IdConcepto int NULL,
	CONSTRAINT PK_EventosLibro PRIMARY KEY (IdRegistro,IdPeriodo,IdSueldo,UserId)
);
 CREATE NONCLUSTERED INDEX NonClusteredIndex-20200514-154241 ON dbo.EventosLibro (  IdRegistro ASC  , IdPeriodo ASC  , IdSueldo ASC  , UserId ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [PRIMARY ] ;
-- B1NTesting.dbo.EventosLibro foreign keysALTER TABLE B1NTesting.dbo.EventosLibro ADD CONSTRAINT FK_EventosLibro_SueldoHead FOREIGN KEY (IdSueldo) REFERENCES B1NTesting.dbo.SueldoHead(IdSueldo);*/
select 'termine' , Now()
