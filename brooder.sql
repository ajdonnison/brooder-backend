DROP TABLE IF EXISTS `config`;
CREATE TABLE `config` (
  `temp_high` FLOAT,
  `temp_low` FLOAT,
  `hysterisis` FLOAT,
  `reference` INTEGER NOT NULL DEFAULT 0,
  `time_start` TIME,
  `time_end` TIME,
  `cycle_offset` INTEGER NOT NULL DEFAULT 0,
  `ramp_factor` FLOAT
);

DROP TABLE IF EXISTS `brooder`;
CREATE TABLE `brooder` (
  `id` INTEGER NOT NULL auto_increment,
  `name` VARCHAR(32) NOT NULL DEFAULT '',
  `sensor` INTEGER NOT NULL DEFAULT 0,
  `light` TINYINT NOT NULL DEFAULT 0,
  `heater` TINYINT NOT NULL DEFAULT 0,
  `light_state` TINYINT NOT NULL DEFAULT 0,
  `heater_state` TINYINT NOT NULL DEFAULT 0,
  `set_temperature` FLOAT,
  `enabled` TINYINT NOT NULL DEFAULT 0,
  `cycle_enabled` TINYINT NOT NULL DEFAULT 0,
  `cycle_started` DATETIME,
  PRIMARY KEY (`id`)
);

DROP TABLE IF EXISTS `sensor`;
CREATE TABLE `sensor` (
  `id` INTEGER NOT NULL auto_increment,
  `busid` VARCHAR(16) NOT NULL,
  `value` FLOAT,
  `last_checked` TIMESTAMP,
  PRIMARY KEY (`id`)
);

DROP TABLE IF EXISTS `readings`;
CREATE TABLE `readings` (
  `sensor` INTEGER NOT NULL DEFAULT 0,
  `taken` TIMESTAMP,
  `value` FLOAT,
  KEY (`sensor`, `taken`)
);

INSERT INTO `sensor` (`id`, `busid`)
VALUES
(1, '28-000004c94cc7'),
(2, '28-000004e1b806'),
(3, '28-000004c8f612'),
(4, '28-00000498251a'),
(5, '28-000004986777');

INSERT INTO `brooder` (`id`, `name`, `sensor`, `light`, `heater`, `enabled`, `cycle_started`)
VALUES
(1, 'Top', 2, 22, 18, 1, '2000-01-01 00:00:00'),
(2, 'Second', 3, 5, 24, 1, '2000-01-01 00:00:00'),
(3, 'Third', 4, 27, 12, 1, '2000-01-01 00:00:00'),
(4, 'Bottom', 5, 17, 23, 1, '2000-01-01 00:00:00');

DELETE FROM `config`;
INSERT INTO `config` (`temp_high`, `temp_low`, `hysterisis`, `reference`, `time_start`, `time_end`, `cycle_offset`, `ramp_factor`)
VALUES (36.5, 15, 0.5, 1, '07:00:00', '19:30:00', 4, 0.5);
