from http import client
from .serializers import RegistrationSerializer, AccountSerializer
from .models import Account
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from administrator.models import AdministratorProfile
from partner.models import PartnerProfile

import base64

class RegistrationView(APIView):
    '''Регистрация нового пользователя''' 
    
    serializer_class = RegistrationSerializer 

    def check_manager(self, request, account):
        try:
            managerId = request.data['Manager']
        except KeyError:
            pass
        else:
            manager = Account.objects.get(id=managerId)

            admin_profile = AdministratorProfile(
                user_id=account,
                manager=manager
            )
            admin_profile.save()

    def check_partner_admin(self, request, account):
        try:
            partnerId = request.data['Partner']
        except KeyError:
            pass
        else:
            partner = Account.objects.get(id=partnerId)

            admin_profile = AdministratorProfile(
                user_id=account,
                partner=partner
            )
            admin_profile.save()

    def check_client_admin(self, request, account):
        try:
            clientId = request.data['AdminClient']
        except KeyError:
            pass
        else:
            client = Account.objects.get(id=clientId)

            admin_profile = AdministratorProfile(
                user_id=account,
                AdminClient=client
            )
            admin_profile.save()

    def check_client_partner(self, request, account):
        try:
            clientId = request.data['PartnerClient']
        except KeyError:
            pass
        else:
            client = Account.objects.get(id=clientId)

            partner_profile = PartnerProfile(
                user_id=account,
                PartnerClient=client
            )
            partner_profile.save()

    def check_email(self, request):
        '''Проверка на наличие почты в системе'''
        try:
            Account.objects.filter(email=request.data['email'])
        except Account.DoesNotExist:
            pass
        else:
            return Response({'msg': 'Данный Email уже зарегистрирован'}, status=411)

    def check_phone(self, request):
        '''Проверка на наличие телефона в системе'''
        try:
            Account.objects.filter(phone=request.data['phone'])
        except Account.DoesNotExist:
            pass
        else:
            return Response({'msg': 'Номер телефона уже зарегистрирован'}, status=412)
    
    def check_data(self, request):
        '''Запуск всех проверок'''
        self.check_email(request)
        self.check_phone(request)  

    def check_roles(self, request, account):
        self.check_manager(request, account)
        self.check_partner_admin(request, account)
        self.check_client_admin(request, account)
        self.check_client_partner(request, account)

    def post(self, request):
        '''Регистрация пользователя'''
        self.check_data(request)
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        account = Account.objects.get(email=request.data['email'])
        print(account)        
        self.check_roles(request, account)
        return Response({'msg': 'Регистрация успешна'}, status.HTTP_201_CREATED)    
      
class SelfAccountView(APIView):
    """Просмотр, изменение пользователя по токену"""
    permissions_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_account(self, id):
        """Поиск пользователя в системе по id"""
        try:
            account = Account.objects.get(id=id)
        except Account.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return account

    """ token_param_config = openapi.Parameter(
        'email', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config]) """
    def get(self, request):
        """Просмотр данных о пользователе данного токена"""

        account = self.get_account(request.user.id)
        serializer = AccountSerializer(account)
        return Response(serializer.data, status=200)

    def patch(self, request):
        """Изменение данных о пользователе данного токена"""
        account = self.get_account(request.user.id)
        serializer = AccountSerializer(
            account, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update(account, validated_data=request.data)
            return Response(data=serializer.data, status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountView(APIView):
    """Просмотр и изменение пользователя по id"""
    permissions_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_account(self, id):
        """Поиск пользователя в системе по id"""
        try:
            account = Account.objects.get(id=id)
        except Account.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return account

    def get(self, request, id):
        """Просмотр данных о пользователе"""
        account = self.get_account(id)
        serializer = AccountSerializer(account)
        return Response(serializer.data, status=200)

    def patch(self, request, id):
        """Изменение данных о пользователе данного токена"""
        account = self.get_account(id)
        serializer = AccountSerializer(
            account, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update(account, validated_data=request.data)
            return Response(data=serializer.data, status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
