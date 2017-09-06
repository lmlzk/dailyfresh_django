from django.conf.urls import url
from df_user import views

urlpatterns = [
    url(r'^register/$', views.register),
    url(r'^check_(\w+)_exist/$', views.check_exist),

    url(r'^login/$', views.login),
    url(r'^login_check/$', views.login_check),
    url(r'^logout/$', views.logout),

    url(r'^info/$', views.info),
    url(r'^address/$', views.address),
    url(r'^order/(\d+)/$', views.order),
    url(r'^order/$', views.order),

    # url(r'^set_address/$', views.set_default),
    url(r'^(\w+)_address/$', views.modify_address),
]