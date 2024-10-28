from django.core.management.base import BaseCommand
from comsoftlab.apps.users.models import User
from django.conf import settings


SECRET_KEY = settings.SECRET_KEY


class Command(BaseCommand):
    help = 'Create user | python manage.py createuser "email" "password"'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='User email')
        parser.add_argument('password', type=str, help='User password')

    def handle(self, *args, **kwargs):
        try:
            email = kwargs['email']
            password = kwargs['password']
            user = User(email=email, password=password)
            user.save()
            self.stdout.write(f'Пользователь создан.')
        except Exception as e:
            self.stdout.write(f'Произошла ошибка | {str(e)}')