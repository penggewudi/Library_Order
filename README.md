#     图书馆座位预约抢座

>！！！代码已失效，仅作为学习参考

  每天早上，五点29的闹钟准时响起，睡眼朦胧的拿起手机开始接下来的工作，因为接下来的一分钟，众多考研党们将一同去争夺图书馆一楼绝佳的复习位置，这个位置对于我们这些考研狗们十分重要，因为这将影响着我们一天复习的效率，可是早起对于晚睡的我们是多么的困难，于是，我们就这种尝试了一下~~~

> 仅供个人学习以及研究，不得作为任何商业用途。


这里以linux 的centos为例吧！首先你的服务器上肯定是要有python的运行环境的，windows的话自己安装，linux的话一般自带
linux的每天定时执行任务用到了


>crontab -e  了解详细信息的话可以自行查阅资料

>31 5 * * * python    这里写你想运行程序的路径（例如:/usr/bin/123.py）

将这行代码插入进去，然后保存退出，即每天的5:31分自动执行程序，那么这样话才差不多实现了自动的过程。打了好多字呀，好累呀。



----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
### 更新~
   （由于学校的图书馆座位预约系统预约时间发生了改变，每次只能预约4个小时，所以需要长时间学习的同学需要每天跑3次）
       
  >> 代码放在2.0里面，1,2,3分别是从早上8点到12点，12点到16点，16点到20点  
  >> 修改完student id 以及desk id ，运行power start即可
  更新如下
 >新增了多名同学一起预约座位（不建议太多，会减低速度以及成功率）
 >加入了异常处理，默认预约失败重新跑10次
 
 ## 由于每4小时预约一次，需要每天跑三次，程序暂未测试，未完待续~

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
### 更新~~
  修改了header，提高了spider的稳定性，同时将多次选座集成到一个的demo里面，详情请看/3.0
 
## 测试成功，撒花~

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
### 更新~~
  将程序打包成了exe可执行文件，方便没有py环境的情况下使用。
  
 >1.程序实现的功能是获取12个小时的座位时间，但是学号和座位的id号码需要手动输入！！！
 
 >2.最好在64位的机器上运行，建议win10。
 
 >3.exe程序使用pyinstaller打包，兼容性和可用性待完善，这里不再说明。

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
### 更新~~
 >1.新增一楼座位号txt，方便查询~~~

 >2.新增查询代码，可以查看座位的使用者~~~

 >3.exe需要管理员密码，想要获取密码请联系email我~

![Result](https://i.loli.net/2018/04/15/5ad2272d4ef83.png)

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
### 更新~~

  由于学校的图书馆预约机制启用了`验证码`登录，所以想要实现验证码登录需要后续更新，暂时由于手机端的预约端还不需要验证码，所以通过移动端web登录
  [CLICK HERE FOR MORE](http://seat.hhit.edu.cn/ClientWeb/m/ic2/Default.aspx) 

 >1.由于学校的预约时间又改回来了，不需要多次预约了，所以改为一次预约

 >2.修改heads

 >3.请求的数据由之前的form改为了query string


## PS:
  经过测试，可以执行。虽然暂时手机端的还可以登陆预约，但是关于验证码的识别肯定是后续要完成的工作，目前可以尝试的有第三方`API`或者`machine leaning`。

> 注意：之前的的代码以及exe基本失效，查询座位使用者还可以使用，剩余code仅供参考，未完待续。。。
 
![Result]( https://i.loli.net/2018/07/15/5b4ade7358f6e.png)

## 更新~~
   果然我之前的猜测是正确的，在登陆界面加入验证码之后，首先想到的是用第三方API进行调用识别，之前寒假因为用过百度的API，所以这里就采用百度的`APIOCR`进行识别，由于验证码较为简单全为数字组成，所以识别的准确率还是不错的，基本上五次以内肯定有一次是正确的，所以讲程序的重试次数设置为五次，经过测试，基本上可以完成登陆。

>1.关于百度文字识别的API，可以去参考百度云官方文档[CLICK HERE FOR MORE](https://cloud.baidu.com/doc/OCR/index.html)

>2.测试过登陆程序之后出现了问题，发现是由于图书馆修改了get的表单，修改后OK。

## PS:
  之前出现验证码的问题之后，想到了是三个解决办法，现在已经实现了两个，还有一个是通过训练来识别验证码，由于时间问题，等待后续的更新了，就这样了吧~~~哈哈哈
![Result](https://i.loli.net/2018/07/16/5b4b7484069e3.png)

>另外：感谢我的朋友提出这么好的想法，感谢思密达~

                              欢迎提出宝贵的建议以及改进的地方，作者技术有限，轻喷，谢谢！





