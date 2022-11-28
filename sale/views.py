from django.shortcuts import render, HttpResponse
import MySQLdb

i = 1


# Create your views here.

def OpenDB():
    conn = MySQLdb.connect(
        host='localhost',
        port=3306,
        user='root',
        db='salesys',
        password='123456',
        charset='utf8'
    )
    cur = conn.cursor()
    sql = 'select * from sale_user'
    cur.execute(sql)
    print(cur.fetchall())
    cur.close()
    conn.close()


def test(REQ):
    OpenDB()
    return HttpResponse('欢迎')


def login(REQ):
    if REQ.method == 'GET':
        return render('login.html')


def sale(REQ):
    pass

def statistics():
    pass