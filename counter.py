from os import environ
from datetime import datetime, timedelta

from models.tables import User, Message

GROUP_ID = environ['GROUP_ID']


def counter(bot, update):
    chat_id = update.message.chat_id

    if chat_id == int(GROUP_ID):

        message = update.message
        user_id = message.from_user.id
        username = message.from_user.username
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name

        user = User.select().where(User.id_user == user_id)

        if not user.exists():

            user = User.create(
                id_user=user_id,
                username=username,
                first_name=first_name,
                last_name=last_name
            )

            Message.create(
                user=user,
                date=datetime.now() - timedelta(hours=6)
            )

        else:

            # datos actualizados
            user = user.get()
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            Message.create(
                user=user,
                date=datetime.now() - timedelta(hours=6)
            )
