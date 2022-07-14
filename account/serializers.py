from urllib import request
from wsgiref import validate
from rest_framework import serializers
from .models import Account
from django.core.mail import send_mail
from rest_framework import authentication, exceptions
from django.conf import settings 


class RegistrationSerializer(serializers.ModelSerializer):
    '''Сериализатор регистрации'''    
    class Meta:
        model = Account
        fields = ('email', 'phone', 'role')
    
    def save(self):

        account = Account(
            email=self.validated_data['email'],
            phone=self.validated_data['phone'],
            role=self.validated_data['role']            
        )
        account_password = "7777"        
              #send_mail(
        #    'Данные об аккаунте',
        #    'Ваша почта - ' + account.email + '\nВаш пароль - ' + account_password,
        #    'businessfoxmail@gmail.com',
        #    [account.email],
        #    fail_silently=False,
        #)
        print(account)
        account.set_password(account_password)
        account.save()
        return account

class AccountSerializer(serializers.ModelSerializer):
    '''Сериализатор аккаунта пользователя'''
    class Meta:
        model = Account
        exclude = ['email', 'role', 'password', 'is_staff', 'is_admin', 'is_active',
                   'last_login', 'is_superuser']
        # extra_kwargs = {
        #     'password': {'write_only': True}
        # }

    def create(self, validated_data):
        user = Account.objects.create(**validated_data)
        # user = Account(
        #     email=validated_data['email'],
        #     phone=validated_data['phone'],
        #     second_name=validated_data['second_name'],
        #     name=validated_data['name'],
        #     last_name=validated_data['last_name'],
        #     role=validated_data['role']
        # )
        
        account_password = "7777"
        # account_password = get_random_string(12)
        # user.set_password(validated_data['password'])
        print(account_password)
        user.set_password(account_password)
        user.save()
        return user





class AccountProfileSerializer(serializers.ModelSerializer):
    '''Сериализатор профиля'''
    class Meta:
        model = Account
        fields = ['surname', 'name', 'patronim', 'role', 'id']


