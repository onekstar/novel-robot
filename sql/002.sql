BEGIN;
CREATE TABLE `Chapter` (
    `id` varchar(32) NOT NULL PRIMARY KEY,
    `novel` varchar(32) NOT NULL,
    `title` varchar(255) NOT NULL,
    `pageid` varchar(32) NOT NULL,
    `createtime` integer UNSIGNED NOT NULL,
    `updatetime` integer UNSIGNED NOT NULL,
    `status` smallint NOT NULL,
    `content` text
)
ENGINE=InnoDB DEFAULT CHARSET=utf8
;
CREATE INDEX `chapter_novel` ON `Chapter` (`novel`);
CREATE INDEX `chapter_title` ON `Chapter` (`title`);
CREATE INDEX `chapter_create` ON `Chapter` (`createtime`);
CREATE INDEX `chapter_update` ON `Chapter` (`updatetime`);
CREATE INDEX `chapter_status` ON `Chapter` (`status`);
COMMIT;
