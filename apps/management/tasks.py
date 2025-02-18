import datetime

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.template.loader import render_to_string
from django.urls import reverse

from apps.management.models import Course, Task

User = get_user_model()


def create_email(course_id, subject, msg, user, end_msg):
    url = settings.SITE_URL + reverse(
        'apps.management:course-detail',
        kwargs={'pk': course_id})

    email = EmailMultiAlternatives(
        subject=render_to_string(
            "emails/subject_base.txt",
            context={"subject": subject},
        ),
        body=render_to_string(
            "emails/message_base.txt",
            context={
                "msg": msg,
                "user_full_name": user.get_full_name(),
                "end_msg": end_msg,
            },
        ).strip(),
        to=[user.email],
    )

    email.attach_alternative(
        render_to_string(
            "emails/management/course_is_starting.html",
            context={
                "msg1": msg,
                "full_name": user.get_full_name(),
                "activate_url": url,
                "msg2": end_msg,
            },
        ),
        "text/html",
    )

    email.send()


@shared_task
def send_course_starts_tomorrow_email():

    end_msg = '''
    See you soon! 
      
    Best,  
    The Team S.
    '''

    courses = (
        Course.objects
        .prefetch_related("students")
        .filter(
            Q(start_datetime__gte=datetime.datetime.now() + datetime.timedelta(days=1))
        )
        .all()
    )
    for course in courses:
        subject = f"Reminder: {course.title} starts tomorrow!"
        for student in course.students.all():
            full_msg = (f"This is a reminder that your course '{course.title}' starts on {course.start_datetime}.\n "
                        f"Click on button to get more details:")
            create_email(course.id, subject, full_msg, student, end_msg)


@shared_task
def send_new_task_notification_email(task_id):
    task = (
        Task.objects
        .prefetch_related("course__students")
        .get(id=task_id)
    )

    subject = "You've got a new task!"
    full_msg = f'''Hey there! A new task '{task.title.strip()}' has been assigned to you. 
                    The deadline is {task.deadline}. 
                    Let us know if you need any help!
                '''
    end_msg = "Good luck! \nYour S Team"

    for student in task.course.students.all():
        create_email(
            course_id=task.course_id,
            subject=subject,
            msg=full_msg,
            user=student,
            end_msg=end_msg,
        )
