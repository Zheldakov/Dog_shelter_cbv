from django.conf import settings
from django.core.mail import send_mail


def send_register_email(email):
    # Отправка письма при регистрации
    send_mail(
        subject="Поздравляем с регистрацией",  #
        message=f"Вы зарегистрированы на сайте Dog Shelter",
        from_email=settings.EMAIL_HOST_USER,  # Email address
        recipient_list=[email],  # Список получателей
    )


def send_new_password(email, new_password):
    # Отправка письма с информацией о новом пароле
    send_mail(
        subject="Вы успешно изменили пароль",
        message=f"Ваш новый пароль {new_password}",
        from_email=settings.EMAIL_HOST_USER,  # Email address
        recipient_list=[email],  # Список получателей
    )
