"""
URL configuration for ecomweb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from utils.api_urls import APIRootView

swagger_patterns = [
    ######## Swagger ##########
    path('api/schema/', SpectacularAPIView.as_view(urlconf=None), name='schema-json'),  # JSON schema
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema-json'), name='swagger-ui'),
    path('api/redocs/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/auth/', include('authapp.urls')),
    path('api/all-endpoints/', APIRootView.as_view(), name='all-endpoints'),
] + swagger_patterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
