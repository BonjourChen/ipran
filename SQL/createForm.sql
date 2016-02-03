BEGIN
    DROP TABLE IF EXISTS `info_b`;
    CREATE TABLE `info_b`(
        `b_id` BIGINT(20) NOT NULL AUTO_INCREMENT COMMENT  'B设备ID（递增）',
        `b_area` VARCHAR(255) NULL DEFAULT NULL COMMENT '区域',
        `b_attribute` VARCHAR(255) NULL DEFAULT NULL COMMENT '网元类型',
        `b_model` VARCHAR(255) NULL DEFAULT NULL COMMENT '网元型号',
        `b_hostname` VARCHAR(255) NULL DEFAULT NULL COMMENT '网元名称',
        -- `b_alias` VARCHAR(255) NULL DEFAULT NULL COMMENT '网元别名',
        `b_wg_ip` VARCHAR(255) NULL DEFAULT NULL COMMENT '网管IP',
        `b_yw_ip` VARCHAR(255) NULL DEFAULT NULL COMMENT '业务IP',
        -- `b_loopno` VARCHAR(255) NULL DEFAULT NULL COMMENT '环号',
        -- `b_config_status` VARCHAR(255) NULL DEFAULT NULL COMMENT '配置下发状态',
        `b_project_status` VARCHAR(255) NULL DEFAULT NULL COMMENT '网元运维状态',
        -- `b_isloop` VARCHAR(255) NULL DEFAULT NULL COMMENT '是否成环',
        -- `b_lock_status` VARCHAR(255) NULL DEFAULT NULL COMMENT '锁定状态',
        -- `b_service_model` VARCHAR(255) NULL DEFAULT NULL COMMENT '业务承载类型',
        PRIMARY KEY(`b_id`),
        INDEX `ind_b_hostname` (`b_hostname`),
        INDEX `ind_b_wg_ip` (`b_wg_ip`),
        INDEX `ind_b_yw_ip` (`b_yw_ip`)
    )
    COLLATE='utf8_general_ci'
    ENGINE=MyISAM;


    DROP TABLE IF EXISTS `info_d`;
    CREATE TABLE `info_d`(
        `d_id` BIGINT(20) NOT NULL AUTO_INCREMENT COMMENT  'B设备ID（递增）',
        `d_area` VARCHAR(255) NULL DEFAULT NULL COMMENT '区域',
        `d_attribute` VARCHAR(255) NULL DEFAULT NULL COMMENT '网元类型',
        `d_model` VARCHAR(255) NULL DEFAULT NULL COMMENT '网元型号',
        `d_hostname` VARCHAR(255) NULL DEFAULT NULL COMMENT '网元名称',
        -- `d_alias` VARCHAR(255) NULL DEFAULT NULL COMMENT '网元别名',
        `d_wg_ip` VARCHAR(255) NULL DEFAULT NULL COMMENT '网管IP',
        `d_yw_ip` VARCHAR(255) NULL DEFAULT NULL COMMENT '业务IP',
        -- `d_loopno` VARCHAR(255) NULL DEFAULT NULL COMMENT '环号',
        -- `d_config_status` VARCHAR(255) NULL DEFAULT NULL COMMENT '配置下发状态',
        `d_project_status` VARCHAR(255) NULL DEFAULT NULL COMMENT '网元运维状态',
        -- `d_isloop` VARCHAR(255) NULL DEFAULT NULL COMMENT '是否成环',
        -- `d_lock_status` VARCHAR(255) NULL DEFAULT NULL COMMENT '锁定状态',
        -- `d_service_model` VARCHAR(255) NULL DEFAULT NULL COMMENT '业务承载类型',
        PRIMARY KEY(`d_id`),
        INDEX `ind_d_hostname` (`d_hostname`),
        INDEX `ind_d_wg_ip` (`d_wg_ip`),
        INDEX `ind_d_yw_ip` (`d_yw_ip`)
    )
    COLLATE='utf8_general_ci'
    ENGINE=MyISAM;

    DROP TABLE IF EXISTS `compare_device`;
    CREATE TABLE `compare_device`(
        `compare_id` BIGINT(20) NOT NULL AUTO_INCREMENT COMMENT '',
        `compare_result` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
        `wg_ems` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
        `tl_ems` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
        `wg_ip` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
        `tl_ip` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
        `project_status` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
        `use_status` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
        `compare_reason` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
        PRIMARY KEY(`compare_id`),
        INDEX `ind_compare_result` (`compare_result`),
        INDEX `ind_wg_ems` (`wg_ems`),
        INDEX `ind_tl_ems` (`tl_ems`),
        INDEX `ind_wg_ip` (`wg_ip`),
        INDEX `ind_tl_ip` (`tl_ip`),
        INDEX `ind_project_status` (`project_status`),
        INDEX `ind_use_status` (`use_status`)
    )
    COLLATE='utf8_general_ci'
    ENGINE=MyISAM;

    DROP TABLE IF EXISTS `bdcsv`;
    CREATE TABLE `bdcsv`(
        `id` BIGINT(20) NOT NULL AUTO_INCREMENT COMMENT '',
        `LoginIp` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
        `Telnet` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
        `HostName` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
        `DeviceType` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
        `nBPeer` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
        `nDPeer` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
        `nMPeer` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
        `nXPeer` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
        `Error` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
        PRIMARY KEY(`id`),
        INDEX `ind_loginIp` (`LoginIp`)
    )
    COLLATE='utf8_general_ci'
    ENGINE=MyISAM;

    DROP TABLE IF EXISTS `bdcsv_err`;
    CREATE TABLE `bdcsv_err`(
        `id` BIGINT(20) NOT NULL AUTO_INCREMENT COMMENT '',
        `LoginIp` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
        -- `Telnet` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
        -- `HostName` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
        -- `DeviceType` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
        -- `nBPeer` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
        -- `nDPeer` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
        -- `nMPeer` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
        -- `nXPeer` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
        `Status` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
        PRIMARY KEY(`id`),
        INDEX `ind_loginIp` (`LoginIp`)
    )
    COLLATE='utf8_general_ci'
    ENGINE=MyISAM;

    DROP TABLE IF EXISTS `bdcsv_previous`;
    CREATE TABLE `bdcsv_previous`(
        `id` BIGINT(20) NOT NULL AUTO_INCREMENT COMMENT '',
        `LoginIp` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
        `Telnet` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
        `HostName` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
        `DeviceType` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
        `nBPeer` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
        `nDPeer` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
        `nMPeer` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
        `nXPeer` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
        `Error` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
        PRIMARY KEY(`id`),
        INDEX `ind_loginIp` (`LoginIp`)
    )
    COLLATE='utf8_general_ci'
    ENGINE=MyISAM;

    DROP TABLE IF EXISTS `errlist`;
    CREATE TABLE `errlist`(
        `id` BIGINT(20) NOT NULL AUTO_INCREMENT COMMENT '',
        `LoginIp` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
        `HostName` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
        `Reason` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
        PRIMARY KEY(`id`),
        INDEX `ind_loginIp` (`LoginIp`)
    )
    COLLATE='utf8_general_ci'
    ENGINE=MyISAM;
END