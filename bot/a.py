import config

from backend.models import BotUser


try:
    for i in BotUser.objects.all():
        