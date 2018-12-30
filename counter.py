from os import environ
from datetime import datetime, timedelta, time

from peewee import fn

from models.tables import User, Message

GROUP_ID = int(environ['GROUP_ID'])
ADMINS = environ['ADMINS']


def is_admin(update):
    user_id = str(update.message.from_user.id)

    listAdmins = ADMINS.split(',')
    admin = False
    for i in listAdmins:
        print(i, ' ', user_id)
        if i == user_id:
            admin = True
            break
    return admin


def add_counter_daily(bot, update, args, job_queue, chat_data):
    ''' Add send messages daily with messages counter'''
    chat_id = update.message.chat_id

    if is_admin(update) and (chat_id == GROUP_ID):
        chat_id = update.message.chat_id

        try:
            # due = int(args[0])

            the_time = args[0].split(':')

            hour = int(the_time[0])
            minute = int(the_time[1])
            second = int(the_time[2])

            today = datetime.now()
            dt = datetime(today.year, today.month, today.day,
                          hour, minute, second)
            hour_server = dt + timedelta(hours=6)

            due = time(hour=hour_server.hour, minute=minute, second=second)
            job = job_queue.run_daily(msg_daily, due, context=chat_id)

            chat_data['counter'] = job

            msg = f'Envio de contador de mensajes diario '\
                'activado con éxito.\n'\
                f'Se enviará a las\n'\
                f'Horas: {hour}\n'\
                f'Minutos: {minute}\n'\
                f'Segundos: {second}'

            update.message.reply_text(msg)

        except (IndexError, ValueError):
            update.message.reply_text('Use el siguiente formato:\n'
                                      '/set 19:00:00')

    else:
        update.message.reply_text('Opción sólo para admins')


def remove_counter_daily(bot, update, chat_data):
    ''' Remove message counter sending '''
    chat_id = update.message.chat_id

    if is_admin(update) and (chat_id == GROUP_ID):

        if 'counter' not in chat_data:
            update.message.reply_text('Contador diario no activado')
            return
        job = chat_data['counter']
        job.schedule_removal()
        del chat_data['counter']
        update.message.reply_text('Contador diario desactivado!')


def msg_daily(bot, job):

    # chat_id = update.message.chat_id

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

    bot.send_message(job.context, text=msg+tops)


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
