# Weather

Telegram-бот на Python: показывает текущую погоду и прогноз на сегодня или завтра для выбранного города. Данные берутся из [OpenWeatherMap](https://openweathermap.org/api).

## Возможности

После команды `/start` бот предлагает кнопки:

- **Выбрать город** — сохраняет город пользователя (по `user_id` в `users.json`).
- **Погода сейчас** — температура, «ощущается как», описание, скорость и направление ветра.
- **Погода на сегодня** / **Погода на завтра** — сводка по прогнозу: описание, мин/макс температура, ветер, влажность.

Если город ещё не выбран, бот сначала попросит его отправить. На произвольный текст без кнопок бот не отвечает.

## Структура проекта

```
main.py                 # запуск бота, обработчики команд и кнопок
bot_functions.py        # разбиение прогноза на сегодня и завтра
response_formatting.py  # текст сводки, подписи ветра и влажности
secrets.py              # токен Telegram-бота и ключ OpenWeatherMap
users.json              # сохранённые города пользователей
```

## Требования

- Python 3
- токен бота от [@BotFather](https://t.me/BotFather)
- API-ключ [OpenWeatherMap](https://openweathermap.org/api)

## Установка

```bash
python -m venv .venv
```

Windows (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

Linux / macOS:

```bash
source .venv/bin/activate
```

Зависимости:

```bash
pip install pyTelegramBotAPI requests
```

## Настройка

В `secrets.py` укажите свои ключи:

```python
secrets = {
    'BOT_API_TOKEN': 'ваш_токен_telegram_бота',
    'API_WEATHER': 'ваш_ключ_openweathermap',
}
```


## Запуск

```bash
python main.py
```

Бот работает в режиме long polling, пока процесс не остановить.

## Как пользоваться

1. Найдите бота в Telegram и отправьте `/start`.
2. Нажмите **Выбрать город** и напишите название города (например, `Москва`).
3. Используйте кнопки **Погода сейчас**, **Погода на сегодня** или **Погода на завтра**.
