import json
import time

from django.shortcuts import render, HttpResponse
import MySQLdb

# Create your views here.
from sale.models import USER, GOODSINFO, CHANGELOG

goodsType = {'xuegao': '雪糕',
            'yinliao': '饮料',
            'lingshi': '零食',
            'richang': '日常用品',
            'fangbianmian': '方便面'}

lossreason = {'guoqi': '过期',
              'bianzhi': '变质',
              'sunhuai': '损坏',
              'diushi': '丢失'}

def test(REQ):
    openDB()
    return HttpResponse('欢迎')


def openDB():
    '''打开数据库'''
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
    '''将数据库结果转换成json格式'''
    json_list = []
    for r in tuple:
        dicts = {}
        for n, i in enumerate(field):
            dicts[i] = str(r[n])
        json_list.append(dicts)
    json_result = json.dumps(json_list, ensure_ascii=False)
    return json_result


def login(REQ):
    '''登录函数'''
    userid = REQ.GET.get('userid')
    password = REQ.GET.get('password')
    rs = USER.objects.filter(UserID=userid, Password=password)  # 查询数据库是否有匹配项
    if rs.exists():
        identity = rs.first().Identity
        return HttpResponse(identity + 1)
    return HttpResponse(0)


def index(REQ):
    '''测试页面用的函数，无实际意义'''
    return render(REQ, 'sale.html')


def goods_search(REQ):
    '''商品搜索，更具关键字搜索'''
    db = openDB()
    cur = db.cursor()
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


def goods_add(REQ):
    '''添加商品'''
    db = openDB()
    cur = db.cursor()
    keywords = []
    for n, key in enumerate(REQ.POST):
        item = REQ.POST[key]
        if key == 'Type' and item in goodsType:
            item = goodsType[item]  # 将种类的拼音转换成汉字
        keywords.append(item)
    keywords = tuple(keywords)
    sql = "insert into sale_goodsinfo (GoodID, GoodName, Price, Cost, Type, Stock, QGPeriod, Note) " \
          "values ('%s', '%s', %s, %s, '%s', 0, %s, '%s')" % keywords
    print(sql)
    try:
        cur.execute(sql)
        db.commit()
        cur.close()
        db.close()
    except Exception as e:
        print('添加失败的原因', end='')
        print(e)
        return HttpResponse(0)
    print('添加成功')
    return HttpResponse(1)


def goods_delete(REQ):
    '''删除商品'''
    deleteID = REQ.POST.get('deleteID')
    try:
        GOODSINFO.objects.filter(GoodID=deleteID).delete()
    except:
        # print(e)
        return HttpResponse(0)
    return HttpResponse(1)


def goods_sale(REQ):
    '''销售商品'''
    re = []
    for n, item in enumerate(REQ.POST):
        if n % 5 == 0 or n % 5 == 4:
            re.append(REQ.POST[item])
    order = [[re[2 * i], re[2 * i + 1]] for i in range(len(re) // 2)]
    # print(order)
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    # print(date)
    db = openDB()
    cur = db.cursor()
    # id = REQ.POST.get('id')
    id = 'server1'
    try:
        for i in order:
            if i[0] == '':  # 避免前端传递空串
                continue
            sql = "insert into sale_sale (GoodID, Time, Mount, UserID) " \
                  "values ('%s', '%s', %s, '%s')" % (i[0], date, i[1], id)
            # print(sql)
            cur.execute(sql)
            db.commit()
    except Exception as e:
        print(e)
        return HttpResponse(0)
    return HttpResponse(1)


def goods_storage(REQ):
    '''商品入库'''
    re = []
    for item in REQ.POST:
        re.append(REQ.POST[item])
    order = [[re[2 * i], re[2 * i + 1]] for i in range(len(re) // 2)]
    # print(order)
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 获取当前时间
    # id = REQ.POST.get('id')
    id = 'admin'
    for i in order:
        if i[0] == '' or i[1] == '':  # 避免前端传递空值
            continue
        try:
            rq = GOODSINFO.objects.filter(GoodID=i[0])
            stock = rq.first().Stock + int(i[1])
            rq.update(Stock=stock)
            note = '入库%d个' % int(i[1])
            CHANGELOG.objects.create(GoodID=i[0], Time=date, Add=int(i[1]), Loss=0, UserID=id, Note=note)
        except:
            return HttpResponse(0)
    return HttpResponse(1)

def goods_loss(REQ):
    '''商品损耗'''
    re = []
    for item in REQ.POST:
        re.append(REQ.POST[item])
    order = [[re[3 * i], re[3 * i + 1], re[3 * i + 2]] for i in range(len(re) // 3)]
    # print(order)
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 获取当前时间
    # id = REQ.POST.get('id')
    id = 'admin'
    for i in order:
        if i[0] == '' or i[1] == '':  # 避免前端传递空值
            continue
        try:
            rq = GOODSINFO.objects.filter(GoodID=i[0])
            stock = rq.first().Stock - int(i[1])
            if stock < 0:
                return HttpResponse(0)
            rq.update(Stock=stock)
            note = ''
            if i[2] != '':
                note = '%s%d个' % (lossreason[i[2]], int(i[1]))
            CHANGELOG.objects.create(GoodID=i[0], Time=date, Add=0, Loss=int(i[1]), UserID=id, Note=note)
        except:
            return HttpResponse(0)
    return HttpResponse(1)


def sale_statistics(REQ):
    re = []
    for item in REQ.POST:
        re.append(REQ.POST[item])
    print(re)
    return HttpResponse(1)