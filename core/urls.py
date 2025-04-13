from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('admin/', admin.site.urls),
    path('forum/', include('forum.urls')),
    path('tickets/', include('tickets.urls')),
]
