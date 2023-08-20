"""daily_status_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from ds_app import views as ds_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ds_views.home, name='home'),
    path('ticket_detail/<int:pk>/', ds_views.ticket_details, name='detail'),
    path('ticket_update/', ds_views.ticket_update, name='update'),
    path('ticket_delete/<int:pk>/', ds_views.ticket_delete, name='delete'),
    path('tickets_list/', ds_views.all_tickets_for_mail, name='all_tickets'),
    path('send_mail/', ds_views.send_mail_view, name='send_mail'),
    path('password_change/', ds_views.change_password_view, name='password_change'),
    path('login/', ds_views.login_view, name='login'),
    path('logout/', ds_views.logout_view, name='logout'),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)