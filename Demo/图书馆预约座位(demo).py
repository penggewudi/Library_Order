#__author__='DP'
#encoding='utf-8'
#v1.0

#淮海工学院选座demo，根据设置的时间去预约第二天的位置，时间为早上8点到晚上21点
#请勿作为任何商业用途,再次声明，出现任何问题概不负责。

import requests
import time
import datetime
import sys



def ready():
    student_ID=input('请输入你的学号进行预约:')
    if input('你输入的学号为'+student_ID+'确认请输入yes:')=='yes':
        print('开始执行......')
        return student_ID
    else:
        print('error!!!')
        sys.exit()


def quit(time_stamp_q):
    url_quit = 'http://seat.hhit.edu.cn/ClientWeb/pro/ajax/login.aspx?act=logout&_=' + str(time_stamp_q)
    r = session.get(url_quit, data=date_quit, headers=header)
    r.raise_for_status()
    print('退出',r.json()['msg'])
    session.close()


print('---------------------------------------------------------------------------------')
print('淮海工学院图书馆预约选座(v1.0)，根据设置的时间去预约第二天的位置，时间为早上8点到晚上21点')
print('---------------------------------------------------------------------------------')
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
print('---------------------------------------------------------------------------------')
# student_ID=2016120785  #学号
student_ID=ready()
#登陆页面的表单，即用户的账号以及密码  默认的账号等于密码  通过post方法
date={'act':'login',
'id':student_ID,
'pwd':student_ID
}

#反爬文件
header={
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
}

#登陆的url
url_dl='http://seat.hhit.edu.cn/ClientWeb/pro/ajax/login.aspx'

#使用session保持登陆的连接
session=requests.session()

#根据用户名和密码登录选座系统
try:
    r=session.post(url_dl,data=date,headers=header)
    if r.status_code==200:
    # print(r.status_code)
        print('Login success!!!')
        print('你登录的用户名称为：',r.json()['data']['name'])
    else:
        print('返回错误码')
except:
    print('Login error!!!')

#每天的选课时间从早上5:30开始！！！ 注意设置起始时间
#将当前时间延迟一天并且获取明天的时间
nowtime=datetime.datetime.now()
detaday=datetime.timedelta(days=1)
mt_days=nowtime+detaday

#将月份和天数格式化成url所需要的格式并将其余的信息补充到url内
month=mt_days.strftime("%m")
days=mt_days.strftime("%d")
dev_id=100456005 #西104—094/095
start='2019-'+str(month)+'-'+str(days)+'+'+'08:00'
end='2019-'+str(month)+'-'+str(days)+'+'+'21:00'
start_time='800'
end_time='2100'
time_stamp=int((round(time.time() * 1000)))


#选座递交的表单，通过get方法
date_yy = {
'_':time_stamp,
'act':'set_resv',
'dev_id':dev_id,
'end':end,
'end_time':end_time,
'kind_id':'',
'lab_id':'',
'memo':'',
'prop':'',
'room_id':'',
'start':start,
'start_time':start_time,
'term':'',
'test_id':'',
'type':'',
'up_files':''
}


url_yy='http://seat.hhit.edu.cn/ClientWeb/pro/ajax/reserve.aspx?dev_id='+str(dev_id)+'&lab_id=&kind_id=&room_id=&type=dev&prop=&test_id=&term=&test_name=&start='+str(start)+'&end='+str(end)+'&start_time='+str(start_time)+'&end_time='+str(end_time)+'&up_file=&memo=&memo=&act=set_resv&_='+str(time_stamp)
# print(url_yy)

try:
    r=session.get(url_yy,data=date_yy,headers=header)
    if r.status_code==200:
        print('选座正常运行')
    else:
        print("返回错误码")
    print("正在打印信息:")
    print(r.json()["msg"])
except:
    print(' Get desk error!!!')

print('正在退出...')
time.sleep(3)

time_stamp_q = int((round(time.time() * 1000)))

date_quit={'_':time_stamp_q,
'act':'logout'
}


quit(time_stamp_q)

