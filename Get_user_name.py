#获取图书馆座位使用者姓名
#默认为一楼西104，若有需要请修改下列roomid

import requests
from urllib.parse import urlencode
import time
import json
time_stamp=int((round(time.time() * 1000)))


# roomId=100455348  #一楼西104
roomId=100455582   #西204
# roomId=100455578   #西201
# roomId=100455588   #西301
# roomId=100455590   #西303
# roomId=100455592   #西401
# roomId=100455594   #西403
# roomId=100455596   #西501
# roomId=100455598   #西504


data={
'byType':'devcls',
'classkind':8,
'display':'fp',
'md': 'd',
'room_id': roomId,
'purpose':'',
'cld_name': 'default',
'date': time.strftime('%Y-%m-%d', time.localtime(time.time())),
'fr_start': time.strftime('%H')+':00',
'fr_end': time.strftime('%H')+':10',
'act': 'get_rsv_sta',
'_': time_stamp
}

url='http://seat.hhit.edu.cn/ClientWeb/pro/ajax/device.aspx?'+urlencode(data)

try:
	r=requests.get(url)
	html=r.text
	data=json.loads(html)
except:
	pass

for m in data['data']:
    name=m['ts']
    if name:
        print(m['devName'],m['ts'][0]['owner'])
    else:
        pass
