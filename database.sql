-- FVK - Esquema inicial para MariaDB
-- Compatible con Django 5.x y los modelos del proyecto.
-- Uso: mysql -u root -p < database.sql

CREATE DATABASE IF NOT EXISTS `fvk_db`
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
USE `fvk_db`;

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `competencia_puntuacion`, `competencia_inscripcion`, `competencia_categoria`, `competencia_evento`;
DROP TABLE IF EXISTS `deporte_arbitro`, `deporte_atleta`, `deporte_club`, `deporte_asociacion`;
DROP TABLE IF EXISTS `cms_contactmessage`, `cms_galeriaimagen`, `cms_album`, `cms_emailsetting`, `cms_sitesetting`;
DROP TABLE IF EXISTS `django_admin_log`, `django_session`, `django_migrations`;
DROP TABLE IF EXISTS `auth_user_groups`, `auth_user_user_permissions`, `auth_group_permissions`;
DROP TABLE IF EXISTS `auth_user`, `auth_group`, `auth_permission`, `django_content_type`;

CREATE TABLE `django_content_type` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_uniq` (`app_label`,`model`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `auth_permission` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` bigint NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_codename_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_fk` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_name_uniq` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_permission_uniq` (`group_id`,`permission_id`),
  CONSTRAINT `auth_group_permissions_group_fk` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_group_permissions_permission_fk` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_username_uniq` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_group_uniq` (`user_id`,`group_id`),
  CONSTRAINT `auth_user_groups_user_fk` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `auth_user_groups_group_fk` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_permission_uniq` (`user_id`,`permission_id`),
  CONSTRAINT `auth_user_user_permissions_user_fk` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `auth_user_user_permissions_permission_fk` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` bigint NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_idx` (`content_type_id`),
  KEY `django_admin_log_user_idx` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_fk` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_fk` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_idx` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `cms_sitesetting` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `sitio_nombre` varchar(180) NOT NULL DEFAULT 'Federación Venezolana de Kenpo',
  `logo` varchar(100) NULL,
  `fondo_pantalla` varchar(100) NULL,
  `color_primario_start` varchar(7) NOT NULL DEFAULT '#003366',
  `color_primario_end` varchar(7) NOT NULL DEFAULT '#0066cc',
  `email_contacto` varchar(254) NOT NULL,
  `telefono_contacto` varchar(40) NOT NULL,
  `direccion` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `cms_emailsetting` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `smtp_host` varchar(180) NOT NULL DEFAULT 'smtp.gmail.com',
  `smtp_port` int unsigned NOT NULL DEFAULT 587,
  `smtp_user` varchar(254) NOT NULL,
  `smtp_password` varchar(255) NOT NULL,
  `smtp_use_tls` tinyint(1) NOT NULL DEFAULT 1,
  `from_email` varchar(254) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `cms_album` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `titulo` varchar(160) NOT NULL,
  `descripcion` longtext NOT NULL,
  `fecha` date NOT NULL,
  `activo` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `cms_galeriaimagen` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `imagen` varchar(100) NOT NULL,
  `titulo` varchar(160) NOT NULL,
  `descripcion` varchar(255) NOT NULL,
  `creada` datetime(6) NOT NULL,
  `album_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `cms_galeriaimagen_album_idx` (`album_id`),
  CONSTRAINT `cms_galeriaimagen_album_fk` FOREIGN KEY (`album_id`) REFERENCES `cms_album` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `cms_contactmessage` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(120) NOT NULL,
  `telefono` varchar(40) NOT NULL,
  `email` varchar(254) NOT NULL,
  `edad` smallint unsigned NULL,
  `ciudad` varchar(100) NOT NULL,
  `asunto` varchar(180) NOT NULL,
  `mensaje` longtext NOT NULL,
  `creado` datetime(6) NOT NULL,
  `atendido` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `deporte_asociacion` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(160) NOT NULL,
  `estado` varchar(80) NOT NULL,
  `presidente` varchar(140) NOT NULL,
  `telefono` varchar(40) NOT NULL,
  `email` varchar(254) NOT NULL,
  `logo` varchar(100) NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `deporte_club` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(160) NOT NULL,
  `entrenador_principal` varchar(140) NOT NULL,
  `ciudad_municipio` varchar(100) NOT NULL,
  `asociacion_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `deporte_club_asociacion_idx` (`asociacion_id`),
  CONSTRAINT `deporte_club_asociacion_fk` FOREIGN KEY (`asociacion_id`) REFERENCES `deporte_asociacion` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `deporte_atleta` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombres` varchar(100) NOT NULL,
  `apellidos` varchar(100) NOT NULL,
  `cedula` varchar(30) NOT NULL,
  `fecha_nacimiento` date NOT NULL,
  `sexo` varchar(1) NOT NULL,
  `cinturon_kyu` varchar(80) NOT NULL,
  `fotografia` varchar(100) NULL,
  `activo` tinyint(1) NOT NULL,
  `club_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `deporte_atleta_cedula_uniq` (`cedula`),
  KEY `deporte_atleta_club_idx` (`club_id`),
  CONSTRAINT `deporte_atleta_club_fk` FOREIGN KEY (`club_id`) REFERENCES `deporte_club` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `deporte_arbitro` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombres` varchar(100) NOT NULL,
  `apellidos` varchar(100) NOT NULL,
  `cedula` varchar(30) NOT NULL,
  `nivel_rango` varchar(100) NOT NULL,
  `estado` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `deporte_arbitro_cedula_uniq` (`cedula`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `competencia_evento` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(180) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `sede_lugar` varchar(180) NOT NULL,
  `estado` varchar(80) NOT NULL,
  `estatus` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `competencia_categoria` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(140) NOT NULL,
  `modalidad` varchar(20) NOT NULL,
  `edad_min` smallint unsigned NOT NULL,
  `edad_max` smallint unsigned NOT NULL,
  `sexo` varchar(20) NOT NULL,
  `rango_cintas` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `competencia_inscripcion` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creada` datetime(6) NOT NULL,
  `evento_id` bigint NOT NULL,
  `atleta_id` bigint NOT NULL,
  `categoria_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_evento_atleta_categoria` (`evento_id`,`atleta_id`,`categoria_id`),
  KEY `competencia_inscripcion_atleta_idx` (`atleta_id`),
  KEY `competencia_inscripcion_categoria_idx` (`categoria_id`),
  CONSTRAINT `competencia_inscripcion_evento_fk` FOREIGN KEY (`evento_id`) REFERENCES `competencia_evento` (`id`),
  CONSTRAINT `competencia_inscripcion_atleta_fk` FOREIGN KEY (`atleta_id`) REFERENCES `deporte_atleta` (`id`),
  CONSTRAINT `competencia_inscripcion_categoria_fk` FOREIGN KEY (`categoria_id`) REFERENCES `competencia_categoria` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `competencia_puntuacion` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `ronda` smallint unsigned NOT NULL,
  `puntos` decimal(5,2) NOT NULL,
  `total` decimal(7,2) NOT NULL DEFAULT 0.00,
  `creada` datetime(6) NOT NULL,
  `inscripcion_id` bigint NOT NULL,
  `juez_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `competencia_puntuacion_inscripcion_idx` (`inscripcion_id`),
  KEY `competencia_puntuacion_juez_idx` (`juez_id`),
  CONSTRAINT `competencia_puntuacion_inscripcion_fk` FOREIGN KEY (`inscripcion_id`) REFERENCES `competencia_inscripcion` (`id`),
  CONSTRAINT `competencia_puntuacion_juez_fk` FOREIGN KEY (`juez_id`) REFERENCES `deporte_arbitro` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SET FOREIGN_KEY_CHECKS = 1;

-- Django llenará django_content_type, permisos y django_migrations al ejecutar:
-- python manage.py migrate
