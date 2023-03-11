from flask import Flask, request
from flask_ngrok import run_with_ngrok
import logging
import json
import random
from classes import Monster, Bonus, Armament, Proklate, Race
from bonuses import bonuses as bonuses_cards
from monsters import monsters as monsters_cards
from curses import curses as proklates_cards
from armament import armament as armores_cards
from race import race as race_cards

app = Flask(__name__)
run_with_ngrok(app)

logging.basicConfig(level=logging.INFO)

sessionStorage = {}

marks = '''!()-[]{};?@#$%:'"\,./^&amp;*_'''
link = '1533899/8ce30965e087db5e9bdc'
# первый элемент отвечает за монстра или нет, то есть 0 - это проклятье, 2 - раса
# 0 - бонус, 1 - оружие
all_treasures = bonuses_cards + armores_cards  # изменить!!!
all_doors_for_game = monsters_cards + proklates_cards  # изменить!!!  # c проклятьями
all_doors_for_hero = monsters_cards + race_cards  # изменить!!!

dict_treasures = {i: all_treasures[i] for i in range(len(all_treasures))}
dict_doors_for_game = {i: all_doors_for_game[i] for i in range(len(all_doors_for_game))}
dict_doors_for_hero = {i: all_doors_for_hero[i] for i in range(len(all_doors_for_hero))}

# картинки
all_picturs = {'monster': ['1521359/cbb76ee4b27267769e5c',
                           '1652229/e4a4c4f9a8383b7c5497', '1652229/ca2469bc833d995da0bb'],
               'proklate': ['965417/5e0db306ecb8d6c76ef0'], 'head': ['1521359/fbf517e919e2a07f7fa5'],
               'body': ['1521359/e35677d1985411762bcb'], 'leg': ['1030494/1efe863b5b43908679e6'],
               'bonus': ['1533899/e3cbd21cacb462d4e482'], 'weapon': ['1030494/899f7a72796d5e905c43'],
               'дварф': ['1521359/0009a96980687b243207'], 'эльф': ['1533899/540e8191f506f23f37b0'],
               'хафлинг': ['1533899/ca930bb4e692625bd227']}


