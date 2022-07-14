import email
from pyexpat import model
from account.models import Account
from rest_framework import serializers

#! Модели
from partner.models import PartnerProfile
from client.models import ClientProfile

class PartnerCreateSerializer(serializers.ModelSerializer):    
    passport = serializers.CharField()
    birthday = serializers.DateField()
    passportWho = serializers.CharField()
    passportWhen = serializers.DateField()
    inn = serializers.CharField()
    snils = serializers.CharField()

    class Meta:

        model = Account
        fields = ( 'email', 'phone', 'passport', 'birthday',  'passportWho', 'passportWhen', 'inn', 'snils', 'role')

    def save(self):
        account = Account(
            email=self.validated_data['email'],
            role='Partner'
        )
        account_password = "7777"
        print(account_password)
        account.set_password(account_password)
        account.save()
        ManagerAccount = Account.objects.get(email=self.validated_data['email'])

        profile = PartnerProfile(
            user_id=ManagerAccount,
            birthday = self.validated_data['birthday'],
            passport = self.validated_data['passport'],
            passportWho = self.validated_data['passportWho'],
            passportWhen = self.validated_data['passportWhen'],
            inn = self.validated_data['inn'],
            snils = self.validated_data['snils']   
        )
        profile.save()
        data = {
            'profile': profile,
            'account': account
        }
        return data

class PartnerProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = PartnerProfile
        fields = "__all__"

class ClientCreateSerializer(serializers.ModelSerializer):    
    passport = serializers.CharField()
    birthday = serializers.DateField()
    passportWho = serializers.CharField()
    passportWhen = serializers.DateField()
    inn = serializers.CharField()
    snils = serializers.CharField()


    class Meta:

        model = Account
        fields = ( 'email', 'phone', 'passport', 'birthday',  'passportWho', 'passportWhen', 'inn', 'snils', 'role')

    def save(self):
        account = Account(
            email=self.validated_data['email'],
            role='Client'
        )
        account_password = "7777"
        print(account_password)
        account.set_password(account_password)
        account.save()
        ClientAccount = Account.objects.get(email=self.validated_data['email'])

        profile = ClientProfile(
            user_id=ClientAccount,
            birthday = self.validated_data['birthday'],
            passport = self.validated_data['passport'],
            passportWho = self.validated_data['passportWho'],
            passportWhen = self.validated_data['passportWhen'],
            inn = self.validated_data['inn'],
            snils = self.validated_data['snils']   
        )
        profile.save()
        data = {
            'profile': profile,
            'account': account
        }
        return data

class ClientProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClientProfile
        fields = "__all__"
