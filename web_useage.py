
import time,datetime
from pywebio import input as webinp   # 用这个代替input
from pywebio import output,start_server,session,pin


# 接入的用户次数
visitorInfo={'visitTimes':0,'nowVisitorCount':0}


def greet_user():
    username = webinp.input("请输入你的名字：")
    output.put_text(f"你好，{username}！欢迎使用PyWebIO。")

# 网络投票功能
Candidates={"候选人A":0,"候选人B":0,"候选人C":0}
def vote_app():
    candidates = webinp.checkbox("请选择候选人：", options=["候选人A", "候选人B", "候选人C"])
    for c in candidates:
        Candidates[c]+=1
    output.put_text("你的投票已经提交！")
    output.put_text("投票结果：")
    for candidate,count in Candidates.items():
        output.put_text(f"{candidate}: {count} 票")

# 使用用户信息
def userinfo():
    """
    example:
    session.info-->{'user_agent': <user_agents.parsers.UserAgent object at 0x00000235CBE1FA48>,
    'user_language': 'zh-CN', 'server_host': '192.168.1.50:8875',
     'origin': 'http://192.168.1.50:8875', 'user_ip': '192.168.1.50',
     'request': HTTPServerRequest(protocol='http', host='192.168.1.50:8875', method='GET', uri='/?app=index&session=NEW', version='HTTP/1.1', remote_ip='192.168.1.50'),
      'backend': 'tornado', 'protocol': 'websocket'}
    :return:
    """
    info=session.info
    user_agents=info['user_agent']
    output.put_text(user_agents,'|',user_agents.browser.family,user_agents.os.family,user_agents.device.family)


# 持续输出信息
def continue_show():
    visitorInfo['visitTimes']+=1
    visitorInfo['nowVisitorCount']+=1
    session.defer_call(when_session_close)  # 设定用户离开或断开的函数

    # scope表示一个输出域,使用以下方法设置一个域
    output.put_scope('visitorInfo')

    while True:
        # 使用一个输出域,clear表示进入scope时会先清空其中的内容
        with output.use_scope(name='visitorInfo', clear=True):
            output.put_text('访问次数', visitorInfo['visitTimes'], '当前用户数量', visitorInfo['nowVisitorCount'],'时间',datetime.datetime.now())
        time.sleep(5)

def when_session_close():
    visitorInfo['nowVisitorCount'] -= 1

# 按钮效果
def button_example():
    pin.put_input('num1',label='输入第一个数字',type=webinp.NUMBER)
    pin.put_input('num2', label='输入第二个数字', type=webinp.NUMBER)
    def cal(button):
        print(button)
        num1=pin.pin['num1']
        num2=pin.pin['num2']
        ret = num1+num2
        output.put_text(f'{num1}+{num2}={ret}')
    output.put_button('计算',onclick=cal)
    session.hold()

def frameChange():
    output.put_scope('1')
    output.put_scope('2')
    global s
    s=False
    def swich():
        global s
        if s:
            output.remove('2')
            with output.use_scope(name='1', clear=True):
                output.put_text('时间',datetime.datetime.now())
                output.put_button('swich', onclick=swich)
            s=False
        else:
            output.remove('1')
            with output.use_scope(name='2', clear=True):
                output.put_text('2')
            s=True


    output.put_button('swich', onclick=swich)
    session.hold()


class Cookie():
    """
    借助run_js脚本来实现cookie保存登陆信息
    """
    def __init__(self):
        session.run_js("""
        window.setCookie = function(name,value,days) {
            var expires = "";
            if (days) {
                var date = new Date();
                date.setTime(date.getTime() + (days*24*60*60*1000));
                expires = "; expires=" + date.toUTCString();
            }
            document.cookie = name + "=" + (value || "")  + expires + "; path=/";
        }
        window.getCookie = function(name) {
            var nameEQ = name + "=";
            var ca = document.cookie.split(';');
            for(var i=0;i < ca.length;i++) {
                var c = ca[i];
                while (c.charAt(0)==' ') c = c.substring(1,c.length);
                if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
            }
            return null;
        }
        """)
    def save(self,name,password):
        session.run_js("setCookie(key, value)", key='name', value=name)
        session.run_js("setCookie(key, value)", key='password', value=password)

    def get(self):
        name=session.eval_js("getCookie(key)", key='name')
        password = session.eval_js("getCookie(key)", key='password')
        return name,password

# 登录
def login():
    cookie=Cookie()
    name,password=cookie.get()
    output.put_scope('login')
    def login_():
        name = pin.pin['login_username']
        password= pin.pin['login_password']
        cookie.save(name,password)
        output.remove('login')
    if name is None or password is None:
        with output.use_scope('login', clear=True):
            pin.put_input('login_username',label="请输入用户名：")
            pin.put_input('login_password',label='请输入密码')
        output.put_button('登入', onclick=login_)
    else:
        print(name,password)
        output.put_text(f'{name} 登入成功')
    session.hold()


# 同方法不同传参的按钮
def setButtons():
    from functools import partial   # partial 可以固定一个传参
    def edit_row(choice, row):
        print(choice)
        output.put_text("You click %s button ar row %s" % (choice, row))
    # 当使用buttons的时候，会返回选择了哪个button
    output.put_table([
        ['Idx', 'Actions'],
        [1, output.put_buttons(['edit', 'delete'], onclick=partial(edit_row, row=1))],
        [2, output.put_buttons(['edit', 'delete'], onclick=partial(edit_row, row=2))],
        [3, output.put_buttons(['edit', 'delete'], onclick=partial(edit_row, row=3))],
    ])

if __name__ == '__main__':
    start_server(setButtons,port=8875,debug=True)
    
