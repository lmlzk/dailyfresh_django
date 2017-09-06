from django.conf.urls import url
from df_goods import views

urlpatterns = [
    url(r'^$', views.home_list_page),  # 显示网站首页内容
    url(r'^goods/(\d+)/$', views.goods_detail),  # 显示商品的详情信息
    url(r'^list/(\d+)/(\d+)/$', views.goods_list),  # 显示商品的列表页信息
    url(r'^get_image_list/$', views.get_image_list),
]
