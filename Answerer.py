from flask import Flask, request, json
from settings import *
from data import *
import vk
import random

def lottery(message, user_id):
    s = ""
    random.seed()
    a = random.randint(0, 9)
    s = "Ты не выйграл ламборгини"
    if a == 0:
        s += "\nНО ТЫ ВЫЙГРАЛ ПОЕЗДКУ В 503 С ДРУГОМ НОСКОМ"

    return s



def wanna_ticket(message, user_id):
    s = ""
    random.seed()
    a = random.randint(1, 31)
    s = f"Билет № {a}\n"
    if a in tickets:
        s += tickets[a]
    else:
        s += "Error"
    user_tickets[user_id] = a

    return s



def get_answer(message, user_id):
    s = ""
    if user_id in user_tickets:
        s = f"Ответ на билет № {user_tickets[user_id]}\n"
        if user_id == "366018072":
            s = "Вы слишком особенный для ответов"
        else:
            s += answers[user_tickets[user_id]]
    else:
        s = "Для начала вытяни билет"

    return s



def ticket(message, user_id):
    s = ""
    if len(message) == 7:
        if int(message[6]) != 0:
            s = f"Билет № {int(message[6])}\n"
            s += tickets[int(message[6])]
            user_tickets[user_id] = int(message[6])
        else:
            s = "Укажите номер от одного до тридцати"
    elif len(message) == 8:
        if int(message[6:8]) <= 30:
            s = f"Билет № {int(message[6:8])}\n"
            s += tickets[int(message[6:8])]
            user_tickets[user_id] = int(message[6:8])
        else:
            s = "Укажите номер от одного до тридцати"
    else:
        s = "Укажите номер билета, условие которого вы хочете получить"

    return s



def answer(message, user_id):
    s = ""
    if len(message) == 7:
        if int(message[6]) != 0:
            s = f"Ответ на билет № {int(message[6])}\n"
            s += answers[int(message[6])]
        else:
            s = "Укажите номер от одного до тридцати"
    elif len(message) == 8:
        if int(message[6:8]) <= 30:
            s = f"Ответ на билет № {int(message[6:8])}\n"
            s += answers[int(message[6:8])]
        else:
            s = "Укажите номер от одного до тридцати"
    else:
        ss = get_answer(message, user_id)
        s = "Номер не указан."
        if (ss != "Для начала вытяни билет"):
            s += f" Вот ответ на последний вытянутый билет\n{ss}"
        else:
            s += f" А раньше билетов ты не вытягивал. Поэтому для начала вытяни билет командой 'дай билет', 'хочу билет' или 'билет N'(N - число от 1 до 30)"

    return s



def baka(message, user_id):
    s = "(⇀‸↼‶)"

    return s



def mailing(message, user_id, admines, users):
    s = ""
    """
    session = vk.Session()
    api = vk.API(session, v=5.69)
    user = {"id":user_id, "role":"administrator"}
    if (user_id == main_admin or user in admines['items']) and len(message) > 9:
        api.messages.send(access_token=token, user_id=str(user_id), message="Полетели")
        s = f"Рассылка от vk.com/id{user_id}\n"
        s += message[9:len(message)].capitalize()
        s.capitalize()
        sc = 0
        for cur in users['items']:
            api.messages.send(access_token=token, user_id=str(cur), message=s)
            sc += 1

        api.messages.send(access_token=token, user_id=str(user_id), message=f"Сообщение отправлено {sc} пользователям")
        s = ""
    else:
        if not (user_id == main_admin or user in admines['items']):
            s = "ну, ты не админ для такого (или просто что-то криво работает)"
        elif len(message) < 10:
            s = "Введи сообщение"
        else:
            s = "Err"
    """
    s = "Mailing is now inactive. Sorry"
    return s



