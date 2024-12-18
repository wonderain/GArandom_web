import copy

from common import *

class user():
    """实际不用这个玩意儿，只是放这里看看的"""
    def __init__(self,name,password,login_infos,power,email):
        """
        用户类
        :param name: 用户名
        :param password: 密码
        :param login_infos: 登录信息
        :param email: 邮箱，用于发送消息
        :param power: 权限 None表示无限权限，其余权限用列表表示
        0:登录权限
        1:修改个人资料权限
        2:创建比赛权限
        3:报名比赛权限
        4:查阅比赛记录权限
        """

def login_info(session_info):
    """
    输入会话信息，作为登录信息
    :param session_info:
    :return:
    """
    localtime=sft()
    user_ip=session_info['user_ip']
    user_agent=str(session_info['user_agent'])
    return [localtime,user_ip,user_agent]


class usersManager():
    default_power = [0, 1, 2, 3, 4]
    def __init__(self):
        self.dbpath='userdb.json'
        self.users=read_json(self.dbpath)
        self.onlineUsers = []
        if not self.users:
            write_json(self.dbpath,{})
            self.users={}
            self.register('管理员0号','guanliyuan0','1944149259@qq.com',[sft(),None,None],power=None)
    # 注册
    def register(self,name:str,password:str,email:str,login_info,power=default_power):
        if len(name)>10:return 1
        if len(password)<6 or len(password)>15:return 2
        if name in self.users:return 3
        self.users[name]={'password':password,'email':email,'power':power,'login_infos':[login_info]}
        self.onlineUsers.append(name)
        write_json(self.dbpath,self.users)
        return 0
    # 登入
    def login(self,name:str,password:str,login_info):
        print(name,'正在尝试登入',password,login_info)
        if name not in self.users:return 1
        if password!=self.users[name]['password']:return 2
        if name in self.onlineUsers:return 3
        self.users[name]['login_infos'].append(login_info)
        self.onlineUsers.append(name)
        write_json(self.dbpath, self.users)
        return 0
    # 登出
    def logout(self,name):
        try:
            self.onlineUsers.remove(name)
            print(name,'断开连接')
        except:
            print(traceback.format_exc())




