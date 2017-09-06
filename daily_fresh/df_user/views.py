from datetime import datetime, timedelta

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST, require_http_methods

from df_goods.models import BrowseHistory
from df_order.models import OrderBasic
from df_user.models import Passport, Address
from django.http import JsonResponse
from utils.decorators import login_required


@require_http_methods(['POST', 'GET'])
def register(request):
    if request.method == 'POST':
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')

        Passport.objects.add_one_passport(username=username, password=password, email=email)
        return redirect("/user/login/")

    return render(request, 'register.html')


@require_GET
def check_exist(request, checked):
    val = request.GET.get(checked)
    if checked == "email":
        ores = Passport.objects.get_one_passport(email=val)
    elif checked == "username":
        ores = Passport.objects.get_one_passport(username=val)
    else:
        ores = None
    res = 0 if ores else 1
    return JsonResponse({'res': res})


def login(request):
    if 'username' in request.COOKIES:
        username = request.COOKIES['username']
    else:
        username = ''
    return render(request, 'login.html', {'username': username})


def logout(request):
    request.session.flush()
    return redirect("/user/login/")


@require_POST
def login_check(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    passport = Passport.objects.get_one_passport(username=username, password=password)
    if passport:
        next_url = request.session.get('pre_url_path', '/')
        jres = JsonResponse({'res': 1, 'next': next_url})
        remember = request.POST.get('remember')
        if remember == 'true':
            jres.set_cookie('username', username, expires=datetime.now() + timedelta(days=14))
        request.session['is_login'] = True
        request.session['passport_id'] = passport.id
        request.session['username'] = username
        return jres
    return JsonResponse({"res": 0})


@login_required
def info(request):
    passport_id = request.session['passport_id']
    addr = Address.objects.get_default_address(passport_id=passport_id)
    history_list = BrowseHistory.objects.get_browse_history_img_list_by_passport(passport_id=passport_id, limit=5)
    return render(request, "user_center_info.html", {"addr": addr, "page": "user", "browse_list": history_list})


@require_http_methods(['GET', 'POST'])
@login_required
def address(request):
    passport_id = request.session['passport_id']
    if request.method == 'POST':
        recipicent_name = request.POST.get('uname')
        recipicent_addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        recipicent_phone = request.POST.get('phone')

        Address.objects.add_one_address(passport_id=passport_id, recipicent_name=recipicent_name,
                                        recipicent_addr=recipicent_addr, zip_code=zip_code,
                                        recipicent_phone=recipicent_phone, )
        return redirect("/user/address/")

    addr = Address.objects.get_default_address(passport_id=passport_id)
    addr_list = Address.objects.get_undefault_address(passport_id=passport_id)
    return render(request, 'user_center_site.html', {'addr_list': addr_list, 'addr': addr, 'page': 'addr'})


@require_GET
@login_required
def order(request, page_index=1):
    passport_id = request.session.get('passport_id')
    order_basic_list = OrderBasic.objects_img.get_order_basic_list_by_passport(passport_id=passport_id)
    paginator = Paginator(order_basic_list, 1)
    order_li =  paginator.page(int(page_index))
    num_pages = paginator.num_pages
    current_num = int(page_index)
    if num_pages <= 5:
        pages = range(1, num_pages + 1)
    elif current_num <= 3:
        pages = range(1, 6)
    elif num_pages - current_num <= 2:
        pages = range(num_pages - 4, num_pages + 1)
    else:
        pages = range(current_num - 2, current_num + 3)

    return render(request, 'user_center_order.html', {'page': 'order', 'pages': pages,
                                                      'order_basic_list': order_li})


@require_GET
@login_required
def modify_address(request, modify):
    passport_id = request.session['passport_id']
    address_id = request.GET.get('address_id')
    if modify == "set":
        res = Address.objects.change_default(passport_id=passport_id, address_id=address_id)
    elif modify == "del":
        res = Address.objects.del_address(passport_id=passport_id, address_id=address_id)
    else:
        res = None
    res = 0 if res else 1
    return JsonResponse({'res': res})
