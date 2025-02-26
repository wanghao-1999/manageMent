from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('doc_management.urls')),
    path('', include('user_management.urls')),
    path('', include('system_config.urls')),

]
