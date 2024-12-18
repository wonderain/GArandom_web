import json,datetime,time
import os,locale,traceback,re
locale.setlocale(locale.LC_ALL, 'en')

# 返回格式化时间
def sft():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


# 装饰器，用于计时
def timer(func):
    def func_in():
        start_time = time.time()
        func()
        end_time = time.time()
        spend_time = (end_time - start_time)/60
        print("Spend_time:{} min".format(spend_time))
    return func_in

# 按行读txt，返回列表
def read_txt_line(path):
    lines=[]
    with open(path,'r',encoding='utf-8') as f:
        for line in f.readlines():
            line=line.replace('\n','')
            if '#' in line:
                line=line[:line.find('#')]
            if line=='':
                continue
            lines.append(line)
    return lines

# 保存json
def write_json(path,data):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data,ensure_ascii=False,indent=4))

# 加载json格式
def read_json(path):
    try:
        if not os.path.exists(path):
            return False
        with open(path, 'r', encoding='utf-8') as f:
            result = json.load(f)
        return result
    except Exception as e:
        print(e.args)
        return False


if __name__=='__main__':
    print(sft())