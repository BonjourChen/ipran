BEGIN
    -- 先清空表格
    TRUNCATE TABLE info_b;
    TRUNCATE TABLE info_d;
    TRUNCATE TABLE bdcsv;

    -- 将info_all表中的数据分拆出info_b分拆进info_d
    INSERT INTO info_b
    (   
        b_area,
        b_attribute,
        b_model,
        b_hostname,
        b_wg_ip,
        b_yw_ip,
        b_project_status)
    SELECT ia.area,
        ia.attribute,
        ia.model,
        ia.hostname,
        ia.wg_ip,
        ia.yw_ip,
        ia.project_status
    FROM info_all ia
    WHERE ia.attribute = "B网元";

    INSERT INTO info_d
    (   
        d_area,
        d_attribute,
        d_model,
        d_hostname,
        d_wg_ip,
        d_yw_ip,
        d_project_status)
    SELECT ia.area,
        ia.attribute,
        ia.model,
        ia.hostname,
        ia.wg_ip,
        ia.yw_ip,
        ia.project_status
    FROM info_all ia
    WHERE ia.attribute = "D-ER";

    -- 将结果中的IP包含5开头的都去掉（不统计）
    DELETE FROM info_b
    WHERE info_b.b_wg_ip REGEXP '^5\.'; 

    DELETE FROM info_d
    WHERE info_d.d_wg_ip REGEXP '^5\.'; 

    -- 插入进bdcsv中
    INSERT INTO bdcsv(
        LoginIp)
    SELECT ib.b_yw_ip
    FROM info_b ib;

    INSERT INTO bdcsv(
        LoginIp)
    SELECT id.d_wg_ip
    FROM info_d id;
END