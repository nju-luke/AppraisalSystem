
## 生成测试展示数据
create table ecology.report_appraise_dtl as
SELECT
	max(txrq) txrq,
    avg(f1) f1,
	avg(f2) f2,
	avg(f3) f3,
	avg(f4) f4,
	avg(f5) f5,
	avg(f6) f6,
	avg(f7) f7,
	avg(f8) f8,
	avg(f9) f9,
	avg(f10) f10,
	avg(f11) f11,
    avg(score) score,
    max(bsbtpr) bsbtpr,
    max(bs_loginid) bs_loginid,
    max(bs_name) bs_name,
    (rand() > 0.5) + 6 e_type
FROM ecology.appraise_dtl
group by bs_name
;

select * from ecology.report_appraise_dtl;

## 添加一个月的数据
insert into ecology.report_appraise_dtl
SELECT
	'2020-04' txrq,
    f1 f1,
	f2 f2,
	f3 f3,
	f4 f4,
	f5 f5,
	f6 f6,
	f7 f7,
	f8 f8,
	f9 f9,
	f10 f10,
	f11 f11,
    score score,
    bsbtpr bsbtpr,
    bs_loginid bs_loginid,
    bs_name bs_name,
    e_type etype
FROM ecology.report_appraise_dtl
;


            select username,
                f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,
                point,
                score,
                bs_name
            from ecology.report_appraise_dtl rad
            left join ecology.report_points rp
            on rad.bs_loginid = rp.username
--            where rad.txrq='{month}' and rp.rec_month='{month}';





