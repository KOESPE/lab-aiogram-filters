# telegram-bot-api-1

## Скриншот работы
![image](https://github.com/KOESPE/telegram-bot-api-1/assets/34860174/a4cf60be-d987-44ad-8d98-39d843cd3b01)

## Подготовка к работе
1. Создать новый проект
2. Создать виртуальное окружение
```console
$ python3 -m venv venv
```
3. Установить необходимые библиотеки
```console
$ pip install aiogram
$ pip install python-dotenv
```
4. Переименовать файл .env.example в .env и вставить свой токен бота

Готово! Осталось запустить файл main.py

types_list: list[str] = [
   'sticker',   - стикер
   'photo',    - фото
   'voice',    - голосовое сообщение
   'video',    - видеосообщение
   'audio',    - аудио
   'location',    - геолокация
   'forward_origin',   - пересланное сообщение
   'animation',    - гиф-анимация
   'poll',    - опрос
   'story',    - история
   'contact',    - контакт
   'video_note',    - кружочек
   'text',    - текст
   'document'    - файл
]
