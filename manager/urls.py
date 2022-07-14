from django.urls import path

from administrator.views import (
PartnerListView,
PartnerView,
ClientListView,
ClientView)

app_name = 'manager'

urlpatterns = [
    path('partner/', PartnerListView.as_view(), name="PartnerListView" ),
    path('partner/<int:id>', PartnerView.as_view(), name="PartnerView"),
    path('client/', ClientListView.as_view(), name="ClientListView" ),
    path('client/<int:id>', ClientView.as_view(), name="ClientView"),
]