@app.route('/', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')
    # выводим эпоху юзера
    try:
        print(sessionStorage[request.json['session']['user_id']]['epoch'])
        print(sessionStorage[request.json['session']['user_id']]['level'])
    except:
        pass
    response = {  # то что отправляем
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(request.json, response)  # функция

    logging.info(f'Response:  {response!r}')

    return json.dumps(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        sessionStorage[user_id] = {
            'level': 1,  # уровень
            'epoch': '11',  # эпоха
            'weapon': [],  # оружие
            'class': race_cards[1],  # раса
            'monster': None,  # монстры при битве
            'overall_strength': 0,  # общая сила
            'bonus_strength': 0,  # бонус к силе
            'money': 0,  # деньги
            'luck': 2,  # удача
            'armor': {'head': None, 'body': None, 'leg': None},  # оружие
            'cards_on_hands': [],  # карты на руках
            'is_alive': True,  # живой ли
            'what_treasures_stay': list(range(len(dict_treasures))),  # какие монстры остались
            'what_doors_stay': list(range(len(dict_doors_for_hero))),  # какие двери остались
            'cards_to_sell': None  # карты на продажу
        }
        # Заполняем текст ответа
        res['response']['text'] = 'Привет! Добро пожаловать в игру "mini Манчкин"!' \
                                  ' Ты уже знаешь правила этой игры!?'
        # Получим подсказки
        res['response']['buttons'] = [{'title': 'Да', 'hide': True}, {'title': 'Нет', 'hide': True}]
        return
    if sessionStorage[user_id]['epoch'][0] == '1':
        if sessionStorage[user_id]['epoch'] == '11':  # знает ли правила
            if req['request']['original_utterance'].lower() in ['да']:
                res['response']['text'] = 'Хорошо! Ты готов к приключениям по подземельям!?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                              {'title': 'Нет', 'hide': True}]
                sessionStorage[user_id]['epoch'] = '12'  # начинаем ли игру
            elif req['request']['original_utterance'].lower() in ['нет']:
                res['response']['text'] = 'Тогда давай я расскажу тебе правила: ...\n' \
                                          'Вы поняли правила?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                              {'title': 'Нет', 'hide': True}]
                sessionStorage[user_id]['epoch'] = '13'  # доп правила
            else:  # не поняли
                res['response']['text'] = 'Я вас не поняла, извините... Так да или нет?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                              {'title': 'Нет', 'hide': True}]
        elif sessionStorage[user_id]['epoch'] == '12':  # согласились ли играть <----
            if req['request']['original_utterance'].lower() in ['да']:
                res['response']['text'] = 'Вы зашли в лабиринт, везде темно,' \
                                          ' но вы увидели несколько дверей, в которых могут' \
                                          ' таяться монстры и проклятья.... Берегите себя,' \
                                          ' да будет игра!!!\n'
                # берем и удалем id
                if len(sessionStorage[user_id]['what_treasures_stay']) >= 4 and len(
                        sessionStorage[user_id]['what_doors_stay']) >= 4:
                    ids_treasures = random.sample(sessionStorage[user_id]['what_treasures_stay'],
                                                  4)  # берем id сокровищ
                    ids_doors = random.sample(sessionStorage[user_id]['what_doors_stay'],
                                              4)  # берем id дверей
                    sessionStorage[user_id]['cards_on_hands'] = [dict_treasures[i] for i in
                                                                 ids_treasures] + [
                                                                    dict_doors_for_hero[i]
                                                                    for i in ids_doors]
                    for i in ids_treasures:
                        sessionStorage[user_id]['what_treasures_stay'].remove(i)
                    for i in ids_doors:
                        sessionStorage[user_id]['what_doors_stay'].remove(i)
                else:
                    if len(sessionStorage[user_id]['what_treasures_stay']) < 4:
                        sessionStorage[user_id]['what_treasures_stay'] = list(
                            range(len(dict_treasures)))
                    if len(sessionStorage[user_id]['what_doors_stay']) < 4:
                        sessionStorage[user_id]['what_doors_stay'] = list(
                            range(len(dict_doors_for_hero)))
                    ids_treasures = random.sample(sessionStorage[user_id]['what_treasures_stay'],
                                                  4)  # берем id сокровищ
                    ids_doors = random.sample(sessionStorage[user_id]['what_doors_stay'],
                                              4)  # берем id дверей
                    sessionStorage[user_id]['cards_on_hands'] = [dict_treasures[i] for i in
                                                                 ids_treasures] + [
                                                                    dict_doors_for_hero[i]
                                                                    for i in ids_doors]
                    for i in ids_treasures:
                        sessionStorage[user_id]['what_treasures_stay'].remove(i)
                    for i in ids_doors:
                        sessionStorage[user_id]['what_doors_stay'].remove(i)
                # удаляем id

                # так если у нас в списке будут классы, иначе:
                # создаем 4 карты двери и сокровищ
                # treasures = [
                #     Armament(*dict_treasures[i][1:]) if dict_treasures[i][0] != 0 else Bonus(
                #         *dict_treasures[i][1:]) for i in ids_treasures]
                # # проверка! может быть раса
                # doors = [Monster(*dict_doors_for_hero[i][1:]) if dict_doors_for_hero[i][0] != 0
                #          else Proklate(*dict_doors_for_hero[i][1:]) for i in ids_doors]
                # сортируем
                sessionStorage[user_id]['cards_on_hands'] = sort_cards(user_id)
                # даем ответ для алисы
                text = show_names(user_id)  # создаем текст для вывода всех предметов
                res['response']['text'] += '<---------\n'
                res['response']['text'] += text
                k, text = find_free_cards(user_id)  # какие карты можно положить?
                res['response']['text'] += text
                res['response']['text'] += '--------->\n'
                res['response']['text'] += 'Какие карты вы хотите положить на стол? (номера)'
                res['response']['buttons'] = [{'title': 'Никакие', 'hide': True}]
                sessionStorage[user_id]['epoch'] = '2'  # начинаем игру
            elif req['request']['original_utterance'].lower() in ['нет']:
                res['response']['text'] = 'Приходите когда будете готовы! До скорых встреч!'
                res['response']['end_session'] = True
            else:  # не поняли
                res['response']['text'] = 'Я вас не поняла, извините... Так да или нет?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                              {'title': 'Нет', 'hide': True}]

        elif sessionStorage[user_id]['epoch'] == '13':  # поняли ли правила
            if req['request']['original_utterance'].lower() in ['да']:
                res['response']['text'] = 'Хорошо! Ты готов к приключениям по подземельям!?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                              {'title': 'Нет', 'hide': True}]
                sessionStorage[user_id]['epoch'] = '12'  # начинаем ли игру
            elif req['request']['original_utterance'].lower() in ['нет']:
                res['response']['text'] = 'Тогда лови ссылку для углубленного' \
                                          ' разбора: https://add-hobby.ru/munchkin.html \n' \
                                          'Хорошо! Ты готов к приключениям по подземельям!?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                              {'title': 'Нет', 'hide': True},
                                              {"title": "Правила",
                                               "url": "https://add-hobby.ru/munchkin.html",
                                               "hide": True}]
                sessionStorage[user_id]['epoch'] = '12'  # начинаем ли игру
            else:  # не поняли
                res['response']['text'] = 'Я вас не поняла, извините... Так да или нет?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                              {'title': 'Нет', 'hide': True}]
    elif sessionStorage[user_id]['epoch'][0] == '2':
        if sessionStorage[user_id]['epoch'] == '2':  # какие карты он достает
            text_res = req['request']['original_utterance'].lower()
            if 'никакие' in text_res:  # ничего не хочет выкладывать
                res['response']['text'] = 'Вы отказались класть карты!\n'
                res['response']['text'] += '<---------\n'
                res['response']['text'] += 'Хорошо, на вашем столе:\n'
                res['response']['text'] += show_names(user_id)
                res['response']['text'] += '--------->\n'
                # доп вопрос
                res['response']['text'] += 'Вы готовы открыть дверь?\n'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                              {'title': 'Нет', 'hide': True}]
                sessionStorage[user_id]['epoch'] = '22'
                # след
                return
            num = []

            for i in text_res.split():
                # просто удаляем знаки препинания
                word = ''
                for x in i:
                    if x not in marks:
                        word += x
                print(word)
                if word.isdigit():
                    num.append(word)
            # проверка
            if len(num) == 0:
                res['response'][
                    'text'] = 'В вашем ответе отсутствуют цифры! Введите цифры! Например 1, 2...\n'
                res['response']['text'] += '<---------\n'
                res['response']['text'] += show_names(user_id)
                k, text = find_free_cards(user_id)  # какие карты можно положить?
                res['response']['text'] += text
                res['response']['text'] += '--------->\n'
                res['response']['text'] += 'Какие карты вы хотите положить на стол? (номера)'
                res['response']['buttons'] = [{'title': 'Никакие', 'hide': True}]
                return
            res['response'][
                'text'] = f'Вы выбрали позиции: {", ".join(num)}\n'
            for x in num:
                if int(x) <= 0 or int(x) > len(sessionStorage[user_id]['cards_on_hands']):
                    res['response'][
                        'text'] += f'Ошибка! Вы должны говорить цифры в диапазоне от 1 до {len(sessionStorage[user_id]["cards_on_hands"])}\n'
                    res['response']['text'] += '<---------\n'
                    res['response']['text'] += show_names(user_id)
                    k, text = find_free_cards(user_id)  # какие карты можно положить?
                    res['response']['text'] += text
                    res['response']['text'] += '--------->\n'
                    res['response']['text'] += 'Какие карты вы хотите положить на стол? (номера)'
                    res['response']['buttons'] = [{'title': 'Никакие', 'hide': True}]
                    return
            t, cards = is_all_right(user_id, [int(i) - 1 for i in
                                              num])  # t - без ошибок? cards - текст функции
            if t:
                # res['response']['text'] += 'Вы выбрали карточки:\n' + cards

                res['response']['text'] += 'Хорошо, на вашем столе:\n'
                res['response']['text'] += '<---------\n'
                res['response']['text'] += show_names(user_id)
                res['response']['text'] += '--------->\n'
                k, text = find_free_cards(user_id)
                if k == 0:
                    # доп вопрос
                    res['response']['text'] += 'Вы готовы открыть дверь?\n'
                    res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                                  {'title': 'Нет', 'hide': True}]
                    sessionStorage[user_id]['epoch'] = '22'
                    # след
                else:
                    res['response'][
                        'text'] += 'У вас есть карты, которые можно положить! Хотите это сделать?'
                    res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                                  {'title': 'Нет', 'hide': True}]
                    sessionStorage[user_id]['epoch'] = '21'
            else:
                res['response']['text'] += 'Ошибка!\n' + cards
                res['response']['text'] += '<---------\n'
                res['response']['text'] += show_names(user_id)
                k, text = find_free_cards(user_id)  # какие карты можно положить?
                res['response']['text'] += text
                res['response']['text'] += '--------->\n'
                res['response']['text'] += 'Какие карты вы хотите положить на стол? (номера)'
                res['response']['buttons'] = [{'title': 'Никакие', 'hide': True}]
                return
        elif sessionStorage[user_id]['epoch'] == '21':  # хочет ли положить еще карты?
            if req['request']['original_utterance'].lower() in ['да']:
                res['response']['text'] = 'Хорошо! Ваши характеритики:\n'
                text = show_names(user_id)  # создаем текст для вывода всех предметов
                res['response']['text'] += '<---------\n'
                res['response']['text'] += text
                k, text = find_free_cards(user_id)  # какие карты можно положить?
                res['response']['text'] += text
                res['response']['text'] += '--------->\n'
                res['response']['text'] += 'Какие карты вы хотите положить на стол? (номера)'
                res['response']['buttons'] = [{'title': 'Никакие', 'hide': True}]
                sessionStorage[user_id]['epoch'] = '2'
            elif req['request']['original_utterance'].lower() in ['нет']:
                res['response'][
                    'text'] = 'Вы отказались выкладывать карты, хорошо, вы готовы открывать дверь?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                              {'title': 'Нет', 'hide': True}]
                sessionStorage[user_id]['epoch'] = '22'
            else:  # не поняли
                res['response']['text'] = 'Я вас не поняла, извините... Так да или нет?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                              {'title': 'Нет', 'hide': True}]
        elif sessionStorage[user_id]['epoch'] == '22':  # хочет открывать дверь?
            if req['request']['original_utterance'].lower() in ['да']:  # ОТКРЫВАЕМ ДВЕРЬ
                res['response']['text'] = f'Вы стучитесь в дверь и ...\n'  # доделать
                class_card = pull_out_card_door(user_id, res)  # открываем дверь
                if class_card == 1:  # пользователю попался монстр
                    sessionStorage[user_id]['epoch'] = '20'
                elif class_card == 3:  # пользователь получил проклятье
                    res['response']['card']['title'] = 'Вы готовы продолжать?'
                    res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                                  {'title': 'Нет', 'hide': True}]
                    sessionStorage[user_id]['epoch'] = '30'
                elif class_card == 4:  # выпала расса
                    res['response']['card']['title'] = 'Вы готовы продожать?'
                    res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                                  {'title': 'Нет', 'hide': True}]
                    sessionStorage[user_id]['epoch'] = '30'
            elif req['request']['original_utterance'].lower() in ['нет']:
                res['response']['text'] = 'Вы хотите выйти из игры?\n'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                              {'title': 'Нет', 'hide': True}]
                sessionStorage[user_id]['epoch'] = '23'
            else:  # не поняли
                res['response']['text'] = 'Я вас не поняла, извините... Так да или нет?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                              {'title': 'Нет', 'hide': True}]
        elif sessionStorage[user_id]['epoch'] == '20':  # Будет ли сражаться герой?
            if req['request']['original_utterance'].lower() in ['да']:
                print('СРАЖАЕМСЯ!')
                n = fight_with_monster(user_id, res)
                if n == 1:  # может победить
                    catch_bonus(user_id, res)  # будет картинка
                    res['response']['card']['title'] = 'Вы его выйграли! ' + res['response']['card'][
                        'title']
                    print([i.title for i in sessionStorage[user_id]['cards_on_hands']])
                    sessionStorage[user_id]["bonus_strength"] = 0
                    sessionStorage[user_id]['monster'] = None
                    sessionStorage[user_id]['epoch'] = '33'
                else:  # не может победить
                    if len([i for i in sessionStorage[user_id]['cards_on_hands'] if
                            i.__class__.__bases__[
                                0].__name__ == 'BonusBase']) == 0:  # если нет карт бонуса
                        num = random.randint(1, 6)
                        res['response'][
                            'text'] = f'У вас нет бонусов, которые могут вам помочь, вам придётся убегать! Подбрасываю кубик иии вам выпало {num}.\n'
                        what, text = do_bad_things_with_hero(user_id, num)
                        if what == 1:  # смог убежать
                            res['response']['text'] += text
                            res['response']['text'] += 'Вы готовы продолжать?'
                            res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                                          {'title': 'Нет', 'hide': True}]
                            sessionStorage[user_id]['epoch'] = '33'
                            # условие больше 5 карт и начинаем от щедрот
                        elif what == 2:  # выжил
                            res['response']['text'] += text
                            res['response'][
                                'text'] += 'Вы выжили после этого!? Это удивительно!! Идем дальше! '
                            # условие больше 5 карт и начинаем от щедрот
                            res['response']['text'] += 'Вы готовы продолжать?'
                            res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                                          {'title': 'Нет', 'hide': True}]
                            sessionStorage[user_id]['epoch'] = '33'
                        else:  # Умер
                            res['response']['text'] += text
                            res['response'][
                                'text'] += 'Вы умерли - как жалко это признавать. Вы хотите играть дальше?'
                            res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                                          {'title': 'Нет', 'hide': True}]
                            sessionStorage[user_id]['epoch'] = '213'  # продаем карты
                    else:
                        res['response'][
                            'text'] = f'Монстр вас побеждает!\nВаша сила: {sessionStorage[user_id]["overall_strength"] + sessionStorage[user_id]["level"]}\nСила монстра: {sessionStorage[user_id]["monster"].level}\nВы будете использовать бонусы?'
                        res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                                      {'title': 'Нет', 'hide': True}]
                        sessionStorage[user_id]['epoch'] = '25'  # выбираем бонусы
            elif req['request']['original_utterance'].lower() in ['нет']:  # УБЕГАЕМ
                print('УХОДИМ')
                num = random.randint(1, 6)
                res['response'][
                    'text'] = f'Вы отказались с ним сражаться, вам придётся убегать! Подбрасываю кубик иии вам выпало {num}.\n'
                what, text = do_bad_things_with_hero(user_id, num)
                if what == 1:  # смог убежать
                    res['response']['text'] += text
                    # условие больше 5 карт и начинаем от щедрот
                    res['response']['text'] += 'Вы готовы продолжать?'
                    sessionStorage[user_id]['epoch'] = '33'
                    res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                                  {'title': 'Нет', 'hide': True}]
                elif what == 2:  # выжил
                    res['response']['text'] += text
                    res['response'][
                        'text'] += 'Вы выжили после этого!? Это удивительно!! Идем дальше! '
                    # условие больше 5 карт и начинаем от щедрот
                    res['response']['text'] += 'Вы готовы продолжать?'
                    sessionStorage[user_id]['epoch'] = '33'
                    res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                                  {'title': 'Нет', 'hide': True}]
                else:  # Умер
                    res['response']['text'] += text
                    res['response'][
                        'text'] += 'Вы умерли - как жалко это признавать. Вы хотите играть дальше?'
                    res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                                  {'title': 'Нет', 'hide': True}]
                    sessionStorage[user_id]['epoch'] = '213'  # продаем карты
            else:  # не поняли
                res['response']['text'] = 'Я вас не поняла, извините... Так да или нет?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                              {'title': 'Нет', 'hide': True}]
        elif sessionStorage[user_id]['epoch'] == '23':  # уходит из игры?
            if req['request']['original_utterance'].lower() in ['да']:
                res['response']['text'] = 'Приходите когда будете готовы! До скорых встреч!'
                res['response']['end_session'] = True
            elif req['request']['original_utterance'].lower() in ['нет']:  # ОТКРЫВАЕМ ДВЕРЬ
                res['response'][
                    'text'] = f'Тогда сама дверь открывается, не дождавшись вас, и ...\n'  # доделать
                class_card = pull_out_card_door(user_id, res)  # открываем дверь
                if class_card == 1:  # пользователю попался монстр
                    sessionStorage[user_id]['epoch'] = '20'
                elif class_card == 3:  # пользователь получил проклятье
                    res['response']['card']['title'] = 'Вы готовы продолжать?'
                    res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                                  {'title': 'Нет', 'hide': True}]
                    sessionStorage[user_id]['epoch'] = '30'
                elif class_card == 4:  # выпала расса
                    res['response']['card']['title'] = 'Вы готовы продожать?'
                    res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                                  {'title': 'Нет', 'hide': True}]
                    sessionStorage[user_id]['epoch'] = '30'
                # показываем карту и смотря какой класс используем функцию
            else:  # не поняли
                res['response']['text'] = 'Я вас не поняла, извините... Так да или нет?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                              {'title': 'Нет', 'hide': True}]
        elif sessionStorage[user_id]['epoch'] == '25':
            if req['request']['original_utterance'].lower() in ['да']:  # выбираем бонусы
                text = choose_bonus(user_id)
                res['response']['text'] = text
                res['response']['text'] += 'Какие бонусы вы хотите выбрать? (номера)'
                res['response']['buttons'] = [{'title': 'Никакие', 'hide': True}]
                sessionStorage[user_id]['epoch'] = '28'
            elif req['request']['original_utterance'].lower() in ['нет', 'никакие']:  # убегаем
                # проверка может быть он выигрывает!!!
                if sessionStorage[user_id]["overall_strength"] + sessionStorage[user_id]["level"] + \
                        sessionStorage[user_id]["bonus_strength"] > sessionStorage[user_id][
                    "monster"].level:
                    catch_bonus(user_id, res)  # будет картинка
                    res['response']['card']['title'] = 'Вы его выйграли! ' + res['response']['card'][
                        'title']
                    sessionStorage[user_id]["bonus_strength"] = 0
                    sessionStorage[user_id]['monster'] = None
                    sessionStorage[user_id]['epoch'] = '4'  # продаем карты
                else:  # убегаем/умираем
                    num = random.randint(1, 6)
                    res['response'][
                        'text'] = f'У вас нет бонусов, которые могут вам помочь, вам придётся убегать! Подбрасываю кубик иии вам выпало {num}.\n'
                    what, text = do_bad_things_with_hero(user_id, num)
                    if what == 1:  # смог убежать
                        res['response']['text'] += text
                        # условие больше 5 карт и начинаем от щедрот
                        res['response']['text'] += 'Вы готовы продолжать?'
                        sessionStorage[user_id]['epoch'] = '33'
                        res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                                      {'title': 'Нет', 'hide': True}]
                    elif what == 2:  # выжил
                        res['response']['text'] += text
                        res['response'][
                            'text'] += 'Вы выжили после этого!? Это удивительно!! Идем дальше! '
                        # условие больше 5 карт и начинаем от щедрот
                        res['response']['text'] += 'Вы готовы продолжать?'
                        sessionStorage[user_id]['epoch'] = '33'
                        res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                                      {'title': 'Нет', 'hide': True}]
                    else:  # Умер
                        res['response']['text'] += text
                        res['response'][
                            'text'] += 'Вы умерли - как жалко это признавать. Вы хотите играть дальше?'
                        res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                                      {'title': 'Нет', 'hide': True}]
                        sessionStorage[user_id]['epoch'] = '213'  # продаем карты
            else:  # не поняли
                res['response']['text'] = 'Я вас не поняла, извините... Так да или нет?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                              {'title': 'Нет', 'hide': True}]
        elif sessionStorage[user_id]['epoch'] == '28':
            input_text = req['request']['original_utterance']
            if input_text.lower() in ['никакие']:  # убегаем
                # проверка может быть он выигрывает!!!
                if sessionStorage[user_id]["overall_strength"] + sessionStorage[user_id]["level"] + \
                        sessionStorage[user_id]["bonus_strength"] > sessionStorage[user_id][
                    "monster"].level:
                    catch_bonus(user_id, res)  # будет картинка
                    res['response']['card']['title'] = 'Вы его выйграли! ' + res['response']['card'][
                        'title']
                    sessionStorage[user_id]["bonus_strength"] = 0
                    sessionStorage[user_id]['monster'] = None
                    sessionStorage[user_id]['epoch'] = '4'  # продаем карты
                    return
                else:
                    num = random.randint(1, 6)
                    res['response'][
                        'text'] = f'Вы отказались от бонусов, вам придётся убегать! Подбрасываю кубик иии вам выпало {num}.\n'
                    what, text = do_bad_things_with_hero(user_id, num)
                    if what == 1:  # смог убежать
                        res['response']['text'] += text
                        # условие больше 5 карт и начинаем от щедрот
                        res['response']['text'] += 'Вы готовы продолжать?'
                        sessionStorage[user_id]['epoch'] = '33'
                        res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                                      {'title': 'Нет', 'hide': True}]
                    elif what == 2:  # выжил
                        res['response']['text'] += text
                        res['response'][
                            'text'] += 'Вы выжили после этого!? Это удивительно!! Идем дальше! '
                        # условие больше 5 карт и начинаем от щедрот
                        res['response']['text'] += 'Вы готовы продолжать?'
                        sessionStorage[user_id]['epoch'] = '33'
                        res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                                      {'title': 'Нет', 'hide': True}]
                    else:  # Умер
                        res['response']['text'] += text
                        res['response'][
                            'text'] += 'Вы умерли - как жалко это признавать. Вы хотите играть дальше?'
                        res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                                      {'title': 'Нет', 'hide': True}]
                        sessionStorage[user_id]['epoch'] = '213'  # продаем карты
                    return
            num = []
            for i in input_text.split():
                # просто удаляем знаки препинания
                word = ''
                for x in i:
                    if x not in marks:
                        word += x
                print(word)
                if word.isdigit():
                    num.append(word)
            if len(num) == 0:
                res['response'][
                    'text'] = 'В вашем ответе отсутствуют цифры! Введите цифры! Например 1, 2...\n'
                res['response']['text'] += '<---------\n'
                text = choose_bonus(user_id)
                res['response']['text'] += text
                res['response']['text'] += '--------->\n'
                res['response']['text'] += 'Какие бонусы вы хотите выбрать? (номера)'
                res['response']['buttons'] = [{'title': 'Никакие', 'hide': True}]
                return
            res['response'][
                'text'] = f'Вы выбрали позиции: {", ".join(num)}\n'
            for x in num:
                if int(x) <= 0 or int(x) > len(
                        [i for i in sessionStorage[user_id]['cards_on_hands'] if
                         i.__class__.__bases__[0].__name__ == 'BonusBase']):
                    res['response'][
                        'text'] += f"Ошибка! Вы должны говорить цифры в диапазоне от 1 до {len([i for i in sessionStorage[user_id]['cards_on_hands'] if i.__class__.__bases__[0].__name__ == 'BonusBase'])}\n"
                    res['response']['text'] += '<---------\n'
                    text = choose_bonus(user_id)
                    res['response']['text'] += text
                    res['response']['text'] += '--------->\n'
                    res['response']['text'] += 'Какие бонусы вы хотите выбрать? (номера)'
                    res['response']['buttons'] = [{'title': 'Никакие', 'hide': True}]
                    return
            dict_bonus = {}
            k = 1
            for i in sessionStorage[user_id]['cards_on_hands']:
                if i.__class__.__bases__[0].__name__ == 'BonusBase':
                    dict_bonus[k] = i
                    k += 1
            print(dict_bonus)
            my_monstr = sessionStorage[user_id]['monster']
            for i in num:
                dict_bonus[int(i)].use_bonus('', sessionStorage[user_id])
                # удаляем бонус из руки
                for x in range(len(sessionStorage[user_id]['cards_on_hands'])):
                    if sessionStorage[user_id]['cards_on_hands'][x] == dict_bonus[int(i)]:
                        sessionStorage[user_id]['cards_on_hands'].pop(x)
                        break
            if sessionStorage[user_id]['monster'] is None:
                sessionStorage[user_id]['monster'] = my_monstr
                catch_bonus(user_id, res)  # будет картинка
                res['response']['card']['title'] = 'Вы его выйграли! ' + res['response']['card'][
                    'title']
                sessionStorage[user_id]["bonus_strength"] = 0
                sessionStorage[user_id]['monster'] = None
                sessionStorage[user_id]['epoch'] = '33'
            else:
                res['response'][
                    'text'] += f'Ваши бонусы приняты! Ваша сила: {sessionStorage[user_id]["overall_strength"] + sessionStorage[user_id]["level"] + sessionStorage[user_id]["bonus_strength"]}\nСила монстра: {sessionStorage[user_id]["monster"].level}\n'
                print(len([i for i in sessionStorage[user_id]['cards_on_hands'] if
                           i.__class__.__bases__[0].__name__ == 'BonusBase']))
                if len([i for i in sessionStorage[user_id]['cards_on_hands'] if
                        i.__class__.__bases__[0].__name__ == 'BonusBase']) != 0:
                    res['response']['text'] += 'Вы хотите положить еще бонусы?'
                    res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                                  {'title': 'Нет', 'hide': True}]
                    sessionStorage[user_id]['epoch'] = '25'
                else:
                    # проверка может быть он выигрывает!!!
                    if sessionStorage[user_id]["overall_strength"] + sessionStorage[user_id][
                        "level"] + \
                            sessionStorage[user_id]["bonus_strength"] > sessionStorage[user_id][
                        "monster"].level:
                        catch_bonus(user_id, res)  # будет картинка
                        res['response']['card']['title'] = 'Вы его выйграли! ' + \
                                                           res['response']['card'][
                                                               'title']
                        sessionStorage[user_id]["bonus_strength"] = 0
                        sessionStorage[user_id]['monster'] = None
                        sessionStorage[user_id]['epoch'] = '33'
                    else:
                        num = random.randint(1, 6)
                        res['response'][
                            'text'] = f'У вас нет бонусов, которые могут вам помочь, вам придётся убегать! Подбрасываю кубик иии вам выпало {num}.\n'
                        what, text = do_bad_things_with_hero(user_id, num)
                        if what == 1:  # смог убежать
                            res['response']['text'] += text
                            # условие больше 5 карт и начинаем от щедрот
                            res['response']['text'] += 'Вы готовы продолжать?'
                            sessionStorage[user_id]['epoch'] = '33'
                            res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                                          {'title': 'Нет', 'hide': True}]
                        elif what == 2:  # выжил
                            res['response']['text'] += text
                            res['response'][
                                'text'] += 'Вы выжили после этого!? Это удивительно!! Идем дальше! '
                            # условие больше 5 карт и начинаем от щедрот
                            res['response']['text'] += 'Вы готовы продолжать?'
                            sessionStorage[user_id]['epoch'] = '33'
                            res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                                          {'title': 'Нет', 'hide': True}]
                        else:  # Умер
                            res['response']['text'] += text
                            res['response'][
                                'text'] += 'Вы умерли - как жалко это признавать. Вы хотите играть дальше?'
                            res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                                          {'title': 'Нет', 'hide': True}]
                            sessionStorage[user_id]['epoch'] = '213'  # продаем карты
        elif sessionStorage[user_id]['epoch'] == '213':  # умер - продолжаем игру?
            if req['request']['original_utterance'].lower() in ['да']:
                # удаляем вещи
                del_all_things(user_id)
                res['response'][
                    'text'] = 'Вас оживил проходящий волшебник! Вы потеряли вещи но сохранили уровень!\n'
                # берем и удалем id
                ids_treasures = random.sample(sessionStorage[user_id]['what_treasures_stay'],
                                              4)  # берем id сокровищ
                ids_doors = random.sample(sessionStorage[user_id]['what_doors_stay'],
                                          4)  # берем id дверей
                # берем и удалем id
                if len(sessionStorage[user_id]['what_treasures_stay']) >= 4 and len(
                        sessionStorage[user_id]['what_doors_stay']) >= 4:
                    ids_treasures = random.sample(sessionStorage[user_id]['what_treasures_stay'],
                                                  4)  # берем id сокровищ
                    ids_doors = random.sample(sessionStorage[user_id]['what_doors_stay'],
                                              4)  # берем id дверей
                    sessionStorage[user_id]['cards_on_hands'] = [dict_treasures[i] for i in
                                                                 ids_treasures] + [
                                                                    dict_doors_for_hero[i]
                                                                    for i in ids_doors]
                    for i in ids_treasures:
                        sessionStorage[user_id]['what_treasures_stay'].remove(i)
                    for i in ids_doors:
                        sessionStorage[user_id]['what_doors_stay'].remove(i)
                else:
                    if len(sessionStorage[user_id]['what_treasures_stay']) < 4:
                        sessionStorage[user_id]['what_treasures_stay'] = list(
                            range(len(dict_treasures)))
                    if len(sessionStorage[user_id]['what_doors_stay']) < 4:
                        sessionStorage[user_id]['what_doors_stay'] = list(
                            range(len(dict_doors_for_hero)))
                    ids_treasures = random.sample(sessionStorage[user_id]['what_treasures_stay'],
                                                  4)  # берем id сокровищ
                    ids_doors = random.sample(sessionStorage[user_id]['what_doors_stay'],
                                              4)  # берем id дверей
                    sessionStorage[user_id]['cards_on_hands'] = [dict_treasures[i] for i in
                                                                 ids_treasures] + [
                                                                    dict_doors_for_hero[i]
                                                                    for i in ids_doors]
                    for i in ids_treasures:
                        sessionStorage[user_id]['what_treasures_stay'].remove(i)
                    for i in ids_doors:
                        sessionStorage[user_id]['what_doors_stay'].remove(i)
                # создаем 4 карты двери и сокровищ
                # treasures = [
                #     Armament(*dict_treasures[i][1:]) if dict_treasures[i][0] != 0 else Bonus(
                #         *dict_treasures[i][1:]) for i in ids_treasures]
                # doors = [Monster(*dict_doors_for_hero[i][1:]) if dict_doors_for_hero[i][0] != 0
                #          else Proklate(*dict_doors_for_hero[i][1:]) for i in ids_doors]
                # сортируем
                sessionStorage[user_id]['cards_on_hands'] = sort_cards(user_id)
                # даем ответ для алисы
                text = show_names(user_id)  # создаем текст для вывода всех предметов
                res['response']['text'] += '<---------\n'
                res['response']['text'] += text
                k, text = find_free_cards(user_id)  # какие карты можно положить?
                res['response']['text'] += text
                res['response']['text'] += '--------->\n'
                res['response']['text'] += 'Какие карты вы хотите положить на стол? (номера)'
                res['response']['buttons'] = [{'title': 'Никакие', 'hide': True}]
                sessionStorage[user_id]['epoch'] = '2'  # начинаем игру
            elif req['request']['original_utterance'].lower() in ['нет']:
                res['response']['text'] = 'Приходите когда будете готовы! До скорых встреч!'
                res['response']['end_session'] = True
            else:  # не поняли
                res['response']['text'] = 'Я вас не поняла, извините... Так да или нет?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                              {'title': 'Нет', 'hide': True}]
    elif sessionStorage[user_id]['epoch'][0] == '3':
        if sessionStorage[user_id]['epoch'] == '30':
            if req['request']['original_utterance'].lower() in ['да']:
                # смотрим есть ли монстр или нет
                if any([True for i in sessionStorage[user_id]['cards_on_hands'] if
                        i.__class__.__bases__[0].__name__ == 'MonsterBase']):
                    # есть монстр
                    res['response'][
                        'text'] = 'У вас есть монстры на руках!!! Хотите с ними сразиться?'
                    sessionStorage[user_id]['epoch'] = '31'
                    res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                                  {'title': 'Нет', 'hide': True}]
                else:
                    catch_door(user_id, res)
                    sessionStorage[user_id]['epoch'] = '33'

            elif req['request']['original_utterance'].lower() in ['нет']:
                res['response']['text'] = 'Вы хотите выйти из игры?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                              {'title': 'Нет', 'hide': True}]
                sessionStorage[user_id]['epoch'] = '301'  # доп правила
            else:  # не поняли
                res['response']['text'] = 'Я вас не поняла, извините... Так да или нет?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                              {'title': 'Нет', 'hide': True}]
        elif sessionStorage[user_id]['epoch'] == '301':
            if req['request']['original_utterance'].lower() in ['да']:
                res['response']['text'] = 'Приходите когда будете готовы! До скорых встреч!'
                res['response']['end_session'] = True
            elif req['request']['original_utterance'].lower() in ['нет']:
                # смотрим есть ли монстр или нет
                if any([True for i in sessionStorage[user_id]['cards_on_hands'] if
                        i.__class__.__bases__[0].__name__ == 'MonsterBase']):
                    # есть монстр
                    res['response'][
                        'text'] = 'У вас есть монстры на руках!!! Хотите с ними сразиться?'
                    res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                                  {'title': 'Нет', 'hide': True}]
                    sessionStorage[user_id]['epoch'] = '31'
                else:
                    res['response']['text'] = ''
                    catch_door(user_id, res)
                    sessionStorage[user_id]['epoch'] = '33'
            else:  # не поняли
                res['response']['text'] = 'Я вас не поняла, извините... Так вы хотите выйти?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                              {'title': 'Нет', 'hide': True}]
        elif sessionStorage[user_id]['epoch'] == '31':
            if req['request']['original_utterance'].lower() in ['да']:
                res['response']['text'] = ''
                choose_monster(user_id, res)
                res['response']['buttons'] = [{'title': 'Никакого', 'hide': True}]
                sessionStorage[user_id]['epoch'] = '32'
            elif req['request']['original_utterance'].lower() in ['нет']:
                res['response']['text'] = ''
                catch_door(user_id, res)  # чистим нычки
                sessionStorage[user_id]['epoch'] = '33'
                print('Мы тут')
                res['response']['end_session'] = False
            else:  # не поняли
                res['response']['text'] = 'Я вас не поняла, извините... Так да или нет?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                              {'title': 'Нет', 'hide': True}]
        elif sessionStorage[user_id]['epoch'] == '32':
            text_res = req['request']['original_utterance'].lower()
            if 'никакого' in text_res:  # ничего не хочет выкладывать
                res['response']['text'] = 'Вы отказались класть монстра!\n'
                catch_door(user_id, res)  # чистим нычки
                sessionStorage[user_id]['epoch'] = '33'
                return
            num = []
            for i in text_res.split():
                # просто удаляем знаки препинания
                word = ''
                for x in i:
                    if x not in marks:
                        word += x
                print(word)
                if word.isdigit():
                    num.append(word)
            # проверка
            if len(num) == 0:
                res['response'][
                    'text'] = 'В вашем ответе отсутствуют цифры! Введите цифру! Например 1.\n'
                choose_monster(user_id, res)
                res['response']['buttons'] = [{'title': 'Никакого', 'hide': True}]
                return
            if len(num) == 1:
                res['response'][
                    'text'] = f'Вы выбрали позицию: {num[0]};\n'
                n = int(num[0])
                kol = len([i for i in sessionStorage[user_id]['cards_on_hands'] if
                           i.__class__.__bases__[0].__name__ == 'MonsterBase'])
                if n <= 0 or n > kol:
                    res['response'][
                        'text'] = f'Ошибка! Пожалуйста, введите цифру в диапозоне от 1 до {kol}'
                else:
                    ind_mon = 0
                    for i in range(len(sessionStorage[user_id]['cards_on_hands'])):
                        if sessionStorage[user_id]['cards_on_hands'][
                            i].__class__.__bases__[0].__name__ == 'MonsterBase':
                            ind_mon += 1
                            if ind_mon == n:  # сражаемся с монсторм
                                monstr = sessionStorage[user_id]['cards_on_hands'][i]
                                sessionStorage[user_id]['cards_on_hands'].pop(i)  # удалили монстра
                                # картинка
                                res['response']['card'] = {}
                                res['response']['card']['type'] = 'BigImage'
                                res['response']['card']['image_id'] = random.choice(
                                    all_picturs['monster'])
                                res['response']['card']['description'] = ''
                                # текст
                                res['response']['text'] += f'Монстр: {monstr.title}.\n'
                                res['response']['card'][
                                    'description'] += f'Его level: {monstr.level}\n'
                                res['response']['card'][
                                    'description'] += f'Если вы победите, то получите:\n1) {monstr.count_gem} сокровищ\n2) +{monstr.count_level} level\n'
                                res['response']['card'][
                                    'description'] += f'Но если вы проиграете, то вас подействует непотребство:\n"{monstr.bad_things}"\n'
                                res['response'][
                                    'text'] += 'Вы готовы сражаться?'
                                # доб текст для карточки
                                res['response']['card']['title'] = res['response']['text']
                                # закрепляем монстра к герою
                                sessionStorage[user_id]['monster'] = monstr
                                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                                              {'title': 'Нет', 'hide': True}]
                                sessionStorage[user_id]['epoch'] = '20'
                                return
            else:
                res['response'][
                    'text'] = 'Вы ввели цифр больше чем одна! Введите одну цифру! Например 1.\n'
                choose_monster(user_id, res)
                res['response']['buttons'] = [{'title': 'Никакого', 'hide': True}]
        elif sessionStorage[user_id][
            'epoch'] == '33':  # готов продолжать + У пользователя больше 5 карт на руке?
            if req['request']['original_utterance'].lower() in ['да']:
                res['response']['text'] = 'Хорошо! Тогда продолжим!\n'
                # У пользователя больше 5 карт на руке?
                if sessionStorage[user_id]['level'] >= 10:
                    res['response'][
                        'text'] = f'У вас {sessionStorage[user_id]["level"]} уровень! Вы выиграли!!!\n'
                    res['response']['end_session'] = True
                else:
                    if len(sessionStorage[user_id]['cards_on_hands']) > 5:
                        res['response'][
                            'text'] += 'У вас больше 5 карт на руках. Вы хотите убрать карту со стола?'
                        res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                                      {'title': 'Нет', 'hide': True}]
                        sessionStorage[user_id]['epoch'] = '42'  # доп правила
                    else:
                        res['response'][
                            'text'] += 'Вы хотите убрать карту со стола?'
                        res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                                      {'title': 'Нет', 'hide': True}]
                        sessionStorage[user_id]['epoch'] = '42'  # доп правила
            elif req['request']['original_utterance'].lower() in ['нет']:  # выход из игры
                res['response']['text'] = 'Приходите когда будете готовы! До скорых встреч!'
                res['response']['end_session'] = True
            else:  # не поняли
                res['response']['text'] = 'Я вас не поняла, извините... Так да или нет?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                              {'title': 'Нет', 'hide': True}]
    elif sessionStorage[user_id]['epoch'][0] == '4':
        if sessionStorage[user_id]['epoch'] == '42':  # готов продолжать + новый цикл
            if req['request']['original_utterance'].lower() in ['да']:
                main_list = []
                for i in sessionStorage[user_id]['weapon']:
                    main_list.append([i.title, 'оружие'])
                try:
                    main_list.append([sessionStorage[user_id]['armor']['head'].title, 'шлем'])
                except:
                    pass
                try:
                    main_list.append([sessionStorage[user_id]['armor']['body'].title, 'броник'])
                except:
                    pass
                try:
                    main_list.append([sessionStorage[user_id]['armor']['leg'].title, 'ботинки'])
                except:
                    pass
                if sessionStorage[user_id]['class'] is not None:
                    dd = {1: 'Эльф', 2: 'Хафлинг', 3: 'Дварф'}
                    main_list.append([dd[sessionStorage[user_id]['class'].what], 'класс'])
                if len(main_list) != 0:
                    res['response']['text'] = f'Какие карты вы хотите убрать со стола в руки?\n'
                    for i in range(len(main_list)):
                        res['response'][
                            'text'] += f'{i + 1}. {main_list[i][0]} - {main_list[i][1]}\n'
                    sessionStorage[user_id]['epoch'] = '421'
                    res['response']['buttons'] = [{'title': 'Никакие', 'hide': True}]
                    return
                else:
                    res['response'][
                        'text'] = f'На вашем столе нет карт! У вас {len(sessionStorage[user_id]["cards_on_hands"])} карт на руке. Вы хотите положить карты на стол?'
                    res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                                  {'title': 'Нет', 'hide': True}]
                    sessionStorage[user_id]['epoch'] = '43'
            elif req['request']['original_utterance'].lower() in ['нет']:
                res['response'][
                    'text'] = f'У вас {len(sessionStorage[user_id]["cards_on_hands"])} карт. Вы хотите положить карты на стол?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                              {'title': 'Нет', 'hide': True}]
                sessionStorage[user_id]['epoch'] = '43'
            else:
                res['response']['text'] = 'Я вас не поняла, извините... Так да или нет?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                              {'title': 'Нет', 'hide': True}]
        elif sessionStorage[user_id]['epoch'] == '421':
            if req["request"]["original_utterance"].lower() in ['никакие']:
                res['response'][
                    'text'] = f'У вас {len(sessionStorage[user_id]["cards_on_hands"])} карт. Вы хотите положить карты на стол?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                              {'title': 'Нет', 'hide': True}]
                sessionStorage[user_id]['epoch'] = '43'
                print('Мы тут')
                return
            main_list = []
            for i in sessionStorage[user_id]['weapon']:
                main_list.append([i, 'weapon'])
            # снаряжение
            x1 = sessionStorage[user_id]['armor']['head']
            if x1 is not None:
                main_list.append([sessionStorage[user_id]['armor']['head'], 'head'])
            x2 = sessionStorage[user_id]['armor']['body']
            if x2 is not None:
                main_list.append([sessionStorage[user_id]['armor']['body'], 'body'])
            x3 = sessionStorage[user_id]['armor']['leg']
            if x3 is not None:
                main_list.append([sessionStorage[user_id]['armor']['leg'], 'leg'])
            if sessionStorage[user_id]['class'] is not None:
                main_list.append([sessionStorage[user_id]['class'].what, 'класс'])
            # проверка
            input_text = req["request"]["original_utterance"].lower()
            num = []
            for i in input_text.split():
                # просто удаляем знаки препинания
                word = ''
                for x in i:
                    if x not in marks:
                        word += x
                print(word)
                if word.isdigit():
                    num.append(word)
            if len(num) == 0:
                res['response'][
                    'text'] = 'В вашем ответе отсутствуют цифры! Введите цифры! Например 1, 2...\n'
                res['response']['text'] = f'Какие карты вы хотите убрать со стола в руки?\n'
                for i in range(len(main_list)):
                    res['response'][
                        'text'] += f'{i + 1}. {main_list[i][0].title} - {main_list[i][1]}\n'
                res['response']['buttons'] = [{'title': 'Никакие', 'hide': True}]
                return
            res['response'][
                'text'] = f'Вы выбрали позиции: {", ".join(num)}\n'
            for x in num:
                if int(x) <= 0 or int(x) > len(main_list):
                    res['response'][
                        'text'] += f"Ошибка! Вы должны говорить цифры в диапазоне от 1 до {len(main_list)}\n"
                    res['response']['text'] = f'Какие карты вы хотите убрать со стола в руки?\n'
                    for i in range(len(main_list)):
                        res['response'][
                            'text'] += f'{i + 1}. {main_list[i][0].title} - {main_list[i][1]}\n'
                    res['response']['buttons'] = [{'title': 'Никакие', 'hide': True}]
                    return
            ml = []
            words = [int(i) for i in num]
            for i in words:
                if main_list[int(i) - 1][1] == 'body':
                    sessionStorage[user_id]['overall_strength'] -= \
                        sessionStorage[user_id]['armor']['body'].bonus
                    sessionStorage[user_id]['armor']['body'] = None
                elif main_list[int(i) - 1][1] == 'head':
                    sessionStorage[user_id]['overall_strength'] -= \
                        sessionStorage[user_id]['armor']['head'].bonus
                    sessionStorage[user_id]['armor']['head'] = None
                elif main_list[int(i) - 1][1] == 'leg':
                    sessionStorage[user_id]['overall_strength'] -= \
                        sessionStorage[user_id]['armor']['leg'].bonus
                    sessionStorage[user_id]['armor']['leg'] = None
                elif main_list[int(i) - 1][1] == 'weapon':
                    sessionStorage[user_id]['overall_strength'] -= main_list[int(i) - 1][0].bonus
                    sessionStorage[user_id]['weapon'].remove(main_list[int(i) - 1][0])
                elif main_list[int(i) - 1][1] == 'класс':
                    if sessionStorage[user_id]['class'] == 1:
                        sessionStorage[user_id]['luck'] -= 1
                    elif sessionStorage[user_id]['class'] == 2:
                        pass
                    elif sessionStorage[user_id]['class'] == 3:
                        sessionStorage[user_id]['overall_strength'] -= 2
                    sessionStorage[user_id]['class'] = None
            for i in words:
                ml.append(main_list[int(i) - 1][0])
            for i in ml:
                sessionStorage[user_id]['cards_on_hands'].append(i)
            res['response']['text'] = f'Вы убрали со стола:\n'
            a = 1
            for i in ml:
                res['response']['text'] += f'{a}. {i.title} \n'
                a += 1
            res['response']['text'] += 'Вы хотите продолжить?\n'
            res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                          {'title': 'Нет', 'hide': True}]
            sessionStorage[user_id]['epoch'] = '422'
        elif sessionStorage[user_id]['epoch'] == '422':
            if req['request']['original_utterance'].lower() in ['нет']:
                res['response']['text'] = 'Приходите когда будете готовы! До скорых встреч!'
                res['response']['end_session'] = True
            elif req['request']['original_utterance'].lower() in ['да']:
                # res['response']['text'] = 'У вас осталось\n'
                # for i in range(len(sessionStorage[user_id]['cards_on_hands'])):
                #     res['response'][
                #         'text'] += f'{i + 1}. {sessionStorage[user_id]["cards_on_hands"][i].title}\n'
                res['response'][
                    'text'] = f'У вас {len(sessionStorage[user_id]["cards_on_hands"])} карт. Вы хотите положить карты на стол?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                              {'title': 'Нет', 'hide': True}]
                sessionStorage[user_id]['epoch'] = '43'
            else:
                res['response']['text'] = 'Я вас не поняла, извините... Так да или нет?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                              {'title': 'Нет', 'hide': True}]
        elif sessionStorage[user_id]['epoch'] == '43':
            if req['request']['original_utterance'].lower() in ['нет']:
                res['response']['text'] = 'Какие карты вы хотите скинуть или продать?\n'
                for i in range(len(sessionStorage[user_id]['cards_on_hands'])):
                    try:
                        res['response'][
                            'text'] += f'{i + 1}) {sessionStorage[user_id]["cards_on_hands"][i].title} ({sessionStorage[user_id]["cards_on_hands"][i].price} $)\n'
                    except:
                        res['response'][
                            'text'] += f'{i + 1}) {sessionStorage[user_id]["cards_on_hands"][i].title} (0 $)\n'
                sessionStorage[user_id]['epoch'] = '44'
                res['response']['buttons'] = [{'title': 'Никакие', 'hide': True}]
            elif req['request']['original_utterance'].lower() in ['да']:
                res['response']['text'] = ''
                show_not_all_cards(user_id, res)
                k, text = find_free_cards(user_id)  # какие карты можно положить?
                res['response']['text'] += '\n' + text
                res['response']['buttons'] = [{'title': 'Никакие', 'hide': True}]
                sessionStorage[user_id]['epoch'] = '431'
            else:
                res['response']['text'] = 'Я вас не поняла, извините... Так да или нет?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                              {'title': 'Нет', 'hide': True}]
        elif sessionStorage[user_id]['epoch'] == '44':
            gg = req['request']['original_utterance'].lower()
            if 'никакие' in gg:  # ничего не хочет продавать
                # проверка больше ли 5 карт
                if len(sessionStorage[user_id]['cards_on_hands']) >= 6:
                    res['response']['text'] = 'Карт на руках должно быть не больше 5\n'
                    res['response']['text'] += 'Какие карты вы хотите скинуть или продать?\n'
                    for i in range(len(sessionStorage[user_id]['cards_on_hands'])):
                        try:
                            res['response'][
                                'text'] += f'{i + 1}) {sessionStorage[user_id]["cards_on_hands"][i].title} ({sessionStorage[user_id]["cards_on_hands"][i].price} $)\n'
                        except:
                            res['response'][
                                'text'] += f'{i + 1}) {sessionStorage[user_id]["cards_on_hands"][i].title} (0 $)\n'
                    sessionStorage[user_id]['epoch'] = '44'
                    return
                else:
                    res['response'][
                        'text'] = 'Вы прошли круг, молодец! Вы остались живы!!! Давайте открывать еще двери! Вы готовы продолжать?'
                    res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                                  {'title': 'Нет', 'hide': True}]
                    sessionStorage[user_id]['epoch'] = '41'
                    return
            else:
                # проверка на правильность
                num = []

                for i in gg.split():
                    # просто удаляем знаки препинания
                    word = ''
                    for x in i:
                        if x not in marks:
                            word += x
                    print(word)
                    if word.isdigit():
                        num.append(word)
                # проверка
                if len(num) == 0:
                    res['response'][
                        'text'] = 'В вашем ответе отсутствуют цифры! Введите цифры! Например 1, 2...\n'
                    res['response']['text'] += 'Какие карты вы хотите скинуть или продать?\n'
                    for i in range(len(sessionStorage[user_id]['cards_on_hands'])):
                        try:
                            res['response'][
                                'text'] += f'{i + 1}) {sessionStorage[user_id]["cards_on_hands"][i].title} ({sessionStorage[user_id]["cards_on_hands"][i].price} $)\n'
                        except:
                            res['response'][
                                'text'] += f'{i + 1}) {sessionStorage[user_id]["cards_on_hands"][i].title} (0 $)\n'
                    sessionStorage[user_id]['epoch'] = '44'
                    res['response']['buttons'] = [{'title': 'Никакие', 'hide': True}]
                    return
                res['response'][
                    'text'] = f'Вы выбрали позиции: {", ".join(num)}\n'
                for x in num:
                    if int(x) <= 0 or int(x) > len(sessionStorage[user_id]['cards_on_hands']):
                        res['response'][
                            'text'] += f'Ошибка! Вы должны говорить цифры в диапазоне от 1 до {len(sessionStorage[user_id]["cards_on_hands"])}\n'
                        res['response']['text'] += 'Какие карты вы хотите скинуть или продать?\n'
                        for i in range(len(sessionStorage[user_id]['cards_on_hands'])):
                            try:
                                res['response'][
                                    'text'] += f'{i + 1}) {sessionStorage[user_id]["cards_on_hands"][i].title} ({sessionStorage[user_id]["cards_on_hands"][i].price} $)\n'
                            except:
                                res['response'][
                                    'text'] += f'{i + 1}) {sessionStorage[user_id]["cards_on_hands"][i].title} (0 $)\n'
                        sessionStorage[user_id]['epoch'] = '44'
                        res['response']['buttons'] = [{'title': 'Никакие', 'hide': True}]
                        return
                sessionStorage[user_id]['cards_to_sell'] = [int(i) for i in num]
                res['response']['text'] = 'Вы действительно хотите продать эти карты?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                              {'title': 'Нет', 'hide': True}]
            sessionStorage[user_id]['epoch'] = '45'
        elif sessionStorage[user_id]['epoch'] == '45':
            if req['request']['original_utterance'].lower() in ['да']:
                main_list = []
                for i in sessionStorage[user_id]['weapon']:
                    main_list.append([i, 'weapon'])
                try:
                    main_list.append([sessionStorage[user_id]['armor']['head'], 'head'])
                except:
                    pass
                try:
                    main_list.append([sessionStorage[user_id]['armor']['body'], 'body'])
                except:
                    pass
                try:
                    main_list.append([sessionStorage[user_id]['armor']['leg'], 'leg'])
                except:
                    pass
                count_choose = 0
                if sessionStorage[user_id]['cards_to_sell'] is None:
                    count_choose = 0
                else:
                    count_choose = len(sessionStorage[user_id]['cards_to_sell'])
                if len(sessionStorage[user_id]['cards_on_hands']) - count_choose >= 6:
                    res['response']['text'] = 'Карт на руках должно быть не больше 5\n'
                    res['response']['text'] += 'Какие карты вы хотите скинуть или продать?\n'
                    for i in range(len(sessionStorage[user_id]['cards_on_hands'])):
                        try:
                            res['response'][
                                'text'] += f'{i + 1}) {sessionStorage[user_id]["cards_on_hands"][i].title} ({sessionStorage[user_id]["cards_on_hands"][i].price} $)\n'
                        except:
                            res['response'][
                                'text'] += f'{i + 1}) {sessionStorage[user_id]["cards_on_hands"][i].title} (0 $)\n'
                    sessionStorage[user_id]['epoch'] = '44'
                else:
                    try:
                        ml = []
                        kl = []
                        count = 0
                        for i in sessionStorage[user_id]['cards_to_sell']:
                            ml.append(sessionStorage[user_id]['cards_on_hands'][int(i) - 1])
                        for i in ml:
                            if i.__class__.__bases__[0].__name__ == 'MonsterBase':
                                sessionStorage[user_id]['cards_on_hands'].remove(i)
                                continue
                            count += int(i.price)
                            sessionStorage[user_id]['cards_on_hands'].remove(i)
                        res['response']['text'] = f'Вы получили за них: {count} монет\n'
                        level = count // 1000
                        print(sessionStorage[user_id]['level'])
                        sessionStorage[user_id]['level'] += level
                        print(sessionStorage[user_id]['level'])
                        ost = count % 1000
                        sessionStorage[user_id]["money"] += ost
                        res['response'][
                            'text'] += f'У вас {sessionStorage[user_id]["money"]} монет\n'
                        res['response']['text'] += f'+{level} level\n'
                        res['response']['text'] += f'У вас остались карты:\n'
                        a = 1
                        for i in sessionStorage[user_id]['cards_on_hands']:
                            res['response']['text'] += f'{a}. {i.title} \n'
                            a += 1
                        if sessionStorage[user_id]['level'] >= 10:
                            res['response'][
                                'text'] += f'У вас {sessionStorage[user_id]["level"]} уровень! Вы выиграли!!!\n'
                            res['response']['end_session'] = True
                        else:
                            res['response'][
                                'text'] += 'Вы прошли круг, молодец! Вы остались живы!!! Давайте открывать еще двери! Вы готовы продолжать?'
                            res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                                          {'title': 'Нет', 'hide': True}]
                            sessionStorage[user_id]['epoch'] = '41'  # доп правила
                    except:
                        res['response']['text'] = 'Ошибка! Давайте заного'
                        sessionStorage[user_id]['epoch'] = '43'
            elif req['request']['original_utterance'].lower() in ['нет']:
                gg = req['request']['original_utterance'].lower()
                res['response']['text'] = 'Какие карты вы хотите скинуть или продать?\n'
                for i in range(len(sessionStorage[user_id]['cards_on_hands'])):
                    try:
                        res['response'][
                            'text'] += f'{i + 1}) {sessionStorage[user_id]["cards_on_hands"][i].title} ({sessionStorage[user_id]["cards_on_hands"][i].price} $)\n'
                    except:
                        res['response'][
                            'text'] += f'{i + 1}) {sessionStorage[user_id]["cards_on_hands"][i].title} (0 $)\n'
                sessionStorage[user_id]['epoch'] = '44'
                res['response']['buttons'] = [{'title': 'Никакие', 'hide': True}]
        elif sessionStorage[user_id]['epoch'] == '431':
            text_res = req['request']['original_utterance'].lower()
            if 'никакие' in text_res:  # ничего не хочет выкладывать
                res['response']['text'] = 'Вы отказались класть карты!\n'
                res['response']['text'] = 'Какие карты вы хотите скинуть или продать?\n'
                for i in range(len(sessionStorage[user_id]['cards_on_hands'])):
                    try:
                        res['response'][
                            'text'] += f'{i + 1}) {sessionStorage[user_id]["cards_on_hands"][i].title} ({sessionStorage[user_id]["cards_on_hands"][i].price} $)\n'
                    except:
                        res['response'][
                            'text'] += f'{i + 1}) {sessionStorage[user_id]["cards_on_hands"][i].title} (0 $)\n'
                res['response']['buttons'] = [{'title': 'Никакие', 'hide': True}]
                sessionStorage[user_id]['epoch'] = '44'
                return
            else:
                # проверка на правильность
                num = []

                for i in text_res.split():
                    # просто удаляем знаки препинания
                    word = ''
                    for x in i:
                        if x not in marks:
                            word += x
                    print(word)
                    if word.isdigit():
                        num.append(word)
                # проверка
                if len(num) == 0:
                    res['response'][
                        'text'] = 'В вашем ответе отсутствуют цифры! Введите цифры! Например 1, 2...\n'
                    show_not_all_cards(user_id, res)
                    res['response']['buttons'] = [{'title': 'Никакие', 'hide': True}]
                    return
                res['response'][
                    'text'] = f'Вы выбрали позиции: {", ".join(num)}\n'
                for x in num:
                    if int(x) <= 0 or int(x) > len(sessionStorage[user_id]['cards_on_hands']):
                        res['response'][
                            'text'] += f'Ошибка! Вы должны говорить цифры в диапазоне от 1 до {len(sessionStorage[user_id]["cards_on_hands"])}\n'
                        show_not_all_cards(user_id, res)
                        res['response']['buttons'] = [{'title': 'Никакие', 'hide': True}]
                        return
                t, cards = is_all_right(user_id, [int(i) - 1 for i in
                                                  num])  # t - без ошибок? cards - текст функции
                if t:
                    res['response']['text'] += 'Ваши действия применились!\n'
                    res['response']['text'] += 'Какие карты вы хотите скинуть или продать?\n'
                    for i in range(len(sessionStorage[user_id]['cards_on_hands'])):
                        try:
                            res['response'][
                                'text'] += f'{i + 1}) {sessionStorage[user_id]["cards_on_hands"][i].title} ({sessionStorage[user_id]["cards_on_hands"][i].price} $)\n'
                        except:
                            res['response'][
                                'text'] += f'{i + 1}) {sessionStorage[user_id]["cards_on_hands"][i].title} (0 $)\n'
                    res['response']['buttons'] = [{'title': 'Никакие', 'hide': True}]
                    sessionStorage[user_id]['epoch'] = '44'
                    return
                else:
                    res['response']['text'] += 'Ошибка!\n' + cards
                    show_not_all_cards(user_id, res)
                    res['response']['buttons'] = [{'title': 'Никакие', 'hide': True}]
                    return
        elif sessionStorage[user_id]['epoch'] == '41':
            if req['request']['original_utterance'].lower() in ['нет']:
                res['response']['text'] = 'Приходите когда будете готовы! До скорых встреч!'
                res['response']['end_session'] = True
            elif req['request']['original_utterance'].lower() in ['да']:
                sessionStorage[user_id]['cards_to_sell'] = None
                sessionStorage[user_id]['bonus_strength'] = 0
                sessionStorage[user_id]['cards_on_hands'] = sort_cards(user_id)
                res['response']['text'] = ''
                if sessionStorage[user_id]['class'] is not None:
                    if sessionStorage[user_id]['class'].what == 2:
                        res['response'][
                            'text'] += 'Из-за того что вы хафлинг, вы получаете +1 уровень!\n'
                        sessionStorage[user_id]['level'] += 1
                        if sessionStorage[user_id]['level'] >= 10:
                            res['response'][
                                'text'] += f'У вас {sessionStorage[user_id]["level"]} уровень! Вы выиграли!!!\n'
                            res['response']['end_session'] = True
                # даем ответ для алисы
                text = show_names(user_id)  # создаем текст для вывода всех предметов
                res['response']['text'] += 'Вы идете дальше!\n'
                res['response']['text'] += '<---------\n'
                res['response']['text'] += text
                k, text = find_free_cards(user_id)  # какие карты можно положить?
                res['response']['text'] += text
                res['response']['text'] += '--------->\n'
                res['response']['text'] += 'Какие карты вы хотите положить на стол? (номера)'
                res['response']['buttons'] = [{'title': 'Никакие', 'hide': True}]
                sessionStorage[user_id]['epoch'] = '2'  # начинаем игру
            else:
                res['response']['text'] = 'Я вас не поняла, извините... Так да или нет?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                              {'title': 'Нет', 'hide': True}]


