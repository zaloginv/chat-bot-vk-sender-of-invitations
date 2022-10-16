from copy import deepcopy
from unittest import TestCase
from unittest.mock import patch, Mock, ANY

from pony.orm import rollback
from vk_api.bot_longpoll import VkBotMessageEvent, VkBotEvent

import settings
from bot import Bot
from generate_invite import generate_invite
from models import db


def isolate_db(test_func):
    def wrapper(*args, **kwargs):
        with db.session:
            test_func(*args, **kwargs)
            rollback()



class Test1(TestCase):
    RAW_EVENT = {'group_id': 216129149, 'type': 'message_new', 'event_id': 'ad3767b83e0f21a6abbe5044d1fa34b28cf02651',
                 'v': '5.131',
                 'object': {'message': {'date': 1664369984, 'from_id': 676003830, 'id': 35, 'out': 0,
                                        'attachments': [],
                                        'conversation_message_id': 34, 'fwd_messages': [],
                                        'important': False, 'is_hidden': False, 'peer_id': 676003830, 'random_id': 0,
                                        'text': 'приветики'},
                            'client_info': {'button_actions': ['text', 'vkpay', 'open_app',
                                                               'location', 'open_link', 'callback', 'intent_subscribe',
                                                               'intent_unsubscribe'],
                                            'keyboard': True, 'inline_keyboard': True, 'carousel': True, 'lang_id': 0}}}

    def test_run(self):
        count = 5
        obj = {'a':1}
        events = [obj] * count
        long_poller_mock = Mock(return_value=events)
        long_poller_listen_mock = Mock()
        long_poller_listen_mock.listen = long_poller_mock

        with patch('bot.vk_api.VkApi'):
            with patch('bot.VkBotLongPoll', return_value=long_poller_listen_mock):
                bot = Bot('','')
                bot.on_event = Mock()
                bot.send_image = Mock()
                bot.run()

                bot.on_event.assert_called()
                bot.on_event.assert_any_call(obj)

                assert bot.on_event.call_count == count


    INPUTS = [
        'привет',
        'когда?',
        'а где?',
        'пригласи меня',
        'Василиса',
        'почта - witchwmail.com',
        'witch@wmail.com',
    ]

    EXPECTED_OUTPUTS = [
        settings.DEFAULT_ANSWER,
        settings.INTENTS[0]['answer'],
        settings.INTENTS[1]['answer'],
        settings.SCENARIOS['registration']['steps']['step1']['text'],
        settings.SCENARIOS['registration']['steps']['step2']['text'],
        settings.SCENARIOS['registration']['steps']['step2']['failure_text'],
        settings.SCENARIOS['registration']['steps']['step3']['text'].format(name='Василиса', email='witch@wmail.com')
    ]

    @isolate_db
    def test_run_ok(self):
        send_mock = Mock()
        api_mock = Mock()
        api_mock.messages.send = send_mock

        events = []

        for input_text in self.INPUTS:
            event = deepcopy(self.RAW_EVENT)
            event['object']['message']['text'] = input_text
            events.append(VkBotMessageEvent(event))

        long_poller_mock = Mock()
        long_poller_mock.listen = Mock(return_value=events)

        with patch('bot.VkBotLongPoll', return_value=long_poller_mock):
            bot=Bot('','')
            bot.api = api_mock
            bot.send_image = Mock()
            bot.run()

        assert send_mock.call_count == len(self.INPUTS)

        real_outputs = []
        for call in send_mock.call_args_list:
            args, kwargs = call
            real_outputs.append(kwargs['message'])
        assert real_outputs == self.EXPECTED_OUTPUTS

    def test_image_generation(self):
        invite_file = generate_invite('Катя','katya@email.com')

        with open('file/invite_example.png', 'rb') as expected_file:
            expected_bytes = expected_file.read()

        assert invite_file.read() == expected_bytes