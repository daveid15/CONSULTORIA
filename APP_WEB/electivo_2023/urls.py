"""electivo_2023 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from core.urls import core_urlpatterns
from django.contrib import admin
from django.urls import path, include
from administrator import views
from administrator.urls import administrator_patterns
from caracterizacion.urls import caracterizacion_patterns
urlpatterns = [
    path("administrator/", include(administrator_patterns)),
    path('', include(core_urlpatterns)),
    path('admin/',admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('registration.urls')),
    path("caracterizacion/", include(caracterizacion_patterns))
    
]
admin.site.site_header = 'Administrador Bussiness_Solutions'
admin.site.site_title = 'bussinessSolutions' 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



