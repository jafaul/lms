import io
import random

from boto3.s3.inject import upload_file
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.images import ImageFile
from django.core.management import BaseCommand
import requests

from apps.authentication.views import PasswordResetView
from apps.authentication.tasks import send_reset_password_mail

User = get_user_model()


class Command(BaseCommand):
    help = f"generate fake users. Default role is 'student', default amount is '12'."

    def add_arguments(self, parser):
        position_choices = {choice[0] for choice in User.Position.choices}
        parser.add_argument(
            '--position',
            type=str,
            default="student",
            choices=position_choices,
            help=f'Specify a position (available positions: {position_choices}).)'
        )
        parser.add_argument(
            '-n',
            type=int,
            choices = list(range(1, 13)),
            default=12,
            help=f'Specify amount of users.'
        )

    def handle(self, *args, **options):
        position = options.get('position')
        number_of_users = options.get('n')

        url = settings.REGRES_TEST_API_URL + "users?page=1"
        response = requests.request("GET", url, headers={}, data={})
        response.raise_for_status()

        result = response.json()
        total_pages = result["total_pages"]
        users = result["data"]
        print("total pages: {}".format(total_pages))
        print(f"Position selected: {position}")

        for i in range(1, total_pages):
            url = settings.REGRES_TEST_API_URL + f"users?page={i+1}"
            response = requests.request("GET", url, headers={}, data={})
            response.raise_for_status()

            users.extend(response.json()["data"])

        random.shuffle(users)

        user_created_counter = 0

        for user in users:
            email = user["email"] + position
            exists = User.objects.filter(email=email).exists()
            if exists:
                print(f"user {email} already exists")
                continue
            new_user = User(
                email=email,
                first_name=user["first_name"],
                last_name=user["last_name"],
                username=user["email"] + position,
                position=position,
            )

            img_url = user.get("avatar")
            self.stdout.write(img_url)
            img = requests.get(img_url, stream=True).content
            file_name = str(user["id"]) + position + ".jpg"
            img_file = ImageFile(io.BytesIO(img), name=file_name)

            new_user.photo = img_file
            new_user.save()
            self.stdout.write(f"Created user {new_user.email} with avatar.")

            send_reset_password_mail.delay(
                new_user.email, PasswordResetView.subject_template_name,
                PasswordResetView.email_template_name,
                PasswordResetView.html_email_template_name,
            )

            user_created_counter += 1
            if user_created_counter == number_of_users:
                break

        self.stdout.write(f"Sent {len(users)} emails to each user to reset password.\n "
                          f" Please activate users by assigning a new password manually.")

