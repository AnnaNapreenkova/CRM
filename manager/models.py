from tabnanny import verbose
from blinker import receiver_connected
from django.db import models

from account.models import Account


class ManagerProfile(models.Model): 
    def manager_upload_path(instance, filename):
        return '{0}/{1}'.format(instance.user_id.email, filename)

    user_id = models.ForeignKey(
        Account, related_name='manager_account', verbose_name='Менеджер', on_delete=models.CASCADE)
    birthday = models.DateField(verbose_name='Дата рождения')
    

   #!Документы 
    passport = models.CharField(
        verbose_name="Серия/номер паспорта", max_length=255)
    passportWho = models.CharField(
        verbose_name="Кем выдан паспорт", max_length=255, blank=True)
    passportWhen = models.DateField(verbose_name="Дата выдачи паспорта", blank=True)
    inn = models.CharField(verbose_name="ИНН", max_length=255, blank=True)
    snils = models.CharField(verbose_name="Снилс", max_length=255, blank=True)    

    passportPDF = models.FileField(
        upload_to=manager_upload_path, verbose_name='Паспорт PDF', blank=True
    )
    snilsPDF = models.FileField(
        upload_to=manager_upload_path, verbose_name="СНИЛС PDF", blank=True)
    innPDF = models.FileField(
        upload_to=manager_upload_path, verbose_name="ИНН PDF", blank=True)    


    class Meta:
        verbose_name = 'Профиль менеджера'
        verbose_name_plural = 'Профили менеджеров'


    def unicode(self):
        return self.user_id.surname + ' ' + self.user_id.name
