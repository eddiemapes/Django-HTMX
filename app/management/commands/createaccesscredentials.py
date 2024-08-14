from django.core.management.base import BaseCommand
from app.models import *
from django.contrib.auth.models import User

class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        users = User.objects.all()
        accesses = AccessCredential.objects.all()
        for user in users:
            access = accesses.filter(user=user)
            if not access:
                AccessCredential.objects.create(user=user)
                print(f'Created AccessCredential object for {user.username}')