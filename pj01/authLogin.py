from django.core.cache import caches
from rest_framework.authentication import BaseAuthentication

from .models import MyUser
user_cache = caches["default"]


class LoginAuthAPI(BaseAuthentication):
    def authenticate(self, request):
        #拿token
        token = request.query_params.get("token")
        #去缓存看看有没有
        u_id = user_cache.get(token)
        if u_id:
            user = MyUser.objects.get(pk=int(u_id))
        #如果有返回一个元组
            return (user,token)
        else:
            return (None,None)