import logging
from time import sleep

import requests
import telegram
from environs import Env


log = logging.getLogger(__file__)


class TelegramLogHandler(logging.Handler):
    def __init__(self, bot, chat_id):
        super().__init__()
        self.bot = bot
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)

        self.bot.send_message(
            chat_id=self.chat_id,
            text=log_entry
        )


if __name__ == '__main__':
    env = Env()
    env.read_env()

    dvmn_token = env('DVMN_TOKEN')
    tg_token = env('TG_TOKEN')
    chat_id = env('TG_CHAT_ID')

    logging.basicConfig(level=logging.INFO)

    bot = telegram.Bot(token=tg_token)

    log.addHandler(
        TelegramLogHandler(bot, chat_id)
    )

    url = 'https://dvmn.org/api/long_polling/'

    headers = {
        'Authorization': f'Token {dvmn_token}'
    }

    params = {}

    log.info('Бот сейчас запущен.')
    while True:
        try:
            response = requests.get(
                url,
                headers=headers,
                params=params
            )
            response.raise_for_status()

            review_data = response.json()
            if review_data['status'] == 'timeout':
                log.debug('Новых проверок нет.')
                params = {'timestamp': review_data['timestamp_to_request']}
            elif review_data['status'] == 'found':
                log.debug('сть новая проверка.')
                params = {'timestamp': review_data['last_attempt_timestamp']}

                for attempt in review_data['new_attempts']:
                    lesson_title = attempt['lesson_title']
                    message = f'У вас проверили работу «{lesson_title}». \n\n'

                    if attempt['is_negative']:
                        message += 'К сожалению, в работе нашлись ошибки.'
                    else:
                        message += 'Преподавателю всё понравилось, '
                        message += 'можно приступать к следующему уроку!'

                bot.send_message(
                    chat_id=chat_id,
                    text=message
                )

        except requests.exceptions.ReadTimeout:
            log.warning('Ошибка времени запроса. Продолжайте пробовать...')
        except requests.exceptions.ConnectionError:
            log_message = 'Ошибка при подключении к интернету. '
            log_message += 'Следующая попытка через 15 минут.'

            log.warning(log_message)
            sleep(900)
