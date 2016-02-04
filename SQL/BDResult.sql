BEGIN
DROP TABLE IF EXISTS `bd_result`;
    CREATE TABLE `bd_result`(
        `bd_id` BIGINT(20) NOT NULL AUTO_INCREMENT COMMENT 'id（递增）',
        `bd_city` VARCHAR(255) NULL DEFAULT NULL COMMENT '地市',
        `bd_ip` VARCHAR(255) NULL DEFAULT NULL COMMENT 'ip',
        `bd_telnet` VARCHAR(255) NULL DEFAULT NULL COMMENT '登陆方式',
        `bd_hostname` VARCHAR(255) NULL DEFAULT NULL COMMENT 'HOSTNAME',
        `bd_devicetype` VARCHAR(255) NULL DEFAULT NULL COMMENT '设备类型',
        `bd_nBPeer` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
        `bd_nDPeer` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
        `bd_nMPeer` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
        `bd_nXPeer` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
        `bd_Error` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
        `bd_compstatus` VARCHAR(255) NULL DEFAULT NULL COMMENT '对比状态',
        `bd_projectstatus` VARCHAR(255) NULL DEFAULT NULL COMMENT '验收状态',
        `bd_comments` VARCHAR(255) NULL DEFAULT NULL COMMENT '备注',
        PRIMARY KEY(`bd_id`),
        INDEX `ind_bd_ip` (`bd_ip`)
    )
    COLLATE='utf8_general_ci'
    ENGINE=MyISAM;

    DROP TABLE IF EXISTS `bd_form`;
    CREATE TABLE `bd_form`(
    	`id` BIGINT(20) NOT NULL AUTO_INCREMENT COMMENT 'id（递增）',
    	`city` VARCHAR(255) NULL DEFAULT NULL COMMENT '地市',
    	`d_total` VARCHAR(255) NULL DEFAULT NULL COMMENT 'D设备总数',
    	`d_yiyanshou` VARCHAR(255) NULL DEFAULT NULL COMMENT 'D设备已验收数量',
    	`d_yanshoulv` VARCHAR(255) NULL DEFAULT NULL COMMENT 'D设备验收率',
    	`d_danshanglian` VARCHAR(255) NULL DEFAULT NULL COMMENT 'D设备单上联数量',
    	`d_dan_yiyanshou` VARCHAR(255) NULL DEFAULT NULL COMMENT 'D设备单上联已验收数量',
    	`b_total` VARCHAR(255) NULL DEFAULT NULL COMMENT 'B设备总数',
       	`b_yiyanshou` VARCHAR(255) NULL DEFAULT NULL COMMENT 'B设备已验收数量',
    	`b_yanshoulv` VARCHAR(255) NULL DEFAULT NULL COMMENT 'B设备验收率',
    	`b_danshanglian` VARCHAR(255) NULL DEFAULT NULL COMMENT 'B设备单上联数量',
    	`b_dan_yiyanshou` VARCHAR(255) NULL DEFAULT NULL COMMENT 'B设备单上联已验收数量',
    	PRIMARY KEY(`id`),
    	INDEX `ind_city` (`city`)
    )
    COLLATE='utf8_general_ci'
    ENGINE=MyISAM;

    -- 清空表格
    TRUNCATE TABLE bd_result;
    TRUNCATE TABLE bd_form;

    -- 将BD原始数据导入结果表
    INSERT INTO bd_result(
        bd_city,
        bd_ip,
        bd_hostname,
        bd_devicetype)
    SELECT
    b.b_area,
    b.b_yw_ip,
    b.b_hostname,
    b.b_attribute
    FROM info_b b;

    INSERT INTO bd_result(
        bd_city,
        bd_ip,
        bd_hostname,
        bd_devicetype)
    SELECT
    d.d_area,
    d.d_wg_ip,
    d.d_hostname,
    d.d_attribute
    FROM info_d d;

    -- 对区域数据做处理
    UPDATE bd_result bd
    SET bd.bd_city = SUBSTRING_INDEX(bd.bd_city,' / ',1)
    WHERE bd.bd_city REGEXP ' / ';

    -- 删除5开头的设备
    DELETE FROM bd_result
    WHERE bd_ip REGEXP '^5\.'; 

    -- 比对验收状态
    UPDATE bd_result bd
    SET
    bd.bd_projectstatus = (SELECT GROUP_CONCAT(DISTINCT(cd.project_status))
        FROM compare_device cd
        WHERE bd.bd_ip = cd.tl_ip
        GROUP BY cd.project_status);
    
    CREATE TEMPORARY TABLE IF NOT EXISTS tmp_device(
        id BIGINT(20) NOT NULL AUTO_INCREMENT PRIMARY KEY,
        ip VARCHAR(255) NULL,
        result VARCHAR(255) NULL)COLLATE='utf8_general_ci';
    TRUNCATE TABLE tmp_device;

    INSERT INTO tmp_device(ip,result)
    SELECT bd.bd_ip, cd.compare_result
    FROM compare_device cd
    LEFT JOIN bd_result bd ON bd.bd_ip = cd.tl_ip
    UNION
    SELECT bd.bd_ip,cd.compare_result
    FROM compare_device cd
    LEFT JOIN bd_result bd ON bd.bd_ip = cd.wg_ip;

    UPDATE bd_result bd
    INNER JOIN tmp_device td ON bd.bd_ip = td.ip
    SET bd.bd_compstatus = td.result;

    -- 单上联统计
    UPDATE bd_result bd
    INNER JOIN bdcsv b ON bd.bd_ip = b.LoginIp
    SET
    bd.bd_telnet = b.Telnet,
    bd.bd_nBPeer = b.nBPeer,
    bd.bd_nDPeer = b.nDPeer,
    bd.bd_nMPeer = b.nMPeer,
    bd.bd_nXPeer = b.nXPeer,
    bd.bd_Error = b.Error;

    -- 统计结果
    INSERT INTO bd_form(city) VALUES
    ('潮州'),('东莞'),('佛山'),('广州'),('河源'),('惠州'),('江门'),('揭阳'),('茂名'),('梅州'),('清远'),
    	('汕头'),('汕尾'),('韶关'),('深圳'),('阳江'),('云浮'),('湛江'),('肇庆'),('中山'),('珠海');

    UPDATE bd_form bf
    SET bf.d_total = (
    	SELECT COUNT(1) FROM bd_result br
    	WHERE br.bd_city = bf.city
    	AND br.bd_devicetype = "D-ER");

    UPDATE bd_form bf
    SET bf.d_yiyanshou = (
    	SELECT COUNT(1) FROM bd_result br
    	WHERE br.bd_city = bf.city
    	AND br.bd_devicetype = "D-ER"
    	AND br.bd_projectstatus = "已验收");

    UPDATE bd_form bf
    SET bf.d_yanshoulv = CONCAT(ROUND((bf.d_yiyanshou/bf.d_total)*100,0),'%');

    UPDATE bd_form bf
    SET bf.d_danshanglian = (
    	SELECT COUNT(1) FROM bd_result br
    	WHERE br.bd_city = bf.city
    	AND br.bd_devicetype = "D-ER"
    	AND (br.bd_Error = "Only uT" OR br.bd_Error = "Only pT"));

    UPDATE bd_form bf
    SET bf.d_dan_yiyanshou = (
    	SELECT COUNT(1) FROM bd_result br
    	WHERE br.bd_city = bf.city
    	AND br.bd_devicetype = "D-ER"
    	AND br.bd_projectstatus = "已验收"
    	AND (br.bd_Error = "Only uT" OR br.bd_Error = "Only pT"));

    UPDATE bd_form bf
    SET bf.b_total = (
    	SELECT COUNT(1) FROM bd_result br
    	WHERE br.bd_city = bf.city
    	AND br.bd_devicetype = "B网元");

    UPDATE bd_form bf
    SET bf.b_yiyanshou = (
    	SELECT COUNT(1) FROM bd_result br
    	WHERE br.bd_city = bf.city
    	AND br.bd_devicetype = "B网元"
    	AND br.bd_projectstatus = "已验收");

    UPDATE bd_form bf
    SET bf.b_yanshoulv = CONCAT(ROUND((bf.b_yiyanshou/bf.b_total)*100,0),'%');

    UPDATE bd_form bf
    SET bf.b_danshanglian = (
    	SELECT COUNT(1) FROM bd_result br
    	WHERE br.bd_city = bf.city
    	AND br.bd_devicetype = "B网元"
    	AND (br.bd_Error = "Only uT" OR br.bd_Error = "Only pT"));

    UPDATE bd_form bf
    SET bf.b_dan_yiyanshou = (
    	SELECT COUNT(1) FROM bd_result br
    	WHERE br.bd_city = bf.city
    	AND br.bd_devicetype = "B网元"
    	AND br.bd_projectstatus = "已验收"
    	AND (br.bd_Error = "Only uT" OR br.bd_Error = "Only pT"));

END