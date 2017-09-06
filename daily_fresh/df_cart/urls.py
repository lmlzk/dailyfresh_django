from django.conf.urls import url
from df_cart import views

urlpatterns = [
    url(r'^add/$', views.cart_add),
    url(r'update', views.cart_update),
    url(r'^count/$', views.cart_count),
    url(r'^del_cart_goods/$', views.cart_del),
    url(r'^$', views.cart_show),
]