def baldej(message, user_id, admines):
    s = ""
    session = vk.Session()
    api = vk.API(session, v=5.69)
    user = {"id":user_id, "role":"administrator"}
    if (user_id == main_admin or user in admines['items']) and len(message) > 7:
        s = f"Балдежная рассылка от vk.com/id{user_id}\n"
        check = ""
        s += message[7:len(message)].capitalize()
        s.capitalize()
        sc = 0
        for cur in admines['items']:
            if cur['id'] != user_id and (cur['role'] == "administrator" or cur['role'] == "creator"):
                api.messages.send(access_token=token, user_id=str(cur['id']), message=s)
                sc += 1
                check += f"Сообщение отправлено vk.com/id{cur['id']}\n"
        s = ""
        api.messages.send(access_token=token, user_id=str(user_id), message=check)
    else:
        if not (user_id == main_admin or user in admines['items']):
            s = "ну, ты не админ для такого (или просто что-то криво работает)"
        elif len(message) < 8:
            s = "Введи сообщение"
        else:
            s = "Err"

    return s



def gitelman(message, user_id):
    s = ""
    s = "https://www.youtube.com/channel/UCcpCC6H9EqNZ6iM2gnuzwxQ/videos"

    return s



def hello(message, user_id):
    s = ""
    if message == "привет":
        s = "Привет, \n Напиши любую команду из списка ниже (Caps не влияет на распознавание команды)\n\n"
    else:
        s = "Похоже, что-то пошло не так. Напиши команды именно из списка ниже (Caps не влияет на распознавание команды)\n\n"
    for i in command:
        s += f"{i}\n"

    return s



def message_new(data):
    session = vk.Session()
    api = vk.API(session, v=5.69)

    user_id = data['user_id']

    msg = data['id']
    sending = False
    if (user_id in last_msg and msg > last_msg[user_id]) or not user_id in last_msg:
        last_msg[user_id] = msg
        sending = True

    s = ""

    if sending:
        s = ""

        message = data['body']
        message.strip()
        message = message.lower()
        admines = api.groups.getMembers(access_token=token, group_id=id_group, filter='managers')
        user = {"id":user_id, "role":"administrator"}

        if message.startswith("хочу билет") or message.startswith("дай билет"):
            s = wanna_ticket(message, user_id)
        elif message.startswith("дай ответ") or message.startswith("хочу ответ"):
            s = get_answer(message, user_id)
        elif message.startswith("билет"):
            s = ticket(message, user_id)
        elif message.startswith("ответ"):
            s = answer(message, user_id)
        elif message.startswith("лотерея"):
            s = lottery(message, user_id)
        elif message.startswith("baka"):
            s = baka(message, user_id)
        elif message.startswith("рассылка"):
            s = mailing(message, user_id, admines, users)
        elif message.startswith("балдеж"):
            s = baldej(message, user_id, admines)
        elif message.startswith("хочу балдеж") or message.startswith("дай балдеж") or message.startswith("гительман"):
            s = gitelman(message, user_id)
        else:
            s = hello(message, user_id)

        if (user_id == main_admin or user in admines['items']) and s != "":
            s = str(s) + "\n<3 <3 <3"

        issub = api.groups.isMember(access_token=token, group_id=id_group, user_id=user_id)
        if not issub:
            s += "\nКруто там тебе сидится без подписки, а?"

    return s



def group_leave(data):
    s = ""
    user_id = data['user_id']
    if  user_id in user_leave:
        s = "Ну и иди, тебя никто не держит!"
    else:
        s = "Ну правильно, ливай, блин. Но я тебя уже запомнил!"
        user_leave.append(user_id)

    return s



def group_join(data):
    s = ""
    user_id = data['user_id']
    if user_id in user_leave:
        s = "А, это тот, который ливал. Даже не поприветствую!"

    return s



def group_officers_edit(data):
    lvl_old = data['level_old']
    lvl_new = data['level_new']
    if lvl_old == 3 and lvl_new != 3:
        admins.remove(user_id)
        s = "Вы были удалены из администраторов сообщества"
    elif lvl_old != 3 and lvl_new == 3:
        s = "Добро пожаловать в админы"

    return s



def group_change_settings(data):
    if 'title' in data['changes'] and user_id != main_admin:
        tit_old = data['changes']['title']['old_value']
        tit_new = data['changes']['title']['new_value']
        s = f"Юзер vk.com/id{user_id} изменил название беседы с '{tit_old}' на '{tit_new}'"
        user_id = main_admin
