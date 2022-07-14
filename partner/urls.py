from django.urls import path

from partner.views import (
ClientListView,
ClientView)

app_name = 'partner'

urlpatterns = [   
    path('client/', ClientListView.as_view(), name="ClientListView" ),
    path('client/<int:id>', ClientView.as_view(), name="ClientView"),
]