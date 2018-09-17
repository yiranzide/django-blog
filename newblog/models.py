from django.db import models
from django.db import connection, transaction


# Create your models here.
# 定义数据结构
# class Models(object):
#     # 成功则提交事务，否则回滚
#     # 所有工作完成后，才会提交事务。
#     @transaction.atomic
#     def update(self, *args, **kwargs):
#         cursor = connection.cursor()    #获得一个游标(cursor)对象
#         model = self.__class__.__name__
#         print('start')
#         sql = '''
#               UPDATE
#                   %s
#               SET
#                   %s = %s
#               WHERE
#                   id = %s
#         '''
#         for k, v in kwargs:
#             cursor.execute(sql, [model, k, v, kwargs['id']])   #执行SQL
#         # set_dirty() 确保 Django 知道哪些修改必须被提交。
#         transaction.set_dirty()
#         return




class User(models.Model):
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=10)


class Blog(models.Model):
    title = models.CharField(max_length=20)
    content = models.CharField(max_length=200)
    pic = models.ImageField(upload_to='blogpic/')
    authorId = models.IntegerField()
    isDelete = models.BooleanField(default=1)
    count = models.IntegerField(default=0)
    readcount = models.ImageField(default=0)

    # 用事务提交
    @transaction.atomic
    def update(self, *args, **kwargs):
        cursor = connection.cursor()  # 获得一个游标(cursor)对象
        model = 'newblog_' + self.__class__.__name__.lower()
        sql = '''
                  UPDATE
                      {}
                  SET
                      %s = '%s'
                  WHERE
                      id = {}
            '''
        sql = sql.format(model, kwargs['id'])
        del kwargs['id']
        for k, v in kwargs.items():
            if k == 'pic':
                v = 'blogpic/{}'.format(v)
            # newsql = sql % (k, v)
            cursor.execute(sql, [k, v])  # 执行SQL
            cursor.close()


class Comment(models.Model):
    context = models.CharField(max_length=200)
    user_id = models.IntegerField()
    blog_id = models.IntegerField()