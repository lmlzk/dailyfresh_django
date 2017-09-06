from django.db import models
from tinymce.models import HTMLField
from db.base_manager import BaseModelManager
from db.base_model import BaseModel
from df_goods.enums import *
from df_user.models import Passport


class GoodsManager(BaseModelManager):
    def get_goods_by_id(self, goods_id):
        goods = self.get_one_object(id=goods_id)
        return goods

    def get_goods_list_by_type(self, goods_type_id, limit=None, sort="default"):
        if sort == "new":
            order_by = ('-create_time',)
        elif sort == "price":
            order_by = ('goods_price',)
        elif sort == "hot":
            order_by = ('-goods_sales',)
        else:
            order_by = ('pk',)
        goods_list = self.get_object_list(filters={'goods_type_id': goods_type_id}, order_by=order_by)
        if limit:
            goods_list = goods_list[:limit]
        return goods_list


class GoodsImgManager(GoodsManager):
    def get_goods_by_id(self, goods_id):
        goods = super().get_goods_by_id(goods_id=goods_id)
        if goods:
            img = Image.objects.get_img_by_goods_id(goods_id=goods_id)
            goods.img_url = img.img_url
        return goods

    def get_goods_list_by_type(self, goods_type_id, limit=None, sort="default"):
        goods_list = super().get_goods_list_by_type(goods_type_id=goods_type_id, limit=limit, sort=sort)
        for goods in goods_list:
            img = Image.objects.get_img_by_goods_id(goods_id=goods.id)
            goods.img_url = img.img_url
        return goods_list


class Goods(BaseModel):
    goods_type_choice = [
        (FRUIT, GOODS_TYPE[FRUIT]),
        (SEAFOOD, GOODS_TYPE[SEAFOOD]),
        (MEAT, GOODS_TYPE[MEAT]),
        (EGGS, GOODS_TYPE[EGGS]),
        (VEGETABLES, GOODS_TYPE[VEGETABLES]),
        (FROZEN, GOODS_TYPE[FROZEN])
    ]

    goods_type_id = models.SmallIntegerField(choices=goods_type_choice, default=FRUIT, verbose_name='商品类型id')
    goods_name = models.CharField(max_length=20, verbose_name="商品名称")
    goods_desc = models.CharField(max_length=256, verbose_name="商品描述")
    goods_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="商品价格")
    transit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品运费')
    goods_unite = models.CharField(max_length=20, verbose_name="商品单位")
    goods_info = HTMLField(verbose_name="商品详情")
    goods_stock = models.IntegerField(default=0, verbose_name="商品库存")
    goods_sales = models.IntegerField(default=0, verbose_name="商品销量")
    goods_status = models.SmallIntegerField(default=1, verbose_name="商品状态")

    objects = GoodsManager()
    objects_image = GoodsImgManager()

    class Meta:
        db_table = 's_goods'


class ImageManger(BaseModelManager):
    def get_img_by_goods_id(self, goods_id):
        imgs = self.get_object_list(filters={'goods_id': goods_id})
        if imgs.exists():
            imgs = imgs[0]
        else:
            imgs.img_url = ''
        return imgs

    def get_img_by_goods_id_list(self, goods_id_list):
        images = self.get_object_list(filters={'goods_id__in': goods_id_list})
        return images


class Image(BaseModel):
    goods = models.ForeignKey('Goods', verbose_name="所属商品")
    img_url = models.ImageField(upload_to="/images/goods/", verbose_name="图片路径")
    is_def = models.BooleanField(default=False, verbose_name="是否默认")

    objects = ImageManger()

    class Meta:
        db_table = 's_goods_image'


class BrowseHistoryManager(BaseModelManager):
    def get_one_history(self, passport_id, goods_id):
        history = self.get_one_object(passport_id=passport_id, goods_id=goods_id)
        return history

    def add_one_history(self, passport_id, goods_id):
        history = self.get_one_history(passport_id, goods_id)
        if history:
            history.save()
        else:
            self.create_one_object(passport_id=passport_id, goods_id=goods_id)

    def get_browse_history_img_list_by_passport(self, passport_id, limit=None):
        history_list = self.get_object_list(filters={"passport_id": passport_id}, order_by=("-update_time",))
        if limit:
            history_list = history_list[:limit]
        for his in history_list:
            his.goods.img_url = Image.objects.get_img_by_goods_id(goods_id=his.goods_id).img_url
        return history_list


class BrowseHistory(BaseModel):
    goods = models.ForeignKey('Goods', verbose_name="所属商品")
    passport = models.ForeignKey('df_user.Passport', verbose_name="所属用户")

    objects = BrowseHistoryManager()

    class Meta:
        db_table = 's_browse_history'

