#!/usr/bin/env python3

from telegram.ext import Updater, CommandHandler, Filters, CallbackContext
import logging
import Adafruit_DHT
from datetime import datetime
from functions import format_result, get_data
from bot_secrets import channels, bottoken
# import numpy as np


c = channels
b = bottoken


updater = Updater(token=b.token(), use_context=True)
dispatcher = updater.dispatcher
j = updater.job_queue

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def status(update, context):
    results = get_data()

    message = format_result(*results)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    logger.info('Sending status: ' + message)

def monitor_humidity(context: CallbackContext):
    job = context.job

    results = get_data(logger)
    humidity = results[1]
    ##  alternative for debugging
    # humidity =  np.random.normal(60, 10, 1)
    humidity_pretty = "{0:0.1f}%".format(humidity)


    if humidity > 75:
        job.context = True
        job.interval *= 2
        logger.info('Sending alert. Humidity at ' + humidity_pretty)
        context.bot.send_message(chat_id=c.channel('id'),
                                 text='Humidity at ' + humidity_pretty + '! Air the room!')
    elif humidity <= 75 and job.context:
        # this part only runs once after we have stopped alerting
        job.context = False
        job.interval = 60
        logger.info('Humidity level restored, resume checking every 60 seconds.')
        context.bot.send_message(
            chat_id=c.channel('id'),
            text='Safe humidity level restored!')
    else:
        # this is the standard case which usually runs every 60 seconds
        job.interval = 60
        logger.info('Checking humidity. Humidity at ' + humidity_pretty)


    # remove the job after two days
    # this, together with sending messages with increasing delay should be decoupled from the checking interval
    if job.interval > 2*24*60*60:
        job.schedule_removal()

j.run_repeating(monitor_humidity, interval=60, first=0, context=False)


status_handler = CommandHandler('status', status, filters=Filters.user(username=c.channel('user')))
dispatcher.add_handler(status_handler)


updater.start_polling()

updater.idle()
