from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from apps.assessment.models import Answer
from django.utils.translation import gettext_lazy as _


@shared_task
def send_homework_accepted_email(answer_id):
    # send_mail(
    #     "Your homework has been approved",
    #     f"Your homework has been approved: {form.instance.description}",
    #     base.DEFAULT_FROM_EMAIL,
    #     [self.request.user.email]
    # )

    # better for html msg
    answer = Answer.objects.select_related("task", "task__course").get(pk=answer_id)
    user = answer.student
    user_fullname = user.get_full_name()

    subject = f"Your homework for task '{answer.task.title.strip()}' is been received".replace(
        "&#x27;", ""
    )
    full_msg = f"""Please be informed that we have received your homework for the task '{answer.task.title}'.
        It will be checked during 7 days."""

    email = EmailMultiAlternatives(
        subject=render_to_string(
            "emails/assessment/subject_answer_send.txt",
            context={"subject": subject},
        ),
        body=render_to_string(
            "emails/assessment/message_answer_send.txt",
            context={"msg": _(full_msg), "user_full_name": user_fullname},
        ).strip(),
        to=[user.email],
    )
    msg1, msg2 = full_msg.split(".\n", 2)

    email.attach_alternative(
        render_to_string(
            "emails/assessment/answer_send.html",
            context={
                "msg2": _(msg2),
                "msg1": _(msg1),
                "full_name": user_fullname,
                "course_id": answer.task.course.id,
            },
        ),
        "text/html",
    )
    email.send()
