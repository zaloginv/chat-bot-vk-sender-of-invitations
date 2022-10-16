"""
принимает на вход текст входящего сообщения (text), словарь (dict) и возвращается bool:
true, если шаг пройден, False, если данные не верные
"""
import re
from generate_invite import generate_invite

re_name = re.compile(r'^[\w\-\s]{2,30}$')
re_email = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')

def handle_name(text, context):
    match = re.match(re_name, text)
    if match:
        context['name'] = text
        return True
    else:
        return False

def handle_email(text, context):
    matches = re.findall(re_email, text)
    if len(matches) > 0:
        context['email'] = matches[0]
        return True
    else:
        return False

def generate_invite_handler(text, context):
    return generate_invite(name=context['name'], email=context['email'])