def choose_monster(user_id, res):
    res['response']['text'] += 'Какого монстра вы хотите сразить?\n'
    monsters = [i for i in sessionStorage[user_id]['cards_on_hands'] if
                i.__class__.__bases__[0].__name__ == 'MonsterBase']
    for i in range(len(monsters)):
        res['response'][
            'text'] += f'{i + 1}) {monsters[i].title}; Сила: {monsters[i].level}; {monsters[i].count_gem} сокровищ(е);\n'
    res['response']['text'] += 'Напишите номер:'


def catch_door(user_id, res):
    res['response']['card'] = {}
    res['response']['card']['type'] = 'BigImage'
    res['response']['card']['title'] = 'Вы готовы продолжать?'
    res['response']['card']['description'] = 'Чистим нычки! Берем карту с дверью, и вам выпадает: '
    # делаем
    if len(sessionStorage[user_id]['what_doors_stay']) >= 1:
        ids = random.sample(sessionStorage[user_id]['what_doors_stay'], 1)
        for i in ids:
            sessionStorage[user_id]['what_doors_stay'].remove(i)
    else:
        sessionStorage[user_id]['what_doors_stay'] = list(
            range(len(dict_doors_for_hero)))
        ids = random.sample(sessionStorage[user_id]['what_doors_stay'], 1)
        for i in ids:
            sessionStorage[user_id]['what_doors_stay'].remove(i)
    ids_doors = ids[0]
    # удаляем id
    print('id двери: ', ids_doors)
    if dict_doors_for_hero[ids_doors].__class__.__bases__[0].__name__ == 'RaceBase':  # раса
        res['response']['card']['description'] += f'Раса: {dict_doors_for_hero[ids_doors].title}. '
        res['response']['card']['image_id'] = random.choice(all_picturs['эльф'])
        sessionStorage[user_id]['cards_on_hands'].append(None)
    else:  # монстр
        res['response']['card']['description'] += f'Монстр: {dict_doors_for_hero[ids_doors].title}. '
        res['response']['card']['image_id'] = random.choice(all_picturs['monster'])
        sessionStorage[user_id]['cards_on_hands'].append(dict_doors_for_hero[ids_doors])
    res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                  {'title': 'Нет', 'hide': True}]


