from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET
from df_cart.models import Cart
from df_goods.models import Goods
from utils.decorators import login_required


@require_GET
@login_required
def cart_add(request):
    goods_id = request.GET.get('goods_id')
    goods_count = request.GET.get('goods_count')
    passport_id = request.session.get('passport_id')

    goods = Goods.objects.get_goods_by_id(goods_id=goods_id)
    if goods.goods_stock < int(goods_count):
        return JsonResponse({'res': 1})
    else:
        Cart.objects.add_one_cart_info(passport_id=passport_id,
                                       goods_id=goods_id, goods_count=int(goods_count))
        return JsonResponse({'res': 0})


@require_GET
@login_required
def cart_count(request):
    passport_id = request.session.get('passport_id')
    res = Cart.objects.get_cart_count_by_passport(passport_id=passport_id)
    return JsonResponse({'res': res})


@login_required
def cart_show(request):
    passport_id = request.session.get('passport_id')
    total_price = Cart.objects.cal_total_price(passport_id=passport_id)
    cart_list = Cart.objects_img.get_cart_list_by_passport(passport_id=passport_id)
    cart_counts = Cart.objects.get_cart_count_by_passport(passport_id=passport_id)
    return render(request, 'cart.html', {'cart_list': cart_list, 'cart_count': cart_counts, 'total_price': total_price})


@require_GET
@login_required
def cart_update(request):
    goods_id = request.GET.get('goods_id')
    goods_count = request.GET.get('goods_count')
    passport_id = request.session.get('passport_id')
    res = Cart.objects.update_cart_info_by_passport(passport_id=passport_id,
                                                    goods_id=goods_id, goods_count=int(goods_count))
    res = 0 if res else 1
    return JsonResponse({'res': res})


@require_GET
@login_required
def cart_del(request):
    goods_id = request.GET.get('goods_id')
    passport_id = request.session.get('passport_id')
    res = Cart.objects.del_cart_info(passport_id=passport_id, goods_id=goods_id)
    res = 0 if res else 1
    return JsonResponse({'res': res})

