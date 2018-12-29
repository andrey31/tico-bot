from os import environ
from datetime import datetime, timedelta

from peewee import fn

from models.tables import User, Message

GROUP_ID = int(environ['GROUP_ID'])


def msg_daily(bot, update):

    chat_id = update.message.chat_id

    today = datetime.today() - timedelta(hours=6)
    yesterday = today - timedelta(days=1)

    total_daily = Message.select().where(Message.date > yesterday,
                                         Message.date < today)
    msg = 'Reporte últimas 24hrs\n\n'\
          f'Mensajes\n └ Totales: {total_daily.count()}\n'
    top_ten = (Message
               .select(Message.user, fn.count(Message.user)
                       .alias('num_messages'))
               .where(Message.date > yesterday, Message.date < today)
               .group_by(Message.user)
               .limit(10))
    tops = ''
    count = 1
    for i in top_ten:
        tops += f'TOP {count}: \n'\
                f' ├alias: @{i.user.username} \n'\
                f' ├nombre: {i.user.first_name}\n'\
                f' └enviados: {i.num_messages}\n'
        count += 1

    bot.send_message(chat_id=chat_id, text=msg+tops)


def counter(bot, update):
    chat_id = update.message.chat_id

    if chat_id == GROUP_ID:

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
