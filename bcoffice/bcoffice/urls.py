"""bcoffice URL Configuration

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
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from .views import get_currency_list, get_market_list

urlpatterns = [
    url(r'v1/get-currency-list/', get_currency_list),
    url(r'v1/get-market-list/', get_market_list),
    url(r'', include('blacklist.urls')),
    url(r'', include('account.urls')),
    url(r'', include('members.urls')),
    url(r'', include('bank_account.urls')),
    url(r'', include('coin_account.urls')),
    url(r'', include('boards.urls')),
    url(r'', include('order_history.urls')),
    url(r'', include('supports.urls')),
    url(r'', include('manager_memo.urls')),
    url(r'', include('policy_manage.urls')),
    url(r'', include('system_controls.urls')),
    url(r'', include('trend.urls')),
]
