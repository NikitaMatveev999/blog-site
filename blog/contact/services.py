from django.core.mail import send_mail


def send(user_email):
    send_mail(
        'Thanks for contacting us!',
        'we will solve your problem as quickly as possible! Wait for new mail',
        'matveevnikita999777@gmail.com',
        [user_email],
        fail_silently=False,
    )
