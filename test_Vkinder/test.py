import re
from chat_bot import commands
from database import db_func
from test_Vkinder import data
from test_Vkinder.data import event
from vk_api_func.vk_class import Vkfunc
import pytest

class Testdbfunk:

    def test_add_and_check_user(self):

        db_func.drop_whitelist(data.SELF_ID)
        db_func.drop_blacklist(data.SELF_ID)
        db_func.delete_user(data.SELF_ID)
        db_func.add_to_users(data.user)
        assert db_func.check_id_in_database(data.SELF_ID) is True

    def test_db_user_info(self):

        assert data.user == db_func.user_info(data.SELF_ID)

    def test_add_white_black_list(self):

        db_func.add_to_whitelist(data.SELF_ID, data.SELF_ID, 'test', 'test', 'test')
        db_func.add_to_blacklist(data.SELF_ID, data.SELF_ID)
        assert data.SELF_ID in db_func.blacklist_ids(data.SELF_ID) and data.SELF_ID in db_func.whitelist_ids(data.SELF_ID)

    def test_drop_white_black_list(self):

        db_func.drop_whitelist(data.SELF_ID)
        db_func.drop_blacklist(data.SELF_ID)
        assert data.SELF_ID not in db_func.blacklist_ids(data.SELF_ID) and data.SELF_ID not in db_func.whitelist_ids(data.SELF_ID)

    def test_remove_from_whitelist(self):

        db_func.add_to_whitelist(data.SELF_ID, data.SELF_ID, 'test', 'test', 'test')
        db_func.remove_from_whitelist(data.SELF_ID)
        assert data.SELF_ID in db_func.blacklist_ids(data.SELF_ID)

    def test_show_white_list(self):

        db_func.drop_whitelist(data.SELF_ID)
        db_func.add_to_whitelist(data.SELF_ID, data.SELF_ID, 'test', 'test', 'test')
        assert db_func.show_whitelist(data.SELF_ID) == [[data.SELF_ID, 'test', 'test', 'test']]

    def test_db_delete_user(self):

        db_func.drop_whitelist(data.SELF_ID)
        db_func.drop_blacklist(data.SELF_ID)
        db_func.delete_user(data.SELF_ID)
        assert db_func.check_id_in_database(data.SELF_ID) is False


class Testvkapifunk:

    def test_search_users(self):
        assert Vkfunc.search_users({}, count=1, q='Павел Дуров') == [[1, 'https://vk.com/durov']]

    def test_get_url(self):
        assert Vkfunc.get_url(1) == 'https://vk.com/durov'

    def test_get_user_name(self):
        assert Vkfunc.get_user_name(1) == ['Павел', 'Дуров']

    def test_get_user(self):
        assert Vkfunc.get_user(1) == data.pavel_durov_user_data

    def test_get_photos(self):
        assert Vkfunc.get_photos(1, count=1) == [215187843]

    def test_get_city(self):
        assert Vkfunc.get_city('Тверь') == 141

    def test_get_city_name(self):
        assert Vkfunc.get_city_name(141) == 'Тверь'

    def test_write_msg(self):
        assert Vkfunc.write_msg(data.user['vk_id'], 'test') is True


class Testchatbotcommands:

    @classmethod
    def setup_class(cls):
        cls.Liked = commands.Liked()
        cls.Search = commands.Search()
        cls.Basic = commands.Basic()

    def test_start(self):
        db_func.drop_whitelist(event.user_id)
        db_func.drop_blacklist(event.user_id)
        db_func.delete_user(event.user_id)
        assert self.Basic.start(event) is True and db_func.check_id_in_database(event.user_id) is True

    def test_stop(self):
        assert self.Basic.stop(event, self.Search) is True and any(self.Search.search_params) is False

    @pytest.mark.parametrize('text', ['от 20 до 30', 'от 20', 'до 30'])
    def test_age(self, text):
        self.Search.age(event, text)
        if 'от ' in text:
            assert self.Search.search_params['age_from'] == re.findall(r'\d+', text)[0]
        elif ' до ' in text:
            assert (self.Search.search_params['age_to'] == re.findall(r'\d+', text)[1] and
                    self.Search.search_params['age_from'] == re.findall(r'\d+', text)[0])

    @pytest.mark.parametrize('text', ['м', 'ж', 'м/ж'])
    def test_sex(self, text):
        self.Search.sex(event, text)
        if text == 'ж':
            assert self.Search.search_params['sex'] == '1'
        elif text == 'м':
            assert self.Search.search_params['sex'] == '2'
        elif text == 'м/ж':
            assert self.Search.search_params['sex'] == None

    @pytest.mark.parametrize('text', [[key, value] for key, value in data.status.items()])
    def test_status(self, text):
        self.Search.status(event, text[1])
        assert self.Search.search_params['status'] == text[0]

    def test_city(self):
        self.Search.city(event, 'Тверь')
        assert self.Search.search_params['city'] == 141

    def test_reset(self):
        self.Search.reset(event)
        if not self.Search.pair_id:
            assert any(self.Search.search_params) is False and len(list(self.Search.search_list)) == 0
        else:
            assert False

    def test_search(self):
        db_func.drop_whitelist(event.user_id)
        db_func.drop_blacklist(event.user_id)
        self.Search.search(event)
        assert self.Search.pair_id == data.search[0]['id']

    def test_like(self):
        self.Search.like(event)
        assert self.Search.pair_id == data.search[1]['id'] and data.search[0]['id'] in db_func.whitelist_ids(event.user_id)

    def test_not_like(self):
        self.Search.not_like(event)
        assert self.Search.pair_id == data.search[2]['id']and data.search[1]['id'] in db_func.blacklist_ids(event.user_id)

    def test_show_white(self):
        db_func.drop_blacklist(event.user_id)
        self.Search.search(event)
        self.Search.like(event)
        self.Liked.show(event)
        assert self.Liked.pair_id == data.search[0]['id']

    def test_next(self):
        self.Liked.next(event)
        assert self.Liked.pair_id == data.search[1]['id']

    def test_remove(self):
        self.Liked.remove(event)
        assert data.search[1]['id'] not in db_func.whitelist_ids(event.user_id)