def del_all_things(user_id):
    sessionStorage[user_id]['weapon'] = []
    if sessionStorage[user_id]['class'] is not None:
        if sessionStorage[user_id]['class'].what == 1:
            sessionStorage[user_id]['luck'] -= 1
        elif sessionStorage[user_id]['class'].what == 2:
            pass
        elif sessionStorage[user_id]['class'].what == 3:
            sessionStorage[user_id]['overall_strength'] -= 2
    sessionStorage[user_id]['class'] = None
    sessionStorage[user_id]['monster'] = None
    sessionStorage[user_id]['bonus_strength'] = None
    sessionStorage[user_id]['money'] = 0
    sessionStorage[user_id]['luck'] = 2
    sessionStorage[user_id]['armor'] = {'head': None, 'body': None, 'leg': None}
    sessionStorage[user_id]['cards_on_hands'] = []
    sessionStorage[user_id]['is_alive'] = True


def do_bad_things_with_hero(user_id, num):
    text = ''
    if sessionStorage[user_id]['luck'] >= num:  # смог убежать
        text += 'Вы смогли убежать!!! Какой вы удачливый!\n'
        return 1, text
    else:
        monster = sessionStorage[user_id]['monster']
        text += 'Вы не смогли убежать:( На вас подействовало непотребство:\n'
        text += monster.bad_things + '\n'
        monster.do_bad_things('', sessionStorage[user_id])
        sessionStorage[user_id]['monster'] = None
        if not sessionStorage[user_id]['is_alive']:  # чел умер
            return 3, text
        else:
            return 2, text


