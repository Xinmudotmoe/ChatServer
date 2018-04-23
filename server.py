import http.server
import re
import sqlite3
import time
import json
cout=[]
sql = sqlite3.Connection("sqlite3/chat.sl3")#,check_same_thread = False)
# pycharm显示异常 #check_same_thread理论上会提高一些速度 但会造成一定程度的数据库不稳定


class INBException(Exception):
    pass
def decode(strs:str) -> str:
    a=strs.split("_")
    b=[]
    for i in a:
        i=int(i)
        if i>0xff:
            c=[]
            while i:
                c.append(i&0xff)
                i>>=8
            b.append(bytes(c).decode('utf-16'))
        else:
            b.append(i.to_bytes(1,'big').decode('ansi'))
    return ''.join(b)
    
def processor(dicts: {"": ""}) -> (int, str):  # Chat请求函数
    clear()
    if not "types" in dicts.keys():
        raise INBException("0")
    if dicts["types"] == '-1':
        return newuser(dicts)
    elif dicts["types"] == '0':
        return output(dicts)
    elif dicts["types"] == '1':
        send(dicts)
        return output(dicts)
    raise INBException("-1")


def newuser(dicts: {"": ""}) -> (int, str):
    sqc = sql.cursor()
    Users = [i[0] for i in sqc.execute("select id from User;").fetchall()]
    #  i=0 #新版本特性 #个屁 只是ide的警告 我就这样用了 能怎么滴 (╯‵□′)╯︵┻━┻
    for i in range(1, 2048):
        if i not in Users:
            break
    nowUtc = int(time.time() * 1000)
    sqc.executescript("insert into User(id,time,lasttime)values(%d,%d,%d);" % (i, nowUtc, nowUtc))
    #cout.append(''.join(["创建了一个新用户:",str(i)]))
    print(''.join(["创建了一个新用户:",str(i)]))
    return 200, str(i)


def output(dicts: {"": ""}) -> (int, str):
    nowUtc = int(time.time() * 1000)
    if "uid" not in dicts:
        raise INBException('1')
    sqc = sql.cursor()
    ut = sqc.execute("select lasttime from User where id = %s;" % dicts["uid"]).fetchall()
    sqc.executescript("update User set lasttime = %d where id = %s"%(nowUtc,dicts["uid"]))
    if len(ut) == 0:
        raise INBException('2')
    message = sqc.execute("select UID,UTC,message from Chat where UTC>%s;" % ut[0][0]).fetchall()
    return 200, json.dumps([{"uid": i[0], "utc": i[1], "message": i[2]} for i in message])

def send(dicts: {"": ""}) -> (int, str):
    nowUtc = int(time.time() * 1000)
    if "uid" not in dicts:
        raise INBException('1')
    sqc = sql.cursor()
    sqc.executescript("insert into Chat(UID,UTC,message)values(%s,%d,%s);" %
                      (dicts["uid"], nowUtc, ''.join(["\"", dicts["send"], "\""])))
    #cout.append(''.join(["用户<",dicts["uid"],">\t-->",dicts["send"]]))
    print(''.join(["用户<",dicts["uid"],">\t-->",decode(str(dicts["send"]))]))
    


def clear() -> None:
    nowUtc = int(time.time() * 1000)
    sqc = sql.cursor()
    sqc.executescript("DELETE FROM User WHERE lasttime < %d;" % (nowUtc - 30000))
