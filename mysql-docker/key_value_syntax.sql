CREATE TABLE `key_values` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `_last_modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `field_key` int(11) DEFAULT NULL,
  `field_value` varchar(200) DEFAULT NULL,
  `field` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq1` (`field`,`field_key`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;