def choose_bonus(user_id):
    all_bonuses = [i for i in sessionStorage[user_id]['cards_on_hands'] if
                   i.__class__.__bases__[0].__name__ == 'BonusBase']
    text = 'Ваши бонусы:\n'
    for i in range(len(all_bonuses)):
        text += f'{i + 1}) {all_bonuses[i].title} ({all_bonuses[i].mini_text})\n'
    return text


def catch_bonus(user_id, res):  # текст для вывода награды
    text = ''
    if len(sessionStorage[user_id]['what_treasures_stay']) >= sessionStorage[user_id][
        'monster'].count_gem:
        ids = random.sample(sessionStorage[user_id]['what_treasures_stay'],
                            sessionStorage[user_id]['monster'].count_gem)
        for i in ids:
            sessionStorage[user_id]['what_treasures_stay'].remove(i)
    else:
        sessionStorage[user_id]['what_treasures_stay'] = list(
            range(len(dict_treasures)))
        ids = random.sample(sessionStorage[user_id]['what_treasures_stay'],
                            sessionStorage[user_id]['monster'].count_gem)
        for i in ids:
            sessionStorage[user_id]['what_treasures_stay'].remove(i)
    kol = 1
    text += f'{kol}) + {sessionStorage[user_id]["monster"].count_level} level\n'
    kol += 1
    sessionStorage[user_id]['level'] += sessionStorage[user_id]['monster'].count_level
    what_picture = set()
    for i in ids:
        # удаляем id
        bonus = dict_treasures[i]
        if bonus.__class__.__bases__[0].__name__ == 'BonusBase':  # получи уровень ...
            text += f'{kol}) Название: {bonus.title}; Стоимость: {bonus.price}\n'
            what_picture.add('bonus')
            sessionStorage[user_id]['cards_on_hands'].append(bonus)
        else:  # одежда
            clothes = bonus
            text += f'{kol}) Название: {clothes.title}; Стоимость: {clothes.price}\n'
            if clothes.what == 1:
                what_picture.add('weapon')
            elif clothes.what == 2:
                what_picture.add('head')
            elif clothes.what == 3:
                what_picture.add('body')
            elif clothes.what == 4:
                what_picture.add('leg')
            sessionStorage[user_id]['cards_on_hands'].append(clothes)
        kol += 1
    # картинка
    res['response']['card'] = {}
    res['response']['card']['type'] = 'BigImage'
    res['response']['card']['image_id'] = random.choice(
        all_picturs[random.choice(list(what_picture))])
    res['response']['card']['title'] = 'Вы готовы продолжать?'
    res['response']['card']['description'] = text
    res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                  {'title': 'Нет', 'hide': True}]


