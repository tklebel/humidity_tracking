#!/usr/bin/env python3

from telegram.ext import Updater, CommandHandler, Filters, CallbackContext
import logging
import Adafruit_DHT
from datetime import datetime
from functions import format_result
from bot_secrets import channels, bottoken


c = channels
b = bottoken


updater = Updater(token=b.token(), use_context=True)
dispatcher = updater.dispatcher
j = updater.job_queue

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def get_data():
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 4)
    time = datetime.now()

    return (time, humidity, temperature)

def status(update, context):
    results = get_data()

    message = format_result(*results)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    logger.info('Sending status.')

def monitor_humidity(context: CallbackContext):
    job = context.job

    results = get_data()
    humidity = results[1]
    humidity_pretty = "{0:0.1f}%".format(humidity)
    alerting = False

    if humidity > 60:
        logger.info('Sending alert. Humidity at ' + humidity_pretty)
        job.interval *= 2
        context.bot.send_message(chat_id=c.channel('id'),
                                 text='Humidity at ' + humidity_pretty + '! Air the room!')
    else:
        job.interval = 60
        logger.info('Checking humidity. Humidity at ' + humidity_pretty)


    # remove the alert after two days
    if job.interval > 2*24*60:
        job.schedule_removal()

j.run_repeating(monitor_humidity, interval=60, first=0)


status_handler = CommandHandler('status', status, filters=Filters.user(username=c.channel('user')))
dispatcher.add_handler(status_handler)


updater.start_polling()

updater.idle()
