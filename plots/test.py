# -*- coding:utf-8 -*-
"""
author: Luke
datettime: 2020/3/23 23:14
"""
from django.contrib.auth.models import User

users = ['zhuxiao',
         'jianghongzhao',
         'gaominrui',
         'liuzhengjun',
         'chenlong',
         'tangjin',
         'nitonglei',
         'cailei',
         'hewei',
         'chenchunxing',
         'dengxiaoyu',
         'chenchen',
         'xulianlian',
         'zhangzhuhua',
         'liangxingguang',
         'xufuli',
         'xingfeifan',
         'wangxiaowei',
         'zhangtao',
         'fengyafen',
         'zhangxiaowang',
         'renyingjie',
         'daizeliang',
         'wangyong',
         'songchen',
         'gongrui',
         'huangyouhua',
         'chenjinghui',
         'chenruijin',
         'wuyuebo',
         'zhangjianjun',
         'zhangfengfeng',
         'chenjiajun',
         'wantongji',
         'hefei']

for user in users:
    User.objects.create_user(user, password=user)
    # user.save()


'''
create table appraisal.data as 
select username, rp.score point, ra.score score, rec_month date from ecology.report_points rp
join (select bs_loginid,txrq,sum(score_w) score from ecology.report_appraise 
group by bs_loginid,txrq
) ra
on ra.bs_loginid = rp.username
'''