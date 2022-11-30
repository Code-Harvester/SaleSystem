from django.db import models


# Create your models here.


class USER(models.Model):  # 用户表
    UserID = models.CharField(verbose_name='用户ID', max_length=16, primary_key=True)  # 用户ID
    UserName = models.CharField(verbose_name='用户姓名', max_length=16)  # 用户姓名
    Password = models.CharField(verbose_name='密码', max_length=64)  # 密码
    Sex = models.CharField(verbose_name='性别', max_length=2)  # 性别
    TEL = models.CharField(verbose_name='电话', max_length=16, null=True)  # 电话
    Identity = models.IntegerField(verbose_name='身份')  # 身份
    Note = models.CharField(verbose_name='备注', max_length=128, null=True)  # 备注


class GOODSINFO(models.Model):  # 商品信息表
    GoodID = models.CharField(verbose_name='商品编号', max_length=16, primary_key=True)  # 商品编号
    GoodName = models.CharField(verbose_name='商品名称', max_length=32)  # 商品名称
    Price = models.DecimalField(verbose_name='单价', max_digits=6, decimal_places=2)  # 单价
    Cost = models.DecimalField(verbose_name='成本', max_digits=6, decimal_places=2)  # 成本
    Type = models.CharField(verbose_name='类别', max_length=16)  # 类别
    Stock = models.IntegerField(verbose_name='库存')  # 当前库存
    QGPeriod = models.IntegerField(verbose_name='保质期')  # 保质期(年)
    Note = models.CharField(verbose_name='备注', max_length=128, null=True)  # 备注


class CHANGELOG(models.Model):  # 商品数量变更日志
    GoodID = models.CharField(verbose_name='商品编号', max_length=16)  # 商品编号
    Time = models.DateTimeField(verbose_name='变更日期')  # 变更日期
    Add = models.IntegerField(verbose_name='添加数量')  # 添加数量
    Loss = models.IntegerField(verbose_name='损耗数量')  # 损耗数量
    UserID = models.CharField(verbose_name='变更人ID', max_length=16)  # 变更人ID
    Note = models.CharField(verbose_name='备注', max_length=128, null=True)  # 备注

    class Meta:
        unique_together = ("GoodID", "Time")  # 唯一性约束


class SALE(models.Model):  # 销售表
    GoodID = models.CharField(verbose_name='商品编号', max_length=16)  # 商品编号
    Time = models.DateTimeField(verbose_name='销售日期')  # 销售日期
    Mount = models.IntegerField(verbose_name='销售数量')  # 销售数量
    UserID = models.CharField(verbose_name='销售人员ID', max_length=16)  # 销售人员ID

    class Meta:
        unique_together = ("GoodID", "Time")  # 唯一性约束
