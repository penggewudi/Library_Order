#__author__='DP'
#encoding='utf-8'


#淮海工学院图书馆预约选座程序）
#设置定时任务（windows或者linux）

#请勿作为任何商业用途,仅仅作为个人学习已经研究所用.
#使用时请修改学号，默认的学号为0000000000

import time
import requests
import datetime
import sys
from aip import AipOcr
from urllib.parse import urlencode



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


time_form=['2018-'+str(month)+'-'+str(days)+' '+'08:00','2018-'+str(month)+'-'+str(days)+' '+'09:00','800','900']
                        # 序号处修改预约时间       1                                              2     3      4
                        # 3，4 处预约时间应改为（08:00改为800，12:00改为1200）

class  get_set(object):
    def __init__(self,student_id,desk_id):
        self.student_id=student_id   #学号
        self.desk_id=desk_id     #座位号id,（请联系管理员获取座位的方法）
        self.session = requests.session()   #stay connection
        self.retry=5   #如果预约失败，重新预约尝试次数

    def start_demo(self):
        print('---------------------------------------------------------------------------------')
        print('淮海工学院图书馆预约选座(v4.0)')
        print('使用时请修改学号，默认的学号为0000000000')
        print('---------------------------------------------------------------------------------')
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        print('---------------------------------------------------------------------------------')

    def yzm_get(self):
        r = self.session.get('http://seat.hhit.edu.cn/ClientWeb/pro/page/image.aspx???')
        with open('yzm.jpg', 'wb') as f:
            f.write(r.content)
            f.close()

    def yzm(self):
        #此处为百度云API文字识别，可以自己去注册申请，每天可以免费试用50000万次。
        #具体API调用方法可以去看使用文档，将*修改为自己的id,api_key,serect_key.
        appid = '11406441'
        apikey = 'HDCiq7IuEtGO1lLznX4dD63O'
        sercet_key = 'zRrtxfFiP3NHYrbtEsMujsCI36Zsnf8c'

        client = AipOcr(appid, apikey, sercet_key)
        with open('yzm.jpg', 'rb') as fp:
            image = fp.read()
        """ 调用通用文字识别, 图片参数为本地图片 """
        message = client.basicGeneral(image)
        print('当前验证码识别为', message['words_result'][0]['words'])
        return message['words_result'][0]['words']

    def login(self):
        while (self.retry > 0):
            self.yzm_get()
            date = {'id': self.student_id,
                    'pwd': self.student_id,
                    'number': self.yzm(),
                    'act': 'dlogin'}
            url_login = 'http://seat.hhit.edu.cn/ClientWeb/pro/ajax/login.aspx'
            # 根据用户名和密码登录选座系统
            r = self.session.post(url_login, data=date, headers=header)
            if r.json()['msg']=='ok':
                print('执行结果:',r.json()['msg'])
                print('login success~~~ your name is :', r.json()['data']["name"])
                break
            else:
                self.retry-=1


    def select_desk(self,start,end,start_time,end_time):
        time_stamp = int((round(time.time() * 1000)))
        self.start=start #预约起始时间
        self.end=end  #预约结束时间
        self.start_time=start_time   #此处为开始修改时间，例如8:00应该改成800，21:30修改为2130
        self.end_time=end_time      #此处为结束修改时间，修改方式同上
        date_yy = {
            'dialogid':'',
            'dev_id': self.desk_id,
            'lab_id':'',
            'kind_id':'',
            'room_id':'',
            'type': 'dev',
            'prop':'',
            'test_id':'',
            'term':'',
            'test_name':'',
            'start':self.start,
            'end': self.end,
            'start_time':self.start_time,
            'end_time': self.end_time,
            'up_file':'',
            'memo':' ',
            'memo':' ',
            'act': 'set_resv',
            '_': time_stamp
        }

        url_yy = 'http://seat.hhit.edu.cn/ClientWeb/pro/ajax/reserve.aspx?'+urlencode(date_yy)
        print(url_yy)
        try:
            while(self.retry>0):
                r = self.session.get(url_yy, data=date_yy, headers=header)
                if r.status_code == 200:
                    print('选座正常运行')
                else:
                    print("出现错误！！！")
                #！！！这里进行判断，如果操作成功，退出登录，否则根据重试次数继续预约
                if(r.json()["msg"].find('操作成功')==-1):
                    print(r.text)
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

    stdudent_1=get_set(student_id=2015120786,desk_id=00000000)   #在这里输入学号和座位号
    stdudent_1.start_demo()
    stdudent_1.login()
    stdudent_1.select_desk(start=time_form[0],end=time_form[1],start_time=time_form[2],end_time=time_form[3])
    stdudent_1.quit_system()






