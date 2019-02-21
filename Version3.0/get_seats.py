#__author__='DP'
#encoding='utf-8'

#修改header,将时间修改为一套程序！

#淮海工学院图书馆预约选座程序，（每次的预约时间修改为4个小时，并且开始预约时间改为上午六点）
#  每次预约4个小时，每天可以预约3次 ，设置定时任务（windows或者linux）
#请勿作为任何商业用途,仅仅作为个人学习已经研究所用.
#使用时请修改学号，默认的学号为0000000000

import time
import requests
import datetime
import sys



header={
'Accept':'application/json, text/javascript, */*; q=0.01',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Connection': 'keep-alive',
'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
'Host':'seat.hhit.edu.cn',
'Origin': 'http://seat.hhit.edu.cn',
'Referer': 'http://seat.hhit.edu.cn/ClientWeb/xcus/ic2/Default.aspx',
'X-Requested-With': 'XMLHttpRequest',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}

nowtime=datetime.datetime.now()
detaday=datetime.timedelta(days=1)
mt_days=nowtime+detaday
month=mt_days.strftime("%m")
days=mt_days.strftime("%d")


time_form=[
['2018-'+str(month)+'-'+str(days)+'+'+'11:00','2018-'+str(month)+'-'+str(days)+'+'+'12:00','1100','1200'],
['2018-'+str(month)+'-'+str(days)+'+'+'12:00','2018-'+str(month)+'-'+str(days)+'+'+'13:00','1200','1300'],
['2018-'+str(month)+'-'+str(days)+'+'+'13:00','2018-'+str(month)+'-'+str(days)+'+'+'14:00','1300','1400']
]


class  get_set(object):
    def __init__(self,student_id,desk_id):
        self.student_id=student_id   #学号
        self.desk_id=desk_id     #座位号id,（请联系管理员获取座位的方法）
        self.session = requests.session()   #stay connection
        self.retry=5   #如果预约失败，重新预约尝试次数

    def start_demo(self):
        print('---------------------------------------------------------------------------------')
        print('淮海工学院图书馆预约选座(v3.0)，根据设置的时间去预约第二天的位置，预约三次，每次4小时从8点开始')
        print('使用时请修改学号，默认的学号为0000000000')
        print('---------------------------------------------------------------------------------')
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        print('---------------------------------------------------------------------------------')

    def logic(self):
        date = {'act': 'login',
                'id': self.student_id,
                'pwd': self.student_id}
        url_logic = 'http://seat.hhit.edu.cn/ClientWeb/pro/ajax/login.aspx'
        # 根据用户名和密码登录选座系统
        try:
            r = self.session.post(url_logic, data=date, headers=header)
            if r.status_code == 200:
                # print(r.status_code)
                print('Login success!!!')
                print('你登录的用户名称为：', r.json()['data']['name'])
            else:
                print('Login error!!!')
        except:
            print('Login error!!!')
            sys.exit()

    def select_desk(self,start,end,start_time,end_time):
        time_stamp = int((round(time.time() * 1000)))
        self.start=start #预约起始时间
        self.end=end  #预约结束时间
        self.start_time=start_time   #此处为开始修改时间，例如8:00应该改成800，21:30修改为2130
        self.end_time=end_time      #此处为结束修改时间，修改方式同上
        date_yy = {
            '_': time_stamp,
            'act': 'set_resv',
            'dev_id': self.desk_id,
            'end': self.end,
            'end_time': self.end_time,
            'kind_id': '',
            'lab_id': '',
            'memo': '',
            'prop': '',
            'room_id': '',
            'start': self.start,
            'start_time': self.start_time,
            'term': '',
            'test_id': '',
            'type': '',
            'up_files': ''
        }
        url_yy = 'http://seat.hhit.edu.cn/ClientWeb/pro/ajax/reserve.aspx?dev_id=' + str(self.desk_id) + '&lab_id=&kind_id=&room_id=&type=dev&prop=&test_id=&term=&test_name=&start=' + str(self.start) + '&end=' + str(self.end) + '&start_time=' + str(self.start_time) + '&end_time=' + str(self.end_time) + '&up_file=&memo=&memo=&act=set_resv&_=' + str(time_stamp)
        try:
            while(self.retry>0):
                r = self.session.get(url_yy, data=date_yy, headers=header)
                if r.status_code == 200:
                    print('选座正常运行')
                else:
                    print("返回错误码")
                    print("正在打印信息:")
                print(''+r.json()["msg"])
                #！！！这里进行判断，如果操作成功，退出登录，否则根据重试次数继续预约
                if(r.json()["msg"].find('操作成功')==-1):
                    self.retry-=1
                else:
                    break
                time.sleep(0.5)
        except:
            print(' Get desk error!!!')
            sys.exit()

        print('正在退出...')


    def quit_system(self):
        time_stamp_q = int((round(time.time() * 1000)))
        date_quit = {'_': time_stamp_q,
                     'act': 'logout'
                     }
        url_quit = 'http://seat.hhit.edu.cn/ClientWeb/pro/ajax/login.aspx?act=logout&_=' + str(time_stamp_q)
        r = self.session.get(url_quit, data=date_quit, headers=header)
        r.raise_for_status()
        print('退出', r.json()['msg'])
        self.session.close()


if __name__=='__main__':
    #可以一次加上多个同学的学号以及座位号，但是不建议这么做，因为这样会降低运行速度

    stdudent_1=get_set(student_id=0000000000,desk_id=999999999)   #在这里输入学号和座位号
    stdudent_1.start_demo()
    stdudent_1.logic()
    for times in time_form:
        # print(times[0],times[1],times[2],times[3])
        stdudent_1.select_desk(start=times[0],end=times[1],start_time=times[2],end_time=times[3])
    stdudent_1.quit_system()






