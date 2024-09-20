"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.i18n import set_language
from django.views.generic.base import RedirectView
#from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.staticfiles.storage import staticfiles_storage

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("accounts.urls")),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'))),
    path('salon/', include('saloon.urls')),
    path('finance/', include('saloonfinance.urls')),
    #path("i18n/setlang/", set_language, name="set_language"),
    # path('api/accounts/', include('accounts.apiurls')),
    # path('api/saloon/', include('saloon.apiurls')),
    # path('api/finance/', include('saloonfinance.apiurls')),
    # path('api/services/', include('saloonservices.apiurls')),
    # path('api/inventory/', include('salooninventory.apiurls')),
    # path('api/api-token-auth/', obtain_auth_token, name='api_token_auth'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
