from django.db import models
import copy


class BaseModelManager(models.Manager):
    def get_all_valid_fields(self):
        model_class = self.model
        attr_list = model_class._meta.get_fields()
        str_attr_list = []
        for attr in attr_list:
            if isinstance(attr, models.ForeignKey):
                str_attr = '%s_id' % attr.name
            else:
                str_attr = attr.name
            str_attr_list.append(str_attr)
        return str_attr_list

    def create_one_object(self, **kwargs):
        valid_fields = self.get_all_valid_fields()
        kws = copy.copy(kwargs)
        for key in kws:
            if key not in valid_fields:
                kwargs.pop(key)
        model_class = self.model
        obj = model_class(**kwargs)
        obj.save()
        return obj

    def get_one_object(self, **filters):
        try:
            obj = self.get(**filters)
        except self.model.DoesNotExist:
            obj = None
        return obj

    def get_object_list(self, filters={}, exclude_filters={}, order_by=('-pk',)):
        object_list = self.filter(**filters).exclude(**exclude_filters).order_by(*order_by)
        return object_list

    def check_object_exist(self, **kwargs):
        object_list = self.get_object_list(filters=kwargs)
        return object_list.exists()

