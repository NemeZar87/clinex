SET FOREIGN_KEY_CHECKS = 0;

-- ===================================
-- Tabla: principal_provincia
-- ===================================
CREATE TABLE IF NOT EXISTS `principal_provincia` (
    `id_indec` VARCHAR(25) NOT NULL,
    `nombre` VARCHAR(100) NOT NULL,
    PRIMARY KEY (`id_indec`),
    UNIQUE KEY (`nombre`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ===================================
-- Tabla: principal_departamento
-- ===================================
CREATE TABLE IF NOT EXISTS `principal_departamento` (
    `id_indec` VARCHAR(25) NOT NULL,
    `nombre` VARCHAR(100) NOT NULL,
    `provincia_id` VARCHAR(25) NOT NULL,
    PRIMARY KEY (`id_indec`),
    UNIQUE KEY `uq_nombre_provincia` (`nombre`, `provincia_id`),
    CONSTRAINT `fk_departamento_provincia`
        FOREIGN KEY (`provincia_id`) REFERENCES `principal_provincia` (`id_indec`)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ===================================
-- Tabla: principal_localidad
-- ===================================
CREATE TABLE IF NOT EXISTS `principal_localidad` (
    `id_indec` VARCHAR(25) NOT NULL,
    `nombre` VARCHAR(100) NOT NULL,
    `departamento_id` VARCHAR(25) NOT NULL,
    PRIMARY KEY (`id_indec`),
    UNIQUE KEY `uq_nombre_departamento` (`nombre`, `departamento_id`),
    CONSTRAINT `fk_localidad_departamento`
        FOREIGN KEY (`departamento_id`) REFERENCES `principal_departamento` (`id_indec`)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SET FOREIGN_KEY_CHECKS = 1;