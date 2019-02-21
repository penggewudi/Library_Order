#__author__='DP'
#encoding='utf-8'

#修改header

#淮海工学院图书馆预约选座程序，
# 设置定时任务（windows或者linux）
#请勿作为任何商业用途,仅仅作为个人学习已经研究所用.
#使用时请修改学号，默认的学号为0000000000


#test：2018.7.14 success

import time
import requests
import datetime
import sys
from  urllib.parse import urlencode

header={
'Accept': '*/*',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Connection': 'keep-alive',
'Host': 'seat.hhit.edu.cn',
'Referer': 'http://seat.hhit.edu.cn/ClientWeb/m/ic2/Default.aspx',
'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
'X-Requested-With': 'XMLHttpRequest'
}

#计算时间，格式化时间格式输出，延后一天
nowtime=datetime.datetime.now()
detaday=datetime.timedelta(days=1)
mt_days=nowtime+detaday
month=mt_days.strftime("%m")
days=mt_days.strftime("%d")


class  get_set(object):
    def __init__(self,student_id,desk_id,start,end,start_time,end_time):
        self.student_id=student_id   #学号
        self.desk_id=desk_id     #座位号id,（请联系管理员获取座位的方法）
        self.session = requests.session()   #stay connection
        self.start=start #预约起始日期
        self.end=end  #预约结束日期
        self.start_time=start_time #预约起始时间
        self.end_time=end_time #预约结束时间
        self.retry=5

    def start_demo(self):
        print('---------------------------------------------------------------------------------')
        print('淮海工学院图书馆预约选座(v4.0)')
        print('使用时请修改学号，座位号，座位ID在同文件夹目录下，默认的学号为0000000000,')
        print('---------------------------------------------------------------------------------')
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        print('---------------------------------------------------------------------------------')

#http://seat.hhit.edu.cn/ClientWeb/pro/ajax/login.aspx?act=login&id=12121212&pwd=rwgeuigwie&role=512&aliuserid=&schoolcode=&wxuserid=&_nocache=1531581709300

    def logic(self):
        time_stamp = int((round(time.time() * 1000)))
        data = {'act': 'login',
                'id': self.student_id,
                'pwd': self.student_id,
                'role': '512',
                'aliuserid':' ',
                'schoolcode':' ',
                'wxuserid':' ',
                '_nocache':time_stamp}
        offset=urlencode(data)
        url_login = 'http://seat.hhit.edu.cn/ClientWeb/pro/ajax/login.aspx?'+offset
        # 根据用户名和密码登录选座系统
        try:
            r = self.session.get(url_login,  headers=header)
            if r.status_code == 200:
                # print(r.status_code)
                print('Login success!!!')
                print('你登录的用户名称为：', r.json()['data']['name'])
            else:
                print('Login error!!!')
        except:
            print('Login error!!!')
            sys.exit()

    def select_desk(self):
        time_stamp = int((round(time.time() * 1000)))
        message={'dev_id': self.desk_id,
                'lab_id': '100455340',  #自习教室的ID，默认图书馆一楼
                'room_id':'' ,
                'kind_id': '100455570', #未知，等待后续测试
                'type': 'dev',
                'prop': '',
                'test_id': '',
                'resv_id': '',
                'term': '',
                'min_user': '',
                'max_user': '',
                'mb_list': '',
                'test_name': '',
                'start': self.start,
}
        message_middle={
            'end': self.end,
        }
        message_add={
            'memo': '',
            'act': 'set_resv',
            '_nocache': time_stamp
        }

        url_order = 'http://seat.hhit.edu.cn/ClientWeb/pro/ajax/reserve.aspx?' + urlencode(message)+'%20'+str(self.start_time)+urlencode(message_middle)+'%20'+str(self.end_time)+urlencode(message_add)

        try:
            while(self.retry>0):
                r = self.session.get(url_order, headers=header)
                if r.status_code == 200:
                    print('选座正常运行')
                    print(''+r.json()["msg"])
                else:
                    print("出现错误，正在打印信息:")
                    print(''+r.json()["msg"])
                    # ！！！这里进行判断，如果操作成功，退出登录，否则根据重试次数继续预约
                if (r.json()["msg"].find('操作成功') == -1):
                        self.retry -= 1
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
        url_quit = 'http://seat.hhit.edu.cn/ClientWeb/pro/ajax/login.aspx?'+urlencode(date_quit)
        r = self.session.get(url_quit, headers=header)
        r.raise_for_status()
        print('退出', r.json()['msg'])
        self.session.close()


if __name__=='__main__':
    #可以一次加上多个同学的学号以及座位号，但是不建议这么做，因为这样会降低运行速度
    order_day= '2018-' + str(month) + '-' + str(days)

    #默认预约教室西104，若有需要请向上找到自习室ID处修改
    student_id=0000000000   #学号
    desk_id = 100457203     #座位号

    start_time='11:10'+'&'  #预约起始时间 注意：预约时间你应该根据实际情况修改，分钟不能出现小数！！！
    end_time='12:10'+'&'    #预约结束时间 注意事项同上！！！

    student_1=get_set(student_id,desk_id,order_day,order_day,start_time,end_time)   #在这里输入学号和座位号
    student_1.start_demo()
    student_1.logic()
    time.sleep(2)   #登陆后等待时间，默认两秒，可以改大改小，建议改大。
    student_1.select_desk()
    time.sleep(1)
    student_1.quit_system()








