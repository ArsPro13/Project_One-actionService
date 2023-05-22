from django.db import models
import json
# Create your models here.

class ServiceDB(models.Model):
    serv_name = models.CharField(max_length = 50)
    serv_record_id = models.IntegerField()
    content = models.TextField()

def storage_get(serv_name, serv_record_id):
    try:
        return ServiceDB.objects.get(serv_name = serv_name, serv_record_id = serv_record_id);
    except ObjectDoesNotExist:
        print("Объект не сушествует")
    except MultipleObjectsReturned:
        print("Найдено более одного объекта")

def storage_set(serv_name, serv_record_id, value):
    object = ServiceDB.objects.get_or_create(serv_name=serv_name, serv_record_id=serv_record_id)
    object.content = json.dumps(value)
    object.save()
