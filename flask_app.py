from flask import Flask, request, json
from settings import *
from data import *

import vk
import random
import time
import Answerer

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from DebDoDab!'

"""
def write_msg(user_id, s):
    s = "Доброго ранку"
    api.messages.send(access_token=token, user_id='366018072', message=s)
    api.messages.send(access_token=token, user_id='177933956', message=s)
"""

@app.route('/', methods=['POST'])
def processing():
    session = vk.Session()
    api = vk.API(session, v=5.69)
    data = json.loads(request.data)

    if 'user_id' in data['object']:
        user_id = data['object']['user_id']
    else:
        return f"Wtf?! Where is 'user_id' in {data['object']}"

    if 'type' not in data.keys():
        return 'not vk'

    elif data['type'] == 'confirmation':
        return confirmation_token

    elif data['type'] == 'message_new':
        s = Answerer.message_new(data['object'])

    elif data['type'] == 'group_leave':
        s = Answerer.group_leave(data['object'])

    elif data['type'] == 'group_join':
        s = Answerer.group_join(data['object'])

    elif data['type'] == 'group_officers_edit':
        s = Answerer.group_officers_edit(data['object'])

    elif data['type'] == 'group_change_settings':
        user_id = main_admin
        s = Answerer.group_change_settings(data['object'])

    else:
        return f"Error. I don't know why, but I hope we'll fix it\nI just don't know what to do with {data['type']}"


    if s != "":
        s.capitalize()
        api.messages.send(access_token=token, user_id=str(user_id), message=s)

    return 'ok'

