import profile
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status


from client.models import ClientProfile
from .serializers import ClientCreateSerializer, ClientProfileSerializer

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






