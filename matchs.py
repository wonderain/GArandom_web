from common import *


class match():
    def __init__(self,title,type1,type2,times,max_player_num,enroll_start_time,enroll_end_time,discribe,rules,editors,choice_team_order):
        """
        比赛信息
        :param choice_team_order:选择队伍的顺序，k=[t,v]表示已经选好k个人，下一次由t选v个，如{2:[1,1],3:[2,2],5:[1,1]}
        :param editors: list,可以编辑的人
        :param type1:分类1-个人(0)or团队分队数量(如:2)
        :param type2:分类1-不自动分队(0),自动分队(1)or自动分队长(2)
        :param rules: 比赛详细规则
        :param discribe: 比赛简单描述
        :param title: 标题
        :param times: 几次性（N）or长期（-1）
        :param max_player_num: 最大参与人数(等于多于这个人数直接开始)
        :param enroll_start_time:报名开始时间
        :param enroll_end_time:报名结束时间
        """
        pass

class match_record():
    def __init__(self,players,teams,win,start_time,end_time):
        """
        :param players: list 参与玩家
        :param teams: list 分队，如果是个人赛，那就队伍数量跟参与数一致
        :param win: list 每个队伍的获胜情况，0是淘汰，1是第一名，2是第二名，……，如果只有两队，那就1-……是胜，0是败
        :param start_time:
        :param end_time:
        """
        pass

class Matchs():
    def __init__(self):
        self.dbpath = 'matchdb.json'
        self.recordpath='match_records'
        try:os.mkdir(self.recordpath)
        except:pass
        self.matches = read_json(self.dbpath)
        if not self.matches:
            write_json(self.dbpath, {})
            self.matches = {}
            self.newMatch('单挑赛',0,1,-1,2,'2000','2050-8-10','单挑不是单挑，快刀才是快刀','...',['宇宙大王'], [])
    def newMatch(self,title,type1,type2,times,max_player_num,enroll_start_time,enroll_end_time,discribe,rules,editors,choice_team_order):
        """创建一种新比赛"""
        if title in self.matches:return False
        self.matches[title]={'type1':type1,'type2':type2,'times':times,
                                   'max_player_num':max_player_num,
                                   'enroll_start_time':enroll_start_time,'enroll_end_time':enroll_end_time,
                                   'discribe':discribe,'rules':rules,'editors':editors,'choice_team_order':choice_team_order}
        write_json(self.dbpath,self.matches)
    def getValidMatches(self):
        """获取有效时间内且还有比赛场次的比赛（-1是无限场次，0才是无场次）"""
        validMatches={}
        for title in self.matches:
            if sft()<self.matches[title]['enroll_end_time'] and self.matches[title]['times']!=0:
                validMatches[title]=self.matches[title]
        return validMatches
    def record(self,title,players,teams,win,start_time,end_time):
        """记录"""
        recordpath=self.recordpath+'/%s.json'%title
        record=read_json(recordpath)
        if not record:
            record=[]
        record.append({'players':players,'teams':teams,'win':win,'start_time':start_time,'end_time':end_time})
        write_json(recordpath, record)


if __name__=='__main__':
    m=Matchs()
    m.newMatch('老登局8',2,2,-1,8,'2000','2050-8-10','','',['宇宙大王'],[0,1,1,0,0,1])
    m.newMatch('老登局6', 2, 2, -1, 6, '2000', '2050-8-10', '', '', ['宇宙大王'],[0,1,1,0])