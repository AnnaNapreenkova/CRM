from django.db import models
from account.models import Account
from django.utils.translation import ugettext_lazy as _


class AdministratorProfile(models.Model):
    user_id = models.ForeignKey(
        Account, related_name='administrator_account', verbose_name="Администратор", on_delete=models.CASCADE)