def pull_out_card_door(user_id, res):  # Вытягиваем карту двери
    what_bring = random.randint(1, 10)
    if what_bring == 10:  # проклятье
        prokl = random.choice(proklates_cards)
        # картинка
        res['response']['card'] = {}
        res['response']['card']['type'] = 'BigImage'
        res['response']['card']['image_id'] = random.choice(all_picturs['proklate'])
        res['response']['card']['title'] = ''
        res['response']['card']['description'] = ''
        # другое
        res['response']['text'] += f'Вам выпало проклятье: {prokl.title}\n'
        res['response']['text'] += f'Но вы остались живи и продолжаете путешествовать!\n'
        # применяем проклятье
        prokl.use_bad_things('', sessionStorage[user_id])
        # доб текст
        res['response']['card']['description'] = res['response']['text']
        return 3
    else:
        if len(sessionStorage[user_id]['what_doors_stay']) >= 1:
            ids = random.sample(sessionStorage[user_id]['what_doors_stay'], 1)
            for i in ids:
                sessionStorage[user_id]['what_doors_stay'].remove(i)
        else:
            sessionStorage[user_id]['what_doors_stay'] = list(
                range(len(dict_doors_for_hero)))
            ids = random.sample(sessionStorage[user_id]['what_doors_stay'], 1)
            for i in ids:
                sessionStorage[user_id]['what_doors_stay'].remove(i)
        id = ids[0]

        smth = dict_doors_for_hero[id]
        if smth.__class__.__bases__[0].__name__ == 'RaceBase':  # раса
            # картинка
            res['response']['card'] = {}
            res['response']['card']['type'] = 'BigImage'
            res['response']['card']['title'] = ''
            res['response']['card']['description'] = ''
            res['response']['card']['description'] = f'Вам выпала новая раса: '
            if smth.what == 1:  # эльф
                res['response']['card']['description'] += 'Эльф\n'
                res['response']['card']['description'] += smth.title + '\n'
                res['response']['card']['image_id'] = all_picturs['эльф']
                sessionStorage[user_id]['cards_on_hands'].append(smth)
            elif smth.what == 2:  # хафлинг
                res['response']['card']['description'] += 'Хафлинг\n'
                res['response']['card']['description'] += smth.title + '\n'
                res['response']['card']['image_id'] = all_picturs['хафлинг']
                sessionStorage[user_id]['cards_on_hands'].append(smth)
            elif smth.what == 3:  # дварф
                res['response']['card']['description'] += 'Дварф\n'
                res['response']['card']['description'] += smth.title + '\n'
                res['response']['card']['image_id'] = all_picturs['дварф']
                sessionStorage[user_id]['cards_on_hands'].append(smth)
            return 4
        else:  # монстр
            monstr = smth
            # картинка
            res['response']['card'] = {}
            res['response']['card']['type'] = 'BigImage'
            res['response']['card']['image_id'] = random.choice(all_picturs['monster'])
            res['response']['card']['description'] = ''
            # текст
            res['response']['text'] += f'Вам выпал: {monstr.title}.\n'
            res['response']['card']['description'] += f'Его level: {monstr.level}\n'
            res['response']['card'][
                'description'] += f'Если вы победите, то получите:\n1) {monstr.count_gem} сокровищ\n2) +{monstr.count_level} level\n'
            res['response']['card'][
                'description'] += f'Но если вы проиграете, то вас подействует непотребство:\n"{monstr.bad_things}"\n'
            res['response'][
                'text'] += 'Вы готовы сражаться?'
            # доб текст для карточки
            res['response']['card']['title'] = res['response']['text']
            # закрепляем монстра к герою
            sessionStorage[user_id]['monster'] = monstr
            res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                          {'title': 'Нет', 'hide': True}]
            return 1


