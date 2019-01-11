from rest_framework import serializers
from .models import *

class MyUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ("id","emp_id","password","last_login","username","email","is_active","phone","emp_name","primission","department")

class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ["name","is_valid"]

