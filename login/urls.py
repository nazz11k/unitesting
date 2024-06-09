from django.contrib.auth.views import LogoutView
from django.urls import path

from login.views import LogInView, SignUpView, profile, PersonalDataView

urlpatterns = [
    path('login/', LogInView.as_view(), name='login'),
    path('signup/<str:user_type>/', SignUpView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', profile, name='profile'),
    path('profile/personal_data/', PersonalDataView.as_view(), name='personal_data'),
]