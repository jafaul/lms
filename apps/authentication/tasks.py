from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from apps.authentication.tokens import account_activation_token
from django.utils.translation import gettext_lazy as _


@shared_task
def activate_email(user):
    subject = "Activate your user account."

    full_msg = f"Please click on the link below to confirm your registration: "
    end_msg = "We are looking forward to you joining us, your S."

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)

    url_confirmation = settings.SITE_URL + reverse(
        'apps.authentication:activate', kwargs={'uidb64': uid, 'token': token})

    email = EmailMultiAlternatives(
        subject=render_to_string(
            "emails/subject_base.txt",
            context={"subject": subject},
        ),
        body=render_to_string(
            "emails/message_base.txt",
            context={
                "msg": _(full_msg + "\n" + url_confirmation),
                "user_full_name": user.get_full_name(), "end_msg": end_msg
            },
        ).strip(),
        to=[user.email],
    )

    email.attach_alternative(
        render_to_string(
            "emails/authentication/email_confirmation.html",
            context={
                "msg1": _(full_msg.replace("link", "button")),
                "msg2": end_msg,
                "full_name": user.get_full_name(),
                "activate_url": url_confirmation,
            },
        ),
        "text/html",
    )
    return email.send()
