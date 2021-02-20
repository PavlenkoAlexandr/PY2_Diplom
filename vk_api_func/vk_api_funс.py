import vk_api
from random import randrange


class Vkapifunc:

    def __init__(self, self_token, community_token):
        self.self_token = self_token
        self.community_token = community_token
        self.vk_funk = vk_api.VkApi(token=self.self_token)
        self.vk_group_funk = vk_api.VkApi(token=self.community_token)

    def search_users(self, values: dict, has_photo='1', count='1000', fields='screen_name,is_closed', offset=None, q=None):
        values['q'] = q
        values['has_photo'] = has_photo
        values['count'] = count
        values['fields'] = fields
        values['offset'] = offset
        result = self.vk_funk.method('users.search', values)
        return [[item['id'], f'https://vk.com/{item["screen_name"]}'] for item in result['items'] if
                item['is_closed'] is False]

    def get_url(self, id):
        result = self.vk_funk.method('users.get', {'user_ids': id, 'fields': 'screen_name'})[0]
        return f'https://vk.com/{result["screen_name"]}'

    def get_user_name(self, id):
        result = self.vk_funk.method('users.get', {'user_ids': id})
        return [result[0]['first_name'], result[0]['last_name']]

    def get_user(self, id, fields='sex,bdate,city'):
        result = self.vk_funk.method('users.get', {'user_ids': id, 'fields': fields})[0]
        user_data = {
            'vk_id': id,
            'birthdate': result['bdate'] if 'bdate' in result else None,
            'sex': result['sex'] if 'sex' in result else None,
            'first_name': result['first_name'] if 'first_name' in result else None,
            'last_name': result['last_name'] if 'last_name' in result else None,
            'city': result['city']['title'] if 'city' in result else None
        }
        return user_data

    def get_photos(self, id, album_id='profile', count='1000', extended='1'):
        result = self.vk_funk.method('photos.get',
                                     {'owner_id': id, 'album_id': album_id, 'count': count, 'extended': extended})
        photos = sorted(result['items'], key=lambda x: (int(x['likes']['count']) + int(x['comments']['count'])),
                        reverse=True)
        return [photo['id'] for photo in photos][0:3]

    def get_city(self, city, country_id=1):
        result = self.vk_funk.method('database.getCities', {'country_id': country_id, 'q': city})
        return result['items'][0]['id']

    def get_city_name(self, city_ids):
        result = self.vk_funk.method('database.getCitiesById', {'city_ids': city_ids})
        return result[0]['title']

    def write_msg(self, user_id, message, keyboard=None, attachment=None):
        self.vk_group_funk.method('messages.send', {
            'user_id': user_id,
            'message': message,
            'keyboard': keyboard,
            'random_id': randrange(10 ** 7),
            'attachment': attachment
        }
                             )
        return True
