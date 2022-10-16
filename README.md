# vk_chat_bot
бот, предназначенный для отправки приглашений на любое мероприятие (в реализации настроен на тематическую вечеринку) по сценарию:
- ограниченно понимает естественный язык благодаря извлечению токенов
- умеет совершать сценарии по конфигу, валидировать данные, переспрашивать и т.д.
- стабилен благодаря использованию базы данных (postgres + ponyorm). сценарии можно продолжить после перезапуска
- билеты генерируются автоматически, нужно лишь указать имя и фамилию. билет приходит пользователю в ответном сообщении
- покрыт автотестами

**bot.py** - основной файл, содержащий конфигурацию и класс Бота

скриншоты работы лежат в examples.pdf
