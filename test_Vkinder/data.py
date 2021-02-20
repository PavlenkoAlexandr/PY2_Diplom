from settings import SELF_ID


class Event:

    def __init__(self, user_id):
        self.user_id = user_id


user = {
    'vk_id': SELF_ID,
    'birthdate': '01.01.1970',
    'sex': 1,
    'first_name': 'first_name',
    'last_name': 'last_name',
    'city': 'city'
}

event = Event(SELF_ID)

pavel_durov_user_data = {
    'birthdate': '10.10.1984',
    'city': 'Санкт-Петербург',
    'first_name': 'Павел',
    'last_name': 'Дуров',
    'sex': 2,
    'vk_id': 1
}

status = {
        '1': 'не женат (не замужем)',
        '5': 'всё сложно',
        '6': 'в активном поиске',
        None: 'любое'
    }

search = [{
        "first_name": "Павел",
        "id": 1,
        "last_name": "Дуров",
        "can_access_closed": True,
        "is_closed": False,
        "screen_name": "durov",
        "track_code": "34d6796colH7VO7NAqXPxxNSaih2t9dGvnOGKvWOzqRexnOSEhXFOLgAs69VwZbHYc2-n5S0"
    }, {
        "first_name": "Иван",
        "id": 53636214,
        "last_name": "Рудской",
        "can_access_closed": True,
        "is_closed": False,
        "screen_name": "eeoneguy",
        "track_code": "bc090cfftJOdPWYMWqajfInOTl8tljaZGv-bF5udJWwMjUkAWBzT-tZtajNb9qN7vgjOrsn4UoQF8oxllQ"
    }, {
        "first_name": "Дмитрий",
        "id": 53083705,
        "last_name": "Медведев",
        "can_access_closed": True,
        "is_closed": False,
        "screen_name": "dm",
        "track_code": "51d8159aO4uk5o88U-eJrxvgfbzfU1YdJ0HaipOhj4fyxfMJ9Zdc4uOwg1ZfttrzKiP8TDs9MgA4TM34nQ"
    }, {
        "first_name": "Павел",
        "id": 135336811,
        "last_name": "Воля",
        "can_access_closed": True,
        "is_closed": False,
        "screen_name": "realvolya",
        "track_code": "cf4b6a8fWBzYT_aRDYOhmFOewXeGUReD5FDkm6Imzen-bC8vEHE_dZJJ__4Ng_fIY1xIg1VUf43iU-SbrEA"
    }, {
        "first_name": "Катя",
        "id": 5592362,
        "last_name": "Клэп",
        "can_access_closed": True,
        "is_closed": False,
        "screen_name": "kate_clapp",
        "track_code": "c39d7d71yiLlKDhPB2vAWWn4mJGJZO8S-wl_XAODOd5gaBIn6BCtS_R-Y3ABb58JXjobUgYGmBbqExou"
    }]
