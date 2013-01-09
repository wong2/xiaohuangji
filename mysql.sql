CREATE TABLE `question_and_answers` (
 `id` bigint(11) NOT NULL AUTO_INCREMENT,
 `question` text COLLATE utf8_bin NOT NULL,
 `answer` text COLLATE utf8_bin NOT NULL,
 `worker` varchar(256) COLLATE utf8_bin NOT NULL,
 `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
 PRIMARY KEY (`id`),
 KEY `time` (`time`),
 KEY `worker` (`worker`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
