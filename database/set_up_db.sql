CREATE TABLE `data_raw` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `obj_num` int(4) unsigned DEFAULT NULL,
  `dt` datetime DEFAULT NULL COMMENT 'Время передачи данных в контроллере',
  `dt_0` datetime DEFAULT current_timestamp() COMMENT 'Время записи данных в БД',
  `text` varchar(600) DEFAULT NULL COMMENT 'Данные (строка)',
  PRIMARY KEY (`id`)
) COMMENT='json данные с контроллера\r\n';

CREATE TABLE `emergency` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `obj_num` int(11) NOT NULL,
  `dt` datetime NOT NULL,
  `dt_0` datetime DEFAULT current_timestamp(),
  `c1` int(11) unsigned DEFAULT NULL COMMENT 'Аварийные данные с Micom',
  `c2` int(11) unsigned DEFAULT NULL,
  `c3` int(11) unsigned DEFAULT NULL,
  `c4` int(11) unsigned DEFAULT NULL,
  `c5` int(11) unsigned DEFAULT NULL,
  `c6` int(11) unsigned DEFAULT NULL,
  `c7` int(11) unsigned DEFAULT NULL,
  `c8` int(11) unsigned DEFAULT NULL,
  `c9` int(11) unsigned DEFAULT NULL,
  `c10` int(11) unsigned DEFAULT NULL,
  `c11` int(11) unsigned DEFAULT NULL,
  `c12` int(11) unsigned DEFAULT NULL,
  `c13` int(11) unsigned DEFAULT NULL,
  `c14` int(11) unsigned DEFAULT NULL,
  `c15` int(11) unsigned DEFAULT NULL,
  `c16` int(11) unsigned DEFAULT NULL,
  `c17` int(11) unsigned DEFAULT NULL,
  `c18` int(11) unsigned DEFAULT NULL,
  `c19` int(11) unsigned DEFAULT NULL,
  `c20` int(11) unsigned DEFAULT NULL,
  `c21` int(11) unsigned DEFAULT NULL,
  `c22` int(11) unsigned DEFAULT NULL,
  `c23` int(11) unsigned DEFAULT NULL,
  `c24` int(11) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`)
) COMMENT='Аварийные данные';

CREATE TABLE `general` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `obj_num` int(4) unsigned NOT NULL COMMENT 'Номер объекта',
  `dt` datetime DEFAULT NULL COMMENT 'Время записи контроллера',
  `dt_0` datetime DEFAULT current_timestamp() COMMENT 'Время записи сервера',
  `vp` float DEFAULT NULL COMMENT 'Напряжение питания контроллера',
  `t_air` float DEFAULT NULL COMMENT 'Темперптура в шкафу',
  `t_cpu` float DEFAULT NULL COMMENT 'Темперптура контроллера',
  `stat` int(11) DEFAULT 0 COMMENT 'Состояние контроллера (Биты)',
  `reset` int(8) DEFAULT NULL COMMENT 'Кол-во рестартов контроллера',
  `cicle` int(4) DEFAULT NULL COMMENT 'Цикл (мин) опроса параметров',
  PRIMARY KEY (`id`)
) COMMENT='Параметры контроллера';

CREATE TABLE `obj_table` (
  `obj_num` int(11) NOT NULL COMMENT 'Номер объекта',
  `obj_name` varchar(64) DEFAULT NULL COMMENT 'Название объекта',
  `obj_conf` varchar(200) DEFAULT NULL COMMENT 'Конфигурация контроллера',
  `obj_dev` varchar(200) DEFAULT NULL COMMENT 'Адреса девайсов (DI32,Micom)',
  `obj_reg` varchar(200) DEFAULT NULL COMMENT 'Адреса регистров опроса Micom',
  PRIMARY KEY (`obj_num`)
) COMMENT='Данные по объекту\r\n';

CREATE TABLE `regular` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `obj_num` int(4) NOT NULL,
  `dt` datetime NOT NULL,
  `dt_0` datetime NOT NULL DEFAULT current_timestamp(),
  `cell_number` int(11) DEFAULT NULL COMMENT 'Номер ячейки с данными',
  `avr` int(4) DEFAULT NULL,
  `0030` int(11) DEFAULT NULL COMMENT 'Данные с регистров Mocom (по HEX  адресу)',
  `0031` int(11) DEFAULT NULL,
  `0032` int(11) DEFAULT NULL,
  `0033` int(11) DEFAULT NULL,
  `0034` int(11) DEFAULT NULL,
  `0035` int(11) DEFAULT NULL,
  `0036` int(11) DEFAULT NULL,
  `0037` int(11) DEFAULT NULL,
  `003B` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) COMMENT='Регулярные данные';

CREATE TABLE `tx_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `obj_num` int(10) unsigned DEFAULT NULL COMMENT 'Номер объекта',
  `str_tx` text DEFAULT NULL COMMENT 'Строка для передачи в контроллер',
  `dt_1` datetime DEFAULT current_timestamp() COMMENT 'Время формирования строки',
  `dt_2` datetime DEFAULT NULL COMMENT 'Время отправления строки в контроллер',
  PRIMARY KEY (`id`)
) COMMENT='Передача строк конфигурации в контроллер на объекте obj_num';
