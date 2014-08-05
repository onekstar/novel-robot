BEGIN;
CREATE TABLE `Novel` (
    `id` varchar(32) NOT NULL PRIMARY KEY,
    `name` varchar(255) NOT NULL UNIQUE,
    `create` integer UNSIGNED NOT NULL,
    `update` integer UNSIGNED NOT NULL,
    `status` smallint NOT NULL
)
ENGINE=InnoDB DEFAULT CHARSET=utf8
;
CREATE INDEX `novel_name` ON `Novel` (`name`);
CREATE INDEX `novel_create` ON `Novel` (`create`);
CREATE INDEX `novel_update` ON `Novel` (`update`);
CREATE INDEX `novel_status` ON `Novel` (`status`);
COMMIT;
