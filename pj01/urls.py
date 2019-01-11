from django.conf.urls import url
from .views import *
urlpatterns = [
    url(r"^register$",RegisterAPI.as_view()),
    url(r"^login$",LoginAPI.as_view()),
    url(r"^userc_d$",User_Change_DeleteAPI.as_view())
]