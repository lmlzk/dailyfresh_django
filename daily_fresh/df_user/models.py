from django.db import models
from db.base_manager import BaseModelManager
from db.base_model import BaseModel
from utils.get_hash import get_hash


class PassportManger(BaseModelManager):
    def add_one_passport(self, username, password, email):
        passport = self.model()
        passport.username = username
        passport.password = get_hash(password)
        passport.email = email
        passport.save()
        return passport

    def get_one_passport(self, username=None, password=None, email=None):
        try:
            if email is not None:
                passport = self.get(email=email)
            elif password is None:
                passport = self.get(username=username)
            else:
                passport = self.get(username=username, password=get_hash(password))
        except:
            passport = None
        return passport


class Passport(BaseModel):
    username = models.CharField(max_length=20, unique=True, verbose_name="用户名")
    password = models.CharField(max_length=40, verbose_name="密码")
    email = models.EmailField(verbose_name="邮箱", unique=True)

    objects = PassportManger()

    class Meta:
        db_table = 's_user_account'


class AddressManager(BaseModelManager):
    def get_default_address(self, passport_id):
        def_addr = self.get_one_object(passport_id=passport_id, is_def=True, is_delete=False)
        return def_addr

    def get_all_address(self, passport_id):
        addr_list = self.filter(passport_id=passport_id, is_delete=False)
        return addr_list

    def get_undefault_address(self, passport_id):
        addr_list = self.get_object_list(filters={'passport_id': passport_id, 'is_delete': False},
                                         exclude_filters={'is_def': True})
        return addr_list

    def change_default(self, passport_id, address_id):
        change_add = self.get_one_object(id=address_id)
        if change_add:
            self.get_all_address(passport_id).update(is_def=False)
            change_add.is_def = True
            change_add.save()
            return True
        return False

    def add_one_address(self, passport_id, recipicent_name, recipicent_addr, zip_code, recipicent_phone, is_def=False):
        def_addr = self.get_default_address(passport_id=passport_id)
        if def_addr is None:
            is_def = True
        address = self.create_one_object(
            passport_id=passport_id, recipicent_name=recipicent_name,
            recipicent_addr=recipicent_addr, zip_code=zip_code,
            recipicent_phone=recipicent_phone, is_def=is_def)
        return address

    def del_address(self, passport_id, address_id):
        del_add = self.get_one_object(id=address_id)
        if del_add:
            del_add.is_delete = True
            if del_add.is_def:
                del_add.is_def = False
                new_default_li = self.get_undefault_address(passport_id)
                if new_default_li.exists():
                    def_id = new_default_li[0].id
                    self.change_default(passport_id=passport_id, address_id=def_id)
            del_add.save()
            return True
        return False


class Address(BaseModel):
    passport = models.ForeignKey('Passport', verbose_name='所属账户')
    recipicent_name = models.CharField(max_length=20, verbose_name='收件人')
    recipicent_addr = models.CharField(max_length=256, verbose_name='收件地址')
    zip_code = models.CharField(max_length=6, verbose_name='邮编')
    recipicent_phone = models.CharField(max_length=11, verbose_name='联系电话')
    is_def = models.BooleanField(default=False, verbose_name='是否默认')

    objects = AddressManager()

    class Meta:
        db_table = 's_user_address'
