# coding=utf-8
'''
time_xzsj 第三方库
作者：PYmili
时间：2021/8/12

'''
#print ("格式参数：")
#print (" %a  星期几的简写")
#print (" %A  星期几的全称")
#print (" %b  月分的简写")
#print (" %B  月份的全称")
#print (" %c  标准的日期的时间串")
#print (" %C  年份的后两位数字")
#print (" %d  十进制表示的每月的第几天")
#print (" %D  月/天/年")
#print (" %e  在两字符域中，十进制表示的每月的第几天")
#print (" %F  年-月-日")
#print (" %g  年份的后两位数字，使用基于周的年")
#print (" %G  年分，使用基于周的年")
#print (" %h  简写的月份名")
#print (" %H  24小时制的小时")
#print (" %I  12小时制的小时")
#print (" %j  十进制表示的每年的第几天")
#print (" %m  十进制表示的月份")
#print (" %M  十时制表示的分钟数")
#print (" %n  新行符")
#print (" %p  本地的AM或PM的等价显示")
#print (" %r  12小时的时间")
#print (" %R  显示小时和分钟：hh:mm")
#print (" %S  十进制的秒数")
#print (" %t  水平制表符")
#print (" %T  显示时分秒：hh:mm:ss")
#print (" %u  每周的第几天，星期一为第一天 （值从0到6，星期一为0）")
#print (" %U  第年的第几周，把星期日做为第一天（值从0到53）")
#print (" %V  每年的第几周，使用基于周的年")
#print (" %w  十进制表示的星期几（值从0到6，星期天为0）")
#print (" %W  每年的第几周，把星期一做为第一天（值从0到53）")
#print (" %x  标准的日期串")
#print (" %X  标准的时间串")
#print (" %y  不带世纪的十进制年份(值从0到99)")
#print (" %Y  带世纪部分的十制年份")
#print (" %z,%Z   时区名称，如果不能得到时区名称则返回空字符。")
#print (" %%  百分号")
#
#print ("----------------------------------------------------------")
#print ("python里使time模块来获取当前的时间")


#print ("24小时格式：" + time.strftime("%H:%M:%S"))
#print ("12小时格式：" + time.strftime("%I:%M:%S"))
#print ("今日的日期：" + time.strftime("%d/%m/%Y"))

#print ("----------------------------------------------------------")

#print ("使用datetime模块来获取当前的日期和时间")

#i = datetime.datetime.now()
#print ("当前的日期和时间是 %s" % i)
#print ("ISO格式的日期和时间是 %s" % i.isoformat() )
#print ("当前的年份是 %s" %i.year)
#print ("当前的月份是 %s" %i.month)
#print ("当前的日期是  %s" %i.day)
#print ("dd/mm/yyyy 格式是  %s/%s/%s" % (i.day, i.month, i.year) )
#print ("当前小时是 %s" %i.hour)
#print ("当前分钟是 %s" %i.minute)
#print ("当前秒是  %s" %i.second)

def time_xz(time_a):
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
