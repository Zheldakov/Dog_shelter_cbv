from django.urls import path

from users.apps import UsersConfig
from users.views import user_register_view, user_login_view, user_profile_view, user_logout_view, user_update_view,user_change_password_view, user_generate_new_password

app_name = UsersConfig.name

urlpatterns = [
    path('', user_login_view, name="login_user"),
    path('logout/', user_logout_view, name='logout_user'),
    path('register/', user_register_view, name='register_user'),
    path('profile/', user_profile_view, name='profile_user'),
    path('update/', user_update_view, name='update_user'),
    path('change_password/', user_change_password_view, name='change_password_user'),
    path('profile/genpassword/', user_generate_new_password, name='generate_new_password_user')

]
