from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, User

# Create your models here.


# todo 自定义权限
# permission = Permission.objects.create(
#     codename='test_view',
#     name='Can view',
#     # content_type = content_type
#     content_type_id = 1
# )