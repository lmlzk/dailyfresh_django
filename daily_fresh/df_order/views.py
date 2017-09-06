from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.db import transaction
from df_cart.models import Cart
from df_order.models import OrderBasic, OrderDetail
from df_user.models import Address
from utils.decorators import login_required
from utils.to_tri import to_tri


@login_required
@require_POST
def order_place(request):
    passport_id = request.session.get('passport_id')
    addr = Address.objects.get_default_address(passport_id=passport_id)
    goods_id_list = request.POST.getlist('goods_id_list')
    cart_list = Cart.objects_img.get_cart_list_by_goods_id_list(passport_id=passport_id, goods_id_list=goods_id_list)
    goods_id_list = ','.join(goods_id_list)

    return render(request, 'place_order.html', {'cart_list': cart_list, 'addr': addr, 'goods_id_list': goods_id_list})


@require_POST
@login_required
@transaction.atomic
def order_commit(request):
    addr_id = request.POST.get('addr_id')
    pay_method = request.POST.get('pay_method')
    goods_id_list = request.POST.get('goods_id_list')
    passport_id = request.session.get('passport_id')

    order_id = datetime.now().strftime('%Y%m%d%H%M%S') + to_tri(passport_id)
    transit_price =10.0

    goods_id_list = goods_id_list.split(',')
    total_count, total_price = Cart.objects.get_goods_count_and_amout_by_id_list(passport_id=passport_id, goods_id_list=goods_id_list)

    save_id =transaction.savepoint()
    try:
        OrderBasic.objects.add_one_order_basic_info(order_id=order_id, passport_id=passport_id,
                                                    addr_id=addr_id, total_count=total_count,
                                                    total_price=total_price, transit_price=transit_price,
                                                    pay_method=pay_method)
        cart_list = Cart.objects.get_cart_list_by_goods_id_list(passport_id=passport_id, goods_id_list=goods_id_list)
        for cart_info in cart_list:
            if cart_info.goods_count < cart_info.goods.goods_stock:
                goods_id = cart_info.goods.id
                goods_count = cart_info.goods_count
                goods_price = cart_info.goods.goods_price
                OrderDetail.objects.add_one_order_detail_info(order_id=order_id, goods_id=goods_id,
                                                              goods_count=goods_count, goods_price=goods_price)
                cart_info.goods.goods_stock -= cart_info.goods_count
                cart_info.goods.goods_sales += cart_info.goods_count

                cart_info.delete()
            else:
                transaction.savepoint_rollback(save_id)
                return JsonResponse({'res': 1, 'content': '库存不足'})
    except Exception as e:
        transaction.savepoint_rollback(save_id)
        return JsonResponse({'res': 1, 'content': '服务器错误'})
    transaction.savepoint_commit(save_id)
    return JsonResponse({'res': 0})
