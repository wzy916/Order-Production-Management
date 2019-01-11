from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class GongYluXian(models.Model):
    proc_name = models.CharField(
        max_length=255
    )
    dep_id = models.CharField(
        max_length=50
    )
    is_valid = models.BooleanField(
    )

class BanChengP(models.Model):
    b_id = models.CharField(
        max_length=20,
        verbose_name="半成品编号",
        unique=True
    )
    b_name = models.CharField(
        max_length=30,
        verbose_name="半成品名称"
    )
    count = models.IntegerField(
        verbose_name="数量"
    )
    is_valid = models.BooleanField(
        default=True,
        verbose_name="是否有效"
    )
    m_id = models.CharField(
        max_length=255,
        verbose_name="毛坯id"
    )
    class Meta:
        verbose_name = "半成品仓库信息"

class Maopi(models.Model):
    m_id = models.CharField(
        max_length=100,
        verbose_name="毛坯编号",
        unique=True
    )
    m_name = models.CharField(
        max_length=30,
        verbose_name="毛坯名称"
    )
    count = models.IntegerField(
        verbose_name="货存数量"
    )
    is_valid = models.BooleanField(
        default=True,
        verbose_name="是否有效"
    )
    banchengpin = models.ManyToManyField(
        BanChengP,
    )
    class Meta:
        verbose_name="毛坯仓库信息"

class Customer(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name="客户名称"
    )
    is_valid = models.BooleanField(
        default=True,
        verbose_name="是否有效"
    )
    class Meta:
        verbose_name = "客户信息"


class Department(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name="部门名字"
    )
    is_valid = models.BooleanField(
        default=True,
        verbose_name="是否有效"
    )
    class Meta:
        verbose_name = "部门信息"

class MyUser(AbstractUser):#继承自AbstractUser
   emp_id = models.CharField(
       max_length=20,
       verbose_name="员工编号",
       null = False
   )
   emp_name = models.CharField(
       max_length=20,
       verbose_name="员工姓名",
   )
   department = models.ForeignKey(
       Department,
       verbose_name="所属部门",
   )
   primission = models.CharField(
       max_length = 50,
       verbose_name="所有权限"
   )
   phone = models.CharField(
       max_length=30,
       verbose_name="电话"
   )
   class Meta:
       verbose_name = "员工信息"

class Sales_order(models.Model):
    order_id = models.CharField(
        max_length=30,
        verbose_name="订单编号",
        null=False,
        unique=True
    )
    is_valid = models.BooleanField(
       default=True,
        verbose_name="是否有效"
    )
    user_id = models.ForeignKey(
        MyUser,
        max_length=30,
        verbose_name="员工id"
    )
    customer = models.ForeignKey(
        Customer,
        verbose_name="客户id"
    )
    phase = models.IntegerField(
        verbose_name="预计生产周期"
    )
    is_done = models.BooleanField(
        default=False,
        verbose_name="订单是否完成"
    )
    si_stop = models.BooleanField(
        default=False,
        verbose_name="暂停订单"
    )
    quantity = models.IntegerField(
        verbose_name="订单数量"
    )
    f_data = models.DateTimeField(
        verbose_name="完成日期"
    )
    s_data = models.DateTimeField(
        auto_now_add=True,
        verbose_name="下单日期"
    )
    process_id = models.CharField(
        max_length=30
    )
    class Meta:
        verbose_name = "订单销售信息"



class DingDanlcsj(models.Model):
    sales_order = models.ForeignKey(
        Sales_order,
        verbose_name="订单编号"
    )
    departmen = models.ForeignKey(
        Department,
        verbose_name="到达部门的id"
    )
    dep_date = models.DateField(
        verbose_name="到达当前部门的时间"
    )
    dep_count = models.IntegerField(
        verbose_name="到哪数量"
    )
    is_valid = models.BooleanField(
        default=True
    )
    class Meta:
        verbose_name = "订单流程时间信息"

class order_pruduct(models.Model):
    maopi = models.ForeignKey(
        Maopi,
        to_field = "m_id"
    )
    banchengp = models.ForeignKey(
        BanChengP,
        to_field ="b_id"
    )
    sales_order = models.ForeignKey(
        Sales_order,
        to_field="order_id"
    )
    gongyluxian = models.ForeignKey(
        GongYluXian
    )
    class Meta:
        verbose_name = "订单产品"



