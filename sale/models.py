from django.db import models


# Create your models here.


class USER(models.Model):  # 用户表
    UserID = models.IntegerField(primary_key=True)  # 用户ID
    UserName = models.CharField(max_length=16)  # 用户姓名
    Password = models.CharField(max_length=64)  # 密码
    Sex = models.CharField(max_length=2)  # 性别
    TEL = models.CharField(max_length=16)  # 电话
    Identity = models.IntegerField()  # 身份
    Note = models.CharField(max_length=128, null=True)  # 备注


class GOODSINFO(models.Model):  # 商品信息表
    GoodID = models.IntegerField(primary_key=True)  # 商品编号
    GoodName = models.CharField(max_length=32)  # 商品名称
    Price = models.IntegerField()  # 单价
    Cost = models.IntegerField()  # 成本
    Type = models.CharField(max_length=16)  # 类别
    Stock = models.IntegerField()  # 当前库存
    QGPeriod = models.DateTimeField()  # 保质期
    Note = models.CharField(max_length=128, null=True)  # 备注


class CHANGELOG(models.Model):  # 商品数量变更日志
    GoodID = models.IntegerField()  # 商品编号
    Time = models.DateTimeField()  # 变更日期
    Add = models.IntegerField()  # 添加数量
    Loss = models.IntegerField()  # 损耗数量
    UserID = models.IntegerField()  # 变更人ID
    Note = models.CharField(max_length=128, null=True)  # 备注

    class Meta:
        unique_together = ("GoodID", "Time")  # 唯一性约束


class SALE(models.Model):  # 销售表
    GoodID = models.IntegerField()  # 商品编号
    Time = models.DateTimeField()  # 销售日期
    Mount = models.IntegerField()  # 销售数量
    UserID = models.IntegerField()  # 销售人员ID

    class Meta:
        unique_together = ("GoodID", "Time")  # 唯一性约束
