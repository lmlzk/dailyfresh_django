from django.db import models
from django.db.models import Sum
from db.base_manager import BaseModelManager
from db.base_model import BaseModel
from df_goods.models import Image


class CartManager(BaseModelManager):
    def get_one_cart_info(self, passport_id, goods_id):
        cart_info = self.get_one_object(passport_id=passport_id, goods_id=goods_id, is_delete=False)
        return cart_info

    def add_one_cart_info(self, passport_id, goods_id, goods_count):
        cart_info = self.get_one_cart_info(passport_id=passport_id, goods_id=goods_id)
        if cart_info:
            cart_info.goods_count += goods_count
            cart_info.save()
        else:
            cart_info = self.create_one_object(passport_id=passport_id, goods_id=goods_id, goods_count=goods_count)
        return cart_info

    def get_cart_count_by_passport(self, passport_id):
        res_dict = self.get_object_list(filters={'passport_id': passport_id, 'is_delete': False})\
            .aggregate(Sum('goods_count'))
        res = res_dict['goods_count__sum']
        return res if res else 0

    def get_cart_list_by_passport(self, passport_id):
        cart_list = self.get_object_list(filters={'passport_id': passport_id, 'is_delete': False})
        return cart_list

    def update_cart_info_by_passport(self, passport_id, goods_id, goods_count):
        cart_info = self.get_one_cart_info(passport_id=passport_id, goods_id=goods_id)
        if cart_info:
            if cart_info.goods.goods_stock >= goods_count:
                cart_info.goods_count = goods_count
                cart_info.save()
                return True
            return False
        self.add_one_cart_info(passport_id=passport_id, goods_id=goods_id, goods_count=goods_count)
        return True

    def update_price(self, passport_id):
        cart_list = self.get_object_list(filters={'passport_id': passport_id, 'is_delete': False})
        if not cart_list.exists():
            return False
        for cart in cart_list:
            cart.price = cart.goods_count * cart.goods.goods_price
            cart.save()
        return True

    def cal_total_price(self, passport_id):
        self.update_price(passport_id)
        res_dict = self.get_object_list(filters={'passport_id': passport_id, 'is_delete': False})\
                    .aggregate(total=Sum('price'))
        res = res_dict.get('total')
        return res if res else 0

    def del_cart_info(self, passport_id, goods_id):
        cart_info = self.get_one_cart_info(passport_id=passport_id, goods_id=goods_id)
        if cart_info:
            cart_info.is_delete = True
            cart_info.save()
            return True
        return False

    def get_cart_list_by_goods_id_list(self, passport_id, goods_id_list):
        cart_list = self.get_object_list(filters={'passport_id': passport_id, 'goods_id__in': goods_id_list})
        return cart_list

    def get_goods_count_and_amout_by_id_list(self, passport_id, goods_id_list):
        total_count, total_price = 0, 0
        cart_list = self.get_cart_list_by_goods_id_list(passport_id=passport_id, goods_id_list=goods_id_list)
        for cart_info in cart_list:
            total_count += cart_info.goods_count
            total_price += cart_info.goods_count*cart_info.goods.goods_price
        return total_count, total_price


class CartImgManager(CartManager):
    def get_cart_list_by_passport(self, passport_id):
        cart_list = super().get_cart_list_by_passport(passport_id=passport_id)
        for cart_info in cart_list:
            img = Image.objects.get_img_by_goods_id(goods_id=cart_info.goods_id)
            cart_info.goods.img_url = img.img_url
        return cart_list

    def get_cart_list_by_goods_id_list(self, passport_id, goods_id_list):
        cart_list = super().get_cart_list_by_goods_id_list(passport_id=passport_id, goods_id_list=goods_id_list)
        for cart_info in cart_list:
            img = Image.objects.get_img_by_goods_id(goods_id=cart_info.goods_id)
            cart_info.goods.img_url = img.img_url
        return cart_list



class Cart(BaseModel):
    passport = models.ForeignKey('df_user.Passport', verbose_name='用户')
    goods = models.ForeignKey('df_goods.Goods', verbose_name='商品')
    goods_count = models.IntegerField(default=1, verbose_name='商品数目')
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name='小计')

    objects = CartManager()
    objects_img = CartImgManager()

    class Meta:
        db_table = 's_cart'
