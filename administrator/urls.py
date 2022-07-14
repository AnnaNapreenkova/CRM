from django.urls import path
from administrator.views import (
ManagerView, 
ManagerListView,
PartnerListView,
PartnerView,
ClientListView,
ClientView)



app_name = "administrator"


urlpatterns = [
    # path('', AdminUserListView.as_view(), name="AdminUserListView"),
    path('manager/', ManagerListView.as_view(), name="ManagerListView" ),
    path('manager/<int:id>', ManagerView.as_view(), name="ManagerView"),
    path('partner/', PartnerListView.as_view(), name="PartnerListView" ),
    path('partner/<int:id>', PartnerView.as_view(), name="PartnerView"),
    path('client/', ClientListView.as_view(), name="ManagerListView" ),
    path('client/<int:id>', ClientView.as_view(), name="ManagerView"),
]


