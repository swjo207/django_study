from django.db import models
from django.core.exceptions import ObjectDoesNotExist

###
#   PositiveIntegerField 를 상속 받는다.
#   for_fields 파라미터를 추가로 받아서 정렬 대상을 지정함
#
class OrderField(models.PositiveIntegerField):

    def __init__(self,for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super(OrderField,self).__init__(*args,**kwargs)

    def pre_save(self,model_instance,add):
        if getattr(model_instance,self.attname) is None:
            # no current value
            try:
                querysets = self.model.objects.all()
                if self.for_fields:
                    # filter by objects with the same field values
                    # for the fields in "for_fields"
                    query = {field: getattr(model_instance, field) for field in self.for_fields}
                    querysets = querysets.filter(**query)
                # get the order of the last item
                last_item = querysets.latest(self.attname)
                value = last_item.order + 1
            except ObjectDoesNotExist:
                value = 0
            setattr(model_instance,self.attname,value)
            return value
        else:
            return super(OrderField,self).pre_save(model_instance,add)

