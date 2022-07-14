from django.contrib import admin
from django.urls import include, path

urlpatterns = [    
    path('admin/', admin.site.urls),
    path('api/v1/account/', include('account.urls'), name="account"),
    path('api/v1/manager/', include('manager.urls'), name="manager"),
    path('api/v1/partner/', include('partner.urls'), name="partner"),
    path('api/v1/client/', include('client.urls'), name="client"),
    path('api/v1/administrator/', include('administrator.urls')),    

]
