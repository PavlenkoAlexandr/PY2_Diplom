import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from vk_api_func.vk_class import Vkfunc


def message_text(values: dict):

    status_for_keyboard = {
        '1': 'Не женат (не замужем)',
        '5': 'Всё сложно',
        '6': 'В активном поиске',
        None: 'Любое'
    }

    sex_for_keyboard = {
        '1': 'Ж',
        '2': 'М',
        None: 'М/Ж'
    }

    string_1 = str()
    string_2 = str()
    string_3 = str()
    string_4 = str()

    if 'age_from' in values and 'age_to' in values:
        string_1 = f'\nВозраст: от {values["age_from"]} до {values["age_to"]} &#9989;'
    elif 'age_from' in values:
        string_1 = f'\nВозраст: от {values["age_from"]} &#9989;'
    elif 'age_to' in values:
        string_1 = f'\nВозраст: до {values["age_to"]} &#9989;'
    elif 'age_from' not in values and 'age_to' not in values:
        string_1 = '\nВозраст: не указан'

    if 'sex' in values:
        string_2 = f'\nПол: {sex_for_keyboard[values["sex"]]} &#9989;'
    elif 'sex' not in values:
        string_2 = '\nПол: не указан'

    if 'status' in values:
        string_3 = f'\nСП: {status_for_keyboard[values["status"]]} &#9989;'
    elif 'status' not in values:
        string_3 = '\nСемейное положение: не указано'

    if 'city' in values:
        string_4 = f'\nГород: {Vkfunc.get_city_name(values["city"])} &#9989;'
    elif 'city' not in values:
        string_4 = '\nГород: не указан'

    text = string_1 + string_2 + string_3 + string_4

    return text


with open(os.path.join(BASE_DIR, 'cities.json'), encoding='utf-8-sig') as f:
    data = json.load(f)
cities = [city['Город'].lower() for city in data]

status = {
    'не женат (не замужем)': '1',
    'всё сложно': '5',
    'в активном поиске': '6',
    'любое': None
}