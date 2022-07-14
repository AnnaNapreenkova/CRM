import profile
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status

from client.models import ClientProfile
from partner.models import PartnerProfile

from .serializers import (
PartnerCreateSerializer, 
PartnerProfileSerializer,
ClientCreateSerializer,
ClientProfileSerializer)

#! Партнёры
class PartnerListView(APIView):
    '''Список и добавление партнеров'''
    permissions_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        try:
            partner = PartnerProfile.objects.all()
        except:
            if PartnerProfile.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PartnerProfileSerializer(partner, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):        
        serializer = PartnerCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PartnerView(APIView):
    '''Получение и редактирование партнеров по id'''
    permissions_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, id):
        try:
            profile = PartnerProfile.objects.get(user_id=id)
        except PartnerProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PartnerProfileSerializer(profile)
        return Response(serializer.data)  
    

    def patch(self, request, id):
        '''Изменение данных о пользователе по id'''
        profile = PartnerProfile.objects.get(user_id=id)
        serializer = PartnerProfileSerializer(
            profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update(profile, validated_data=request.data)
            return Response(data=serializer.data, status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#! Клиенты
class ClientListView(APIView):
    '''Список и добавление клиентов'''
    permissions_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request):
        try:
            client = ClientProfile.objects.all()
        except:
            if ClientProfile.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ClientProfileSerializer(client, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):        
        serializer = ClientCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientView(APIView):
    '''Получение и редактирование клиентов по id'''
    permissions_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, id):
        try:
            profile = ClientProfile.objects.get(user_id=id)
        except ClientProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ClientProfileSerializer(profile)
        return Response(serializer.data)   
    
    def patch(self, request, id):
        '''Изменение данных о пользователе по id'''
        profile = ClientProfile.objects.get(user_id=id)
        serializer = ClientProfileSerializer(
            profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update(profile, validated_data=request.data)
            return Response(data=serializer.data, status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#! Администрирование
""" class ManagerUserListView(APIView):
    '''Администрирование менеджером'''
    def get(self, request):
        users = []        
        users += Account.objects.filter(role='Partner')
        users += Account.objects.filter(role='AdminClient')
        serializer = AccountSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors) """
