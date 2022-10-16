TOKEN = ''
GROUP_ID = 0

INTENTS = [
    {
        'name':'дата проведения',
        'tokens': ('когда','сколько','дата','дату'),
        'scenario': None,
        'answer':'вечеринка пройдет 15.02.2023'
    },
    {
        'name': 'место проведения',
        'tokens': ('где', 'место', 'локация', 'адрес'),
        'scenario': None,
        'answer': 'шабаш пройдет по адресу: г. Москва, Кудыкина Гора, д. 13, стр. 3'
    },
    {
        'name': 'регистрация',
        'tokens': ('регис', 'добав', 'пригл'),
        'scenario': 'registration',
        'answer': None
    }
]

SCENARIOS = {
    'registration': {
        'first_step': 'step1',
        'steps': {
            'step1': {
                'text': 'для регистрации введите имя:',
                'failure_text': 'ошибка. имя должно состоять из 2-30 букв и (если нужно) дефиса. попробуйте снова',
                'handler': 'handle_name',
                'next_step': 'step2'
            },
            'step2': {
                'text': 'введите email для обратной связи:',
                'failure_text': 'ошибка. попробуйте ещё раз',
                'handler': 'handle_email',
                'next_step': 'step3'
            },
            'step3': {
                'text': 'спасибо за регистрацию, {name}. вот ваш билет, распечатайте его',
                'image': 'generate_invite_handler',
                'failure_text': None,
                'handler': None,
                'next_step': None
            }

        }
    }
}

DEFAULT_ANSWER = 'хм. не знаю как на это ответить. но могу рассказать, ' \
                 'где и когда будет следующий  шабаш (тематическая вечеринка).' \
                 ' и вышлю приглашение ;)'

DB_CONFIG = dict(
    provider='postgres',
    user='',
    password='1234',
    host='localhost',
    database='vk_chat_bot'
)