def fight_with_monster(user_id, res):
    monstr = sessionStorage[user_id]['monster']
    if monstr.level < sessionStorage[user_id]['overall_strength'] + sessionStorage[user_id][
        'level']:
        res['response'][
            'text'] = 'Вы сразились с ним и победили его в честном бою! Поздравляем! Вы можете тянуть награду!\n'
        return 1
    else:
        res['response'][
            'text'] = 'У вас не хватает силы, чтобы победить его! Вы хотите использовать бонусы?\n'
        res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                      {'title': 'Нет', 'hide': True}]
        sessionStorage[user_id]['epoch'] = '25'
        return 2


def is_all_right(user_id, nums):  # проверяем на правильность выбора карт
    cards_choose = {'Bonus': [], 'Race': [], 'head': [], 'body': [], 'leg': [], 'weapon': []}
    #  Monster, Bonus, Armament, Proklate, Race
    # записываем в словарь
    for i in nums:
        card = sessionStorage[user_id]['cards_on_hands'][i]
        if card.__class__.__bases__[0].__name__ == 'ArmamentBase':
            if card.what == 1:
                cards_choose['weapon'].append(card)
            if card.what == 2:
                cards_choose['head'].append(card)
            if card.what == 3:
                cards_choose['body'].append(card)
            if card.what == 4:
                cards_choose['leg'].append(card)
        elif card.__class__.__bases__[0].__name__ == 'MonsterBase':
            return False, 'Вы выбрали монстра!\nЕго нельзя одеть на себя или еще лучше применить как бонус!\n'
        elif card.__class__.__bases__[0].__name__ == 'ProklateBase':
            return False, 'Вы выбрали проклятье!\nЕго нельзя одеть на себя или еще лучше применить как бонус!\n'
        elif card.__class__.__bases__[0].__name__ == 'BonusBase':
            if card.price != 1000:
                return False, f'Вы выбрали бонус "{card.title}",но его не как нельзя применить!'
            else:
                cards_choose['Bonus'].append(card)
        elif card.__class__.__bases__[0].__name__ == 'RaceBase':
            cards_choose['Race'].append(card)
        elif card.__class__.__bases__[0].__name__ == 'BonusBase':
            cards_choose['Bonus'].append(card)
    # предметы
    kol_head = 0
    kol_body = 0

    if len(cards_choose['head']) > 1:
        return False, f'Вы выбрали {len(cards_choose["head"])} шлемов! Куда вам столько?'
    if len(cards_choose['body']) > 1:
        return False, f'Вы выбрали {len(cards_choose["body"])} брони! Куда вам столько?'
    if len(cards_choose['leg']) > 1:
        return False, f'Вы выбрали {len(cards_choose["body"])} поножь! Куда вам столько?'
    if len(cards_choose['weapon']) > 2:
        return False, f'Вы выбрали {len(cards_choose["weapon"])} оружия! Куда вам столько?'
    if len(cards_choose['Race']) > 1:
        return False, f'Вы выбрали {len(cards_choose["Race"])} рас! Куда вам столько?'
    # оружие
    elif len(cards_choose['weapon']) == 2:
        # if cards_choose['weapon'][0].if_weapon_hand == 1 and cards_choose['weapon'][
        #     1].if_weapon_hand == 1 and len(sessionStorage[user_id]['weapon']) == 0:
        #     pass
        # else:
        #     return False, f'Вы выбрали {len(cards_choose["weapon"])} оружия! Превышен лимит оружия на руках'
        if len(sessionStorage[user_id]['weapon']) == 0:
            pass
        else:
            return False, f'Вы выбрали {len(cards_choose["weapon"])} оружия! Превышен лимит оружия на руках'
    elif len(cards_choose['weapon']) == 1:
        # if cards_choose['weapon'][0].if_weapon_hand == 1:
        #     if len(sessionStorage[user_id]['weapon']) == 0:
        #         pass
        #     elif len(sessionStorage[user_id]['weapon']) == 1:
        #         if sessionStorage[user_id]['weapon'][0].if_weapon_hand == 1:
        #             pass
        #         else:
        #             return False, f'Вы выбрали {len(cards_choose["weapon"])} оружия! Превышен лимит оружия на руках'
        #     else:
        #         return False, f'Вы выбрали {len(cards_choose["weapon"])} оружия! Превышен лимит оружия на руках'
        # else:
        #     if len(sessionStorage[user_id]['weapon']) == 0:
        #         pass
        #     else:
        #         return False, f'Вы выбрали {len(cards_choose["weapon"])} оружия! Превышен лимит оружия на руках'
        if len(sessionStorage[user_id]['weapon']) != 2:
            pass
        else:
            return False, f'Вы выбрали {len(cards_choose["weapon"])} оружия! Превышен лимит оружия на руках'

    # засовываем все в героя!
    print(cards_choose)
    all_names_cards = '---------\n'
    if len(cards_choose['head']) != 0:
        if sessionStorage[user_id]['armor']['head'] is None:
            sessionStorage[user_id]['overall_strength'] += cards_choose['head'][0].bonus
        else:
            sessionStorage[user_id]['overall_strength'] -= sessionStorage[user_id]['armor'][
                'head'].bonus
            sessionStorage[user_id]['overall_strength'] += cards_choose['head'][0].bonus
        sessionStorage[user_id]['armor']['head'] = cards_choose['head'][0]
        all_names_cards += f"{cards_choose['head'][0].title}\n"
    if len(cards_choose['body']) != 0:
        if sessionStorage[user_id]['armor']['body'] is None:
            sessionStorage[user_id]['overall_strength'] += cards_choose['body'][0].bonus
        else:
            sessionStorage[user_id]['overall_strength'] -= sessionStorage[user_id]['armor'][
                'body'].bonus
            sessionStorage[user_id]['overall_strength'] += cards_choose['body'][0].bonus
        sessionStorage[user_id]['armor']['body'] = cards_choose['body'][0]
        all_names_cards += f"{cards_choose['body'][0].title}\n"
    if len(cards_choose['leg']) != 0:
        if sessionStorage[user_id]['armor']['leg'] is None:
            sessionStorage[user_id]['overall_strength'] += cards_choose['leg'][0].bonus
        else:
            sessionStorage[user_id]['overall_strength'] -= sessionStorage[user_id]['armor'][
                'leg'].bonus
            sessionStorage[user_id]['overall_strength'] += cards_choose['leg'][0].bonus
        sessionStorage[user_id]['armor']['leg'] = cards_choose['leg'][0]
        all_names_cards += f"{cards_choose['leg'][0].title}\n"
    if len(cards_choose['weapon']) != 0:
        sessionStorage[user_id]['weapon'] = cards_choose['weapon']
        if len(cards_choose['weapon']) == 1:
            all_names_cards += f"{cards_choose['weapon'][0].title}\n"
            sessionStorage[user_id]['overall_strength'] += cards_choose['weapon'][0].bonus
        else:
            all_names_cards += f"{cards_choose['weapon'][0].title}\n"
            all_names_cards += f"{cards_choose['weapon'][1].title}\n"
            sessionStorage[user_id]['overall_strength'] += cards_choose['weapon'][0].bonus
            sessionStorage[user_id]['overall_strength'] += cards_choose['weapon'][1].bonus
    if len(cards_choose['Race']) != 0:
        sessionStorage[user_id]['class'] = cards_choose['Race'][0]
        dd = {1: 'Эльф', 2: 'Хафлинг', 3: 'Дварф'}
        all_names_cards += f"{dd[cards_choose['Race'][0].what]}\n"
        if cards_choose['Race'][0].what == 1:
            sessionStorage[user_id]['luck'] += 1
        elif cards_choose['Race'][0].what == 2:
            pass
        elif cards_choose['Race'][0].what == 2:
            sessionStorage[user_id]['overall_strength'] += 2
        sessionStorage[user_id]['class'] = cards_choose['Race'][0]
    if len(cards_choose['Bonus']) != 0:
        sessionStorage[user_id]['level'] += len(cards_choose['Bonus'])
        all_names_cards += f"{cards_choose['Bonus'][0].title} * {len(cards_choose['Bonus'])}\n"
    all_names_cards += '---------\n'
    # удаляем карточки, которые использовали
    for i in range(len(nums)):
        sessionStorage[user_id]['cards_on_hands'].pop(nums[i] - i)
    print(sessionStorage[user_id]['cards_on_hands'])
    return True, all_names_cards + 'Ваши действия применились для героя! Он стал сильнее!!!\n'


def find_free_cards(user_id):  # передаю num от 1 - бес
    list_obj = sessionStorage[user_id]['cards_on_hands']
    d = {'class': [], 'head': [], 'body': [], 'leg': [], 'bonus': [], 'weapon': []}
    for i in range(len(list_obj)):
        if list_obj[i].__class__.__bases__[0].__name__ == 'BonusBase':
            if list_obj[i].price == 1000:
                d['bonus'].append(str(i + 1))
        if list_obj[i].__class__.__bases__[0].__name__ == 'RaceBase':
            if sessionStorage[user_id]['class'] is not None:
                d['class'].append(str(i + 1))
        if list_obj[i].__class__.__bases__[0].__name__ == 'ArmamentBase':
            if list_obj[i].what == 1:
                if len(sessionStorage[user_id]['weapon']) != 2:
                    d['weapon'].append(str(i + 1))
            if list_obj[i].what == 2:
                if sessionStorage[user_id]['armor']['head'] is None:
                    d['head'].append(str(i + 1))
            if list_obj[i].what == 3:
                if sessionStorage[user_id]['armor']['body'] is None:
                    d['body'].append(str(i + 1))
            if list_obj[i].what == 4:
                if sessionStorage[user_id]['armor']['leg'] is None:
                    d['leg'].append(str(i + 1))
    text = 'Вы можете положить:\n'
    kol = 0
    for k, v in d.items():
        if k == 'class' and len(d['class']) != 0:
            text += f'Раса: {", ".join(sorted(v))}\n'
            kol += 1
        if k == 'weapon' and len(d['weapon']) != 0:
            text += f'Оружие: {", ".join(sorted(v))}\n'
            kol += 1
        if k == 'head' and len(d['head']) != 0:
            text += f'Головняк: {", ".join(sorted(v))}\n'
            kol += 1
        if k == 'body' and len(d['body']) != 0:
            text += f'Броник: {", ".join(sorted(v))}\n'
            kol += 1
        if k == 'leg' and len(d['leg']) != 0:
            text += f'Поножи: {", ".join(sorted(v))}\n'
            kol += 1
        if k == 'bonus' and len(d['bonus']) != 0:
            text += f'Получи уровень: {", ".join(sorted(v))}\n'
            kol += 1
    if kol == 0:
        text = 'Вы можете положить: -\n'
    return kol, text


def sort_cards(user_id):  # сортировка карт в руке
    list_obj = sessionStorage[user_id]['cards_on_hands']
    s = []
    for i in list_obj:
        s.append([i.__class__.__bases__[0].__name__, i])
    res = [i[1] for i in sorted(s, key=lambda x: x[0])]
    return res


def show_names(user_id):  # показ амундирования
    dd = {1: 'Эльф', 2: 'Хафлинг', 3: 'Дварф'}
    armor = sessionStorage[user_id]['armor']
    weapon = sessionStorage[user_id]['weapon']
    class_human = sessionStorage[user_id]['class']
    list_obj = sessionStorage[user_id]['cards_on_hands']
    text = ''
    text += f'Ваш level: {sessionStorage[user_id]["level"]}\n'
    text += f'Ваша сила: {sessionStorage[user_id]["overall_strength"] + sessionStorage[user_id]["level"]}\n'
    if weapon != []:  # оружие
        if len(weapon) == 1 or weapon[0].title == weapon[1].title:
            text += f'Ваше оружие:\n1) {weapon[0].title} (+{weapon[0].bonus} к силе)\n'
        else:
            text += f'Ваше оружие:\n1) {weapon[0].title} (+{weapon[0].bonus} к силе) \n2) {weapon[1].title} (+{weapon[1].bonus} к силе)\n'
    else:
        text += f'Ваше оружие: -\n'
    text += 'На вас одет: \n'
    print(armor)
    for k, v in armor.items():  # 'head': None, 'body': None, 'leg': None
        if k == 'head':
            if armor[k] is not None:
                text += f'Головняк: {v.title} (+{v.bonus} к силе) \n'
            else:
                text += f'Головняк: - \n'
        if k == 'body':
            if armor[k] is not None:
                text += f'Броник: {v.title} (+{v.bonus} к силе) \n'
            else:
                text += f'Броник: - \n'
        if k == 'leg':
            if armor[k] is not None:
                text += f'Поножи: {v.title} (+{v.bonus} к силе) \n'
            else:
                text += f'Поножи: - \n'
    if class_human is not None:
        text += f'Ваша раса: {dd[class_human.what]}\n'
    else:
        text += f'Ваша раса: -\n'
    print('СПИСОК ОБЕКТОВ')
    print([i.__class__.__bases__[0].__name__ for i in list_obj])
    if list_obj != []:
        text += f'Ваши карты на руках: \n'
        for i in range(len(list_obj)):
            if list_obj[i].__class__.__bases__[0].__name__ == 'BonusBase':
                text += f'{i + 1}) Бонус: "{list_obj[i].title}" ({list_obj[i].mini_text})\n'
            elif list_obj[i].__class__.__bases__[0].__name__ == 'ArmamentBase':
                text += f'{i + 1}) Одежка: "{list_obj[i].title}" (+{list_obj[i].bonus} strength)\n'
            elif list_obj[i].__class__.__bases__[0].__name__ == 'MonsterBase':
                text += f'{i + 1}) Монстр: "{list_obj[i].title}"; level={list_obj[i].level}\n'
            elif list_obj[i].__class__.__bases__[0].__name__ == 'RaceBase':
                text += f'{i + 1}) Раса: "{dd[class_human.what]}"\n'
    else:
        text += f'Ваши карты на руках: -\n'
    print(text)
    return text


def show_not_all_cards(user_id, res):
    dd = {1: 'Эльф', 2: 'Хафлинг', 3: 'Дварф'}
    armor = sessionStorage[user_id]['armor']
    weapon = sessionStorage[user_id]['weapon']
    class_human = sessionStorage[user_id]['class']
    list_obj = sessionStorage[user_id]['cards_on_hands']
    res['response']['text'] += 'Характеристики героя: '
    res['response']['text'] += f'level: {sessionStorage[user_id]["level"]}; '
    res['response'][
        'text'] += f'Cила: {sessionStorage[user_id]["overall_strength"] + sessionStorage[user_id]["level"]}; '
    res['response']['text'] += f'Монеты: {sessionStorage[user_id]["money"]}; '
    res['response']['text'] += f'Удача: {sessionStorage[user_id]["luck"]}; '
    if class_human is not None:
        res['response']['text'] += f'Раса: {dd[class_human.what]}; '
    else:
        res['response']['text'] += f'Раса: -; '
    if len(weapon) != 0:
        res['response']['text'] += f'Оружие: +{" +".join([str(i.bonus) for i in weapon])}; '
    else:
        res['response']['text'] += f'Оружие: -; '
    if armor['head'] is not None:
        res['response']['text'] += f'Головняк: {armor["head"].bonus}; '
    else:
        res['response']['text'] += f'Головняк: -; '
    if armor['body'] is not None:
        res['response']['text'] += f'Броня: {armor["body"].bonus}; '
    else:
        res['response']['text'] += f'Броня: -; '
    if armor['leg'] is not None:
        res['response']['text'] += f'Поножи: {armor["leg"].bonus}; '
    else:
        res['response']['text'] += f'Поножи: -; '

    res['response']['text'] += '\nКарты на руках:\n'
    for i in range(len(list_obj)):
        if list_obj[i].__class__.__bases__[0].__name__ == 'BonusBase':
            res['response'][
                'text'] += f'{i + 1}) Бонус: "{list_obj[i].title}" ({list_obj[i].mini_text})\n'
        elif list_obj[i].__class__.__bases__[0].__name__ == 'ArmamentBase':
            res['response'][
                'text'] += f'{i + 1}) Одежка: "{list_obj[i].title}" (+{list_obj[i].bonus})\n'
        elif list_obj[i].__class__.__bases__[0].__name__ == 'MonsterBase':
            res['response'][
                'text'] += f'{i + 1}) Монстр: "{list_obj[i].title}" ({list_obj[i].level} lvl)\n'
        elif list_obj[i].__class__.__bases__[0].__name__ == 'RaceBase':
            res['response']['text'] += f'{i + 1}) Раса: "{dd[class_human.what]}"\n'
    res['response']['text'] += 'Какие карты вы хотите положить? (номера)'


if __name__ == '__main__':
    app.run()
