-- ===================================
-- Tabla: principal_departamento
-- ===================================
CREATE TABLE IF NOT EXISTS `principal_departamento` (
    `id_indec` VARCHAR(10) NOT NULL,
    `nombre` VARCHAR(100) NOT NULL,
    `provincia_id_indec` VARCHAR(5) NOT NULL,
    PRIMARY KEY (`id_indec`),
    INDEX `idx_provincia` (`provincia_id_indec`),
    CONSTRAINT `fk_departamento_provincia`
        FOREIGN KEY (`provincia_id_indec`) REFERENCES `principal_provincia` (`id_indec`)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ===================================
-- Tabla: principal_localidad
-- ===================================
CREATE TABLE IF NOT EXISTS `principal_localidad` (
    `id_indec` VARCHAR(15) NOT NULL,
    `nombre` VARCHAR(100) NOT NULL,
    `departamento_id_indec` VARCHAR(10) NOT NULL,
    PRIMARY KEY (`id_indec`),
    INDEX `idx_departamento` (`departamento_id_indec`),
    CONSTRAINT `fk_localidad_departamento`
        FOREIGN KEY (`departamento_id_indec`) REFERENCES `principal_departamento` (`id_indec`)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

SET FOREIGN_KEY_CHECKS = 1;
