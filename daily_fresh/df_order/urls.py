from django.conf.urls import url
from df_order import views

urlpatterns = [
    url(r'^$', views.order_place),
    url(r'^commit/$', views.order_commit),
]