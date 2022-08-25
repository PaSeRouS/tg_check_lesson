# Бот проверок работ от Девмана

Это скрипт позволяет получать уведомления о проверке работ на ресурсе [Devman](https://dvmn.org/).

## Установка

Python3 должен быть установлен на вашем комптьютере.

Используйте следующую команду для установки зависимостей, нужных для корректной работы скрипта.
```
pip install -r requirements.txt
```

В корне создайте файл `.env`, в котором будут храниться переменные окружения, нужные для работы скрипта.

`DVMN_TOKEN`=Ваш персональный токен с сайта [dvmn.org](https://dvmn.org/api/docs/).   
`TG_TOKEN`=Токен вашего [телеграм-бота](https://core.telegram.org/bots#6-botfather).  
`TG_CHAT_ID`=Ваш идентификационный номер в телеграме. Можно узнать у бота `@userinfobot`. 

После того как все библиотеки установлены, а переменны окружения заполнены можно запустить скрипт следующей командой из кнсоли, находясь в папке со скриптом.

```
python main.py 
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
