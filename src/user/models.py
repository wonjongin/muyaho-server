from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager, AbstractBaseUser
from django.db.models.signals import pre_save
from django.dispatch import receiver
from notice.models import Notice
from django.contrib.auth.hashers import make_password, is_password_usable
# from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        superuser = self.create_user(
            email=email,
            password=password,
        )
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True
        superuser.save(using=self._db)
        return superuser


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True, null=False, blank=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    nickname = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'


@receiver(pre_save, sender=User)
def password_hashing(instance, **kwargs):
    if not is_password_usable(instance.password):
        instance.password = make_password(instance.password)



class Keyword(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class AlarmSettings(models.Model): #알람
    keyword = models.CharField(max_length=100)
    alarm_date = models.DateTimeField()
    alarm_days = models.IntegerField()
    # 월 수 금: 2+8+32 = 42
    # 알람 없을 때: 0 
    # 일: 1
    # 월: 2
    # 화: 4
    # 수: 8
    # 목: 16
    # 금: 32
    # 토: 64
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Notification(models.Model): #알림
    keyword = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.TextField()
    remind_date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE)

class Scrap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE)