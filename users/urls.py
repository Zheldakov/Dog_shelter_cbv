from django.urls import path

from users.apps import UsersConfig
from users.views import user_logout_view,user_change_password_view, user_generate_new_password,UserRegisterView, UserLoginView, UserProfileView, UserUpdateView

app_name = UsersConfig.name

urlpatterns = [
    path('', UserLoginView.as_view(), name="login_user"),
    path('logout/', user_logout_view, name='logout_user'),
    path('register/', UserRegisterView.as_view(), name='register_user'),
    path('profile/', UserProfileView.as_view, name='profile_user'),
    path('update/', UserUpdateView.as_view, name='update_user'),
    path('change_password/', user_change_password_view, name='change_password_user'),
    path('profile/genpassword/', user_generate_new_password, name='generate_new_password_user')

]
