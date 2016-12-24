CREATE TABLE `running_log` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `_last_modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `date` datetime DEFAULT NULL,
  `miles` float DEFAULT NULL,
  `minutes` float DEFAULT NULL,
  `feeling` int(11) DEFAULT NULL,
  `extras` int(11) DEFAULT NULL,
  `description` text,
  `terrain` varchar(50) DEFAULT NULL,
  `course` int(11) DEFAULT NULL,
  `course_description` text,
  `miles_approx` int(11) DEFAULT NULL,
  `minutes_approx` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq1` (`date`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;