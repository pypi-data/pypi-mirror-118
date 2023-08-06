# coding:utf-8
'''
第三方库
作者：PYmili
时间：2021/8/12

'''
def OStime(time_a):
    import datetime
    from datetime import datetime
    import time
    import random
    import pytz
    import timezones
    from dateutil import tz
    import re
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
                 "\n\t1.nyr 获取当前年月日 使用方法：OStime('nyr')\n"\
                 "\n\t2.12xs 获取当前12小时形式的时间 使用方法：OStime('12xs')\n"\
                 "\n\t3.24xs 获取当前24小时形式的时间 使用方法：OStime('24xs')\n"\
                 "\n\t4.jh 获取当前年月日时分秒的时间 使用方法：OStime('jh')\n"\
                 "\n\t5.m 获取当前时间的秒，为数字输出 使用方法：OStime('m')\n"\
                 "\n\t6.f 获取当前时间的分，为数字输出 使用方法：OStime('f')\n"\
                 "\n\t7.s 获取当前时间的时，为数字输出 使用方法：OStime('s')\n"\
                 "\n\t8.r 获取当前时间的日期，为数字输出 使用方法：OStime('r')\n"\
                 "\n\t9.y 获取当前时间的月，为数字输出 使用方法：OStime('y')\n"\
                 "\n\t10.n 获取当前时间的年，为数字输出 使用方法：OStime('n')\n"\
                 "\n\t11.Beijing_time 获取当前北京时间，数字输出 使用方法:OStime('Beijing_time')\n"\
                 "\n\t12.GMT-8-Time_MS 获取GMT-8毫秒时间，数字输出 使用方法：OStime('GMT-8-Time_MS') 时间间隔1000ms\n"\
                 "\n\t13.Running_time 获取程序运行时间（有误差），数字输出 使用方法：OStime('Running_time')\n"\
                 "\n\t剩余待完善............................................\n"\
                 "\n\t#############################################################")
        help_yw = ("The display time corresponding to each command is as follows:\n"\
                   "\t=============================================================="
                   "\n\t1.nyr get the current month, year and day. Usage: OStime('nyr')\n"\
                   "\n\t2.12xs get the current 12 hour time usage: OStime('12xs')\n"\
                   "\n\t3.24xs get the current 24-hour time usage method: OStime('24xs')\n"\
                   "\n\t4.jh get the time of the current month, year, day, hour, minute and second. Usage: OStime('jh')\n"\
                   "\n\t5. m get the second of the current time, which is digital output. Usage: OStime('m')\n"\
                   "\n\t6. f get the minute of the current time, which is digital output. Usage: OStime('f')\n"\
                   "\n\t7. s when obtaining the current time, it is used for digital output. Method: OStime('s')\n"\
                   "\n\t8. r get the date of the current time for digital output. Usage: OStime('r')\n"\
                   "\n\t9. y get the month of the current time, which is digital output. Usage: OStime('y')\n"\
                   "\n\t10. n get the year of the current time, which is digital output. Usage: OStime('n')\n"\
                   "\n\t11.Beijing_time to obtain the current Beijing time. How to use digital output: OStime('Beijing_time')\n"\
                   "\n\t12.GMT-8-Time_MS obtains GMT-8 ms time, and the digital output method is OStime('GMT-8-Time_MS') interval 1000ms\n"\
                   "\n\t13.Running_time to obtain the running time of the program (with error). How to use digital output: OStime('Running_time')\n"\
                   "\n\t remaining to be improved......................................... \n"\
                   "\n\t#############################################################")

        print(helps)
        print("PYmili")
        print("联系我"\
              "\n\tQQ:2097632843\n"\
              "\n\t邮件:mc2005wj@163.com\n")

        print("\n")
        print(help_yw)
        print("PYmili")
        print("Contact me"\
              "\n\tQQ:2097632843\n"\
              "\n\tmessage: mc2005wj@163.com\n")

    if time_a == '作者':
        print("PYmili")
        print("联系我"\
              "\n\tQQ:2097632843\n"\
              "\n\tmail:mc2005wj@163.com\n")
    if time_a == 'Beijing_time':
        tz = pytz.timezone('Asia/Shanghai') #东八区
        t = datetime.fromtimestamp(int(time.time()),
            pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S %Z%z')
        print(t)
    if time_a == 'GMT-8-Time_MS':
        gmt  = time.gmtime()
        millis = gmt.tm_hour*3600000 + gmt.tm_min*60000 + gmt.tm_sec*1000
        print(millis)
    if time_a == 'Running_time':
        s_time = time.time()
        sqrt_list = [x**2 for x in range(1, 1000000, 3)]
        e_time = time.time()
        print("{:.5}s".format(e_time-s_time))
