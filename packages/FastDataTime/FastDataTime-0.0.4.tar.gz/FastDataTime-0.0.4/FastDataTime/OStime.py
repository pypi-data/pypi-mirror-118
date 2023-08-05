# coding=utf-8
'''
第三方库
作者：PYmili
时间：2021/8/12

'''

def OStime(time_a):
    import datetime
    import time
    if time_a == 'nyr':
        time_nyr = time.strftime("%Y/%m/%d")
        print(time_nyr)
    if time_a == '12xs':
        time_12xs = time.strftime("%I:%M:%S")
        print(time_12xs)
    if time_a == '24xs':
        time_24xs = time.strftime("%H:%M:%S")
        print(time_24xs)
    if time_a == 'jh':
        time_jh = time.strftime("%Y/%m/%d %H:%M:%S")
        print(time_jh)
    if time_a == 'm':
        m = datetime.datetime.now()
        print('%s' %m.second)
    if time_a == 'f':
        f = datetime.datetime.now()
        print('%s' %f.minute)
    if time_a == 's':
        s = datetime.datetime.now()
        print('%s' %s.hour)
    if time_a == 'r':
        rq = datetime.datetime.now()
        print('%s' %rq.day)
    if time_a == 'y':
        yf = datetime.datetime.now()
        print('%s' %yf.month)
    if time_a == 'n':
        nf = datetime.datetime.now()
        print('%s' %nf.year)
    if time_a == 'help':
        helps = ("各命令 对应各显示时间 如下：\n"\
                 "\t=============================================================="
                 "\n\t1.nyr 获取当前年月日 使用方法：time_xz('nyr')\n"\
                 "\n\t2.12xs 获取当前12小时形式的时间 使用方法：time_xz('12xs')\n"\
                 "\n\t3.24xs 获取当前24小时形式的时间 使用方法：time_xz(24xs)\n"\
                 "\n\t4.jh 获取当前年月日时分秒的时间 使用方法：time_xz(jh)\n"\
                 "\n\t5.m 获取当前时间的秒，为数字输出 使用方法：time_xz(m)\n"\
                 "\n\t6.f 获取当前时间的分，为数字输出 使用方法：time_xz(f)\n"\
                 "\n\t7.s 获取当前时间的时，为数字输出 使用方法：time_xz(s)\n"\
                 "\n\t8.r 获取当前时间的日期，为数字输出 使用方法：time_xz(r)\n"\
                 "\n\t9.y 获取当前时间的月，为数字输出 使用方法：time_xz(y)\n"\
                 "\n\t10.n 获取当前时间的年，为数字输出 使用方法：time_xz(n)\n"\
                 "\n\t剩余待完善............................................\n"\
                 "\n\t#############################################################")
        print(helps)
        print("PYmili")
        print("联系我"\
              "\n\tQQ:2097632843\n"\
              "\n\t邮件:2097632843\n")
    if time_a == '作者':
        print("PYmili")
        print("联系我"\
              "\n\tQQ:2097632843\n"\
              "\n\t邮件:2097632843\n")
