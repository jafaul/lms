from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from apps.assessment.models import Answer, Mark
from django.utils.translation import gettext_lazy as _


def create_email(full_msg, subject, course_id, user, end_msg, btn_name=''):
    user_fullname = user.get_full_name()

    email = EmailMultiAlternatives(
        subject=render_to_string(
            "emails/subject_base.txt",
            context={"subject": subject},
        ),
        body=render_to_string(
            "emails/message_base.txt",
            context={"msg": _(full_msg), "user_full_name": user_fullname, "end_msg": end_msg},
        ).strip(),
        to=[user.email],
    )
    msg1, msg2 = full_msg.split(".\n", 2)

    email.attach_alternative(
        render_to_string(
            "emails/assessment/answer_send.html",
            context={
                "msg2": _(msg2 + "\n" + end_msg),
                "msg1": _(msg1),
                "full_name": user_fullname,
                "course_id": course_id.id,
                "btn_name": btn_name,
            },
        ),
        "text/html",
    )
    email.send()



@shared_task
def send_homework_accepted_email(answer_id):
    answer = Answer.objects.select_related("task", "task__course").get(pk=answer_id)
    user = answer.student

    subject = f"Your homework for task '{answer.task.title.strip()}' is been received".replace(
        "&#x27;", ""
    )
    full_msg = f"""Please be informed that we have received your homework for the task '{answer.task.title}'.
        It will be checked during 7 days."""

    end_msg = "Best luck, your S."

    create_email(
        full_msg, subject, answer.course_id, user, end_msg
    )


@shared_task
def send_mark_notification_email(mark_id):
    mark = Mark.objects.select_related("answer__student", "answer__task", "answer__task__course").get(pk=mark_id)

    subject = f"+{mark.mark_value}: score for HW, task {mark.task.id}"
    full_msg = f"You've got a score for a homework for task '{mark.task.title}' course '{mark.task.course.title}'"
    btn_name = "Check score"
    end_msg = "Best Luck! \n Your S Team"

    create_email(
        full_msg, subject, mark.answer.task.course_id, mark.answer.student, end_msg, btn_name
    )
