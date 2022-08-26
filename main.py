from time import sleep

import requests
import telegram
from environs import Env


if __name__ == '__main__':
    env = Env()
    env.read_env()

    dvmn_token = env('DVMN_TOKEN')
    tg_token = env('TG_TOKEN')
    chat_id = env('TG_CHAT_ID')

    bot = telegram.Bot(token=tg_token)

    url = 'https://dvmn.org/api/long_polling/'

    headers = {
        'Authorization': f'Token {dvmn_token}'
    }

    params = {}

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
                params = {'timestamp': review_data['timestamp_to_request']}
            elif review_data['status'] == 'found':
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
            continue
        except requests.exceptions.ConnectionError:
            sleep(900)
