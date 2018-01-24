from django.db import models
from django.db.models.base import ModelBase

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField

    @classmethod
    def get_sharding_table(cls, id=None):
        piece = id
        return cls._meta.db_table + str(piece)

    @classmethod
    def sharding_get(cls, id=None, **kwargs):
        assert isinstance(id, int), 'id must be integer!'
        table = cls.get_sharding_table(id)
        sql = "SELECT * FROM %s" % table
        # kwargs['id'] = id
        condition = ' AND '.join([k + '=%s' for k in kwargs])
        params = [str(v) for v in kwargs.values()]
        where = " WHERE " + condition

        try:
            return cls.objects.raw(sql + where, params=params)  # the5fire:这里应该模仿Queryset中get的处理方式
        except IndexError:
            # the5fire:其实应该抛Django的那个DoesNotExist异常
            return None

    @classmethod
    def sharding_listAll(cls, id=None):
        assert isinstance(id, int), 'id must be integer!'
        table = cls.get_sharding_table(id)
        sql = "SELECT * FROM %s" % table
        try:
            return cls.objects.raw(sql)  # the5fire:这里应该模仿Queryset中get的处理方式
        except IndexError:
            # the5fire:其实应该抛Django的那个DoesNotExist异常
            return None


    class Meta:
        db_table = 'user_'
        app_label = 'HelloWorld'


