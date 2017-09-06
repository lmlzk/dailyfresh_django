from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from df_cart.models import Cart
from df_goods.models import Goods, BrowseHistory, Image
from df_goods.enums import *


def get_cart_count(request):
    if request.session.has_key('is_login'):
        passport_id = request.session.get('passport_id')
        cart_count = Cart.objects.get_cart_count_by_passport(passport_id=passport_id)
    else:
        cart_count = 0
    return cart_count


def home_list_page(request):
    # 1.获取每一个种类的3个新品信息和4个普通商品信息
    fruits_new = Goods.objects.get_goods_list_by_type(goods_type_id=FRUIT, limit=3, sort='new')
    fruits = Goods.objects_image.get_goods_list_by_type(goods_type_id=FRUIT, limit=4)

    seafood_new = Goods.objects.get_goods_list_by_type(goods_type_id=SEAFOOD, limit=3, sort='new')
    seafood = Goods.objects_image.get_goods_list_by_type(goods_type_id=SEAFOOD, limit=4)

    meat_new = Goods.objects.get_goods_list_by_type(goods_type_id=MEAT, limit=3, sort='new')
    meat = Goods.objects_image.get_goods_list_by_type(goods_type_id=MEAT, limit=4)

    eggs_new = Goods.objects.get_goods_list_by_type(goods_type_id=EGGS, limit=3, sort='new')
    eggs = Goods.objects_image.get_goods_list_by_type(goods_type_id=EGGS, limit=4)

    vegetables_new = Goods.objects.get_goods_list_by_type(goods_type_id=VEGETABLES, limit=3, sort='new')
    vegetables = Goods.objects_image.get_goods_list_by_type(goods_type_id=VEGETABLES, limit=4)

    frozen_new = Goods.objects.get_goods_list_by_type(goods_type_id=FROZEN, limit=3, sort='new')
    frozen = Goods.objects_image.get_goods_list_by_type(goods_type_id=FROZEN, limit=4)

    cart_count = get_cart_count(request)

    context = {'fruits_new': fruits_new, 'fruits': fruits,
               'seafood_new': seafood_new, 'seafood': seafood,
               'meat_new': meat_new, 'meat': meat,
               'eggs_new': eggs_new, 'eggs': eggs,
               'vegetables_new': vegetables_new, 'vegetables': vegetables,
               'frozen_new': frozen_new, 'frozen': frozen,
               'cart_count': cart_count}
    return render(request, 'index.html', context)


def goods_detail(request, goods_id):
    if not Goods.objects.check_object_exist(id=goods_id):
        return redirect("/goods/")
    goods = Goods.objects_image.get_goods_by_id(goods_id=goods_id)
    goods_new_li = Goods.objects_image.get_goods_list_by_type(goods_type_id=goods.goods_type_id, limit=2, sort='new')
    type_title = GOODS_TYPE[goods.goods_type_id]
    if request.session.has_key('is_login'):
        passport_id = request.session.get('passport_id')
        BrowseHistory.objects.add_one_history(passport_id=passport_id, goods_id=goods_id)
    cart_count = get_cart_count(request)
    return render(request, 'detail.html', {'goods': goods,
                                           'goods_new_li': goods_new_li,
                                           'type_title': type_title,
                                           'type_id': goods.goods_type_id,
                                           'cart_count': cart_count
                                           })


# /list/1/1/?sort=排序方式
def goods_list(request, goods_type_id, page_index):
    cart_count = get_cart_count(request)
    # 0.获取排序方式sort
    sort = request.GET.get('sort', 'default')
    # 1.根据商品类型id获取商品信息
    goods_li = Goods.objects_image.get_goods_list_by_type(goods_type_id=goods_type_id, sort=sort)

    # 2.进行分页
    paginator = Paginator(goods_li, 2)

    # 3.获取第pindex页的内容
    goods_li = paginator.page(int(page_index)) # goods_li是一个Page对象

    # 4.获取页码列表
    pages = paginator.page_range

    num_pages = paginator.num_pages
    current_num = int(page_index)
    # 总页数<=5
    # 如果当前页是前3页
    # 如果当前页是后3页
    # 既不是前3页也不是后3页 3 4 5 6 7
    if num_pages <= 5:
        pages = range(1, num_pages + 1)
    elif current_num <= 3:
        pages = range(1, 6)
    elif num_pages - current_num <= 2:
        pages = range(num_pages - 4, num_pages + 1)
    else:
        pages = range(current_num - 2, current_num + 3)

    # 6.获取商品的2个新品信息
    goods_new_li = Goods.objects_image.get_goods_list_by_type(goods_type_id=goods_type_id, limit=2, sort='new')
    # 7.获取商品种类标题
    type_title = GOODS_TYPE[int(goods_type_id)]

    return render(request, 'list.html', {'goods_li': goods_li,
                                         'goods_new_li': goods_new_li,
                                         'type_title': type_title,
                                         'type_id': goods_type_id,
                                         'sort': sort,
                                         'pages': pages,
                                         'cart_count': cart_count})


def get_image_list(request):
    goods_id_list = request.GET.get('goods_id_list')
    goods_id_list = goods_id_list.split(',')
    images = Image.objects.get_img_by_goods_id_list(goods_id_list=goods_id_list)
    img_dict = {}
    for image in images:
        img_dict[image.goods.id] = image.img_url.name
    return JsonResponse({'img_dict': img_dict})

