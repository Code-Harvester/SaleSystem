import json
from datetime import datetime, timedelta

from django.shortcuts import render, HttpResponse, redirect
import MySQLdb

# Create your views here.
from sale.models import USER


def test(REQ):
    openDB()
    return HttpResponse('欢迎')


def openDB():
    db = MySQLdb.connect(
        host='localhost',
        port=3306,
        user='root',
        db='salesys',
        password='123456',
        charset='utf8'
    )
    return db

def tuple2json(tuple, field):
    json_list = []
    for r in tuple:
        dicts = {}
        for n, i in enumerate(field):
            dicts[i] = str(r[n])
        json_list.append(dicts)
    json_result = json.dumps(json_list, ensure_ascii=False)
    return json_result


def login(REQ):
    userid = REQ.GET.get('userid')
    password = REQ.GET.get('password')
    rs = USER.objects.filter(UserID=userid, Password=password)  # 查询数据库是否有匹配项
    if rs.exists():
        identity = rs.first().Identity
        return HttpResponse(identity + 1)
    return HttpResponse(0)


def index(REQ):
    return render(REQ, 'search.html')


def goodssearch(REQ):
    db = openDB()
    cur = db.cursor()
    print(REQ.POST)
    keyword = REQ.POST.get('queryname')
    sql = "select * from sale_goodsinfo where GoodID like '%%%s%%' or GoodName like '%%%s%%'" % (keyword, keyword)
    cur.execute(sql)
    # print(sql)
    rq = cur.fetchall()
    field = ['GoodID', 'GoodName', 'Price', 'Cost', 'Type', 'Stock', 'QGPeriod', 'Note']
    json_result = tuple2json(rq, field)
    # print(json_result)
    cur.close()
    db.close()
    return HttpResponse(json_result)


def goodsadd(REQ):
    db = openDB()
    cur = db.cursor()
    keywords = []
    for key in REQ.POST:
        keywords.append(key.value)
    keywords = tuple(keywords)
    sql = "insert into sale_goodsinfo ('GoodID', 'GoodName', 'Price', 'Cost', 'Type', 'Stock', 'QGPeriod', 'Note') \
           values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % keywords
    cur.execute(sql)
    cur.close()
    db.close()

    return HttpResponse(1)
