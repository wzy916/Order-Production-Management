import uuid
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from django.conf import settings
from .authLogin import LoginAuthAPI
from .serializer import MyUserSerializer
from .models import *
from django.contrib.auth import get_user_model, authenticate
from django.core.cache import caches
MyUser = get_user_model()

#注册
class RegisterAPI(ListCreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    def create(self, request, *args, **kwargs):
        confirm_pwd = request.data.get("u_confirm_pwd")
        password = request.data.get("password")
        if len(password)<3 or confirm_pwd!=password:
            res = {
                "code":2,
                "msg":"密码过短或确认密码不一致"
            }
            return Response(res)
        if  len(request.data.get("username")) == 0:
            return Response({"code":1,"msg":"用户名不能为空"})
        if MyUser.objects.filter(username=request.data.get("username")).exists():
            res = {
                "code":3,
                "msg":"该用户已经存在"
            }
            return Response(res)
        serializer = MyUserSerializer(data=request.data)
        serializer.is_valid()
        instance = serializer.save()
        instance.set_password(password)
        instance.is_active=1
        instance.save()
        new_serializer = self.get_serializer(instance)
        return Response(new_serializer.data, status=status.HTTP_201_CREATED)
    def get(self, request, *args, **kwargs):
        # queryset = self.filter_queryset(self.get_queryset())
        # queryset  = self.get_queryset()
        # queryset = queryset.order_by("-id")
        serializer = self.get_serializer(self.queryset.all(), many=True)
        return Response(serializer.data)

#登录
user_cache = caches["default"]
class LoginAPI(ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        #原来的post的是创建数据的
        #解析参数
        uname = request.data.get("username")
        print(uname)
        pwd = request.data.get("password")
        print(pwd)
        #做检验
        user = authenticate(username=uname,password=pwd)
        print(user)
        if user:
            token = uuid.uuid4().hex
            user_cache.set(token,user.id,settings.SET_TIME_CACHE)
            res = {
                "code":0,
                "msg":"登录成功",
                "data":{
                    "token":token
                }
            }
            return Response(res)
        else:
            res = {
                "code":1,
                "msg":"密码或用户名不正确"
            }
            return Response(res)

#修改密码,用户逻辑删除
class User_Change_DeleteAPI(RetrieveUpdateDestroyAPIView):
    authentication_classes = (LoginAuthAPI,)
    def put(self, request, *args, **kwargs):
        user = request.user
        new_pwd = request.data.get("n_password")
        user.password = user.set_password(new_pwd)
        user.save()
        res = {
            "code":0,
            "msg":"密码修改成功"
        }
        return Response(res)

    def delete(self, request, *args, **kwargs):
        user = request.user
        if user.primission == "1":
            uname = request.data.get("username")
            user1 = MyUser.objects.filter(username=uname)[0]
            user1.is_active = 0
            user1.save()
            res = {
                "code":0,
                "msg":"该用户已删除"
            }
            return Response(res)
        else:
            res = {
                "code":1,
                "msg":"删除失败"
            }
            return Response(res)
# c65ce3e755e241ada9fff3a15f6c5168

#根据仓库产品编号等条件查询现有库存






