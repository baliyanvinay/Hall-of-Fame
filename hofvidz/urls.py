from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from hall import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name="home"),
    # User Authentication
    path('signup',views.SignUp.as_view(),name='signup'),
    path('login',auth_views.LoginView.as_view(),name='login'),
    path('logout',auth_views.LogoutView.as_view(),name='logout'),
]
