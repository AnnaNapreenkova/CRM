from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from PIL import Image
from django.conf import settings
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from datetime import datetime
from datetime import timedelta
import os
import shutil

#! МЕНЕДЖЕР АККАУНТОВ
#!##########################

class MyAccountManager(BaseUserManager):
    
    def create_user(self, email, phone, role, password):
        if not phone:
            raise ValueError('Указанное имя пользователя должно быть установлено')

        if not email:
            raise ValueError('Данный адрес электронной почты должен быть установлен')

        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, phone, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            phone=phone,
            role='Admin'
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create_admin_user(self, admin_user):
        user = self.model(
            email=admin_user['email'],
            phone=admin_user['phone'],
            surname=admin_user['surname'],
            name=admin_user['name'],
            patronim=admin_user['patronim'],
            role=admin_user['role']
        )
        user.set_password('7777')
        user.save(using=self._db)
        return user

#! АККАУНТ
#!########

class Account(AbstractBaseUser):    

    def account_avatar_upload_path(instance, filename):
        ext = '.' + filename.split('.')[-1]
        return '{0}/avatar{1}'.format(instance.email, ext)
    email = models.EmailField(verbose_name="Email", max_length=60, unique=True)
    phone = models.CharField(verbose_name="Телефон",
                             max_length=20, null=True, blank=True)

    date_joined = models.DateTimeField(
        verbose_name="Дата создания", auto_now_add=True)
    last_login = models.DateTimeField(
        verbose_name="Дата последней активности", auto_now=True)
    is_admin = models.BooleanField(verbose_name="Администратор", default=False)
    is_active = models.BooleanField(verbose_name="Активирован", default=True)
    is_staff = models.BooleanField(verbose_name="Сотрудник", default=False)
    is_superuser = models.BooleanField(
        verbose_name="Супер пользователь", default=False)

    surname = models.CharField(
        verbose_name="Фамилия", max_length=255, blank=True)
    name = models.CharField(verbose_name="Имя", max_length=255, blank=True)
    patronim = models.CharField(
        verbose_name="Отчество", max_length=255, blank=True)
    
    ROLES = (
        ('AdminClient', 'Клиент Админа'),        
        ('PartnerClient', 'Клиент партнера'),
        ('Manager', 'Менеджер'),       
        ('Admin', 'Администратор'), 
        ('Partner', 'Партнер')       
    )

    role = models.CharField(verbose_name="Роль", choices=ROLES, max_length=255)

    avatar = models.ImageField(
        upload_to=account_avatar_upload_path, verbose_name="Аватар", null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', ]

    objects = MyAccountManager()  

    def unicode(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    class Meta:
        verbose_name = "Аккаунт"
        verbose_name_plural = "Аккаунты"   


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def account_post_save(sender, instance=None, created=False, updated=False, **kwargs):    
    if created:
        Token.objects.create(user=instance)       
        