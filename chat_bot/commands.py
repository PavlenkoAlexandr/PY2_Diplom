from chat_bot import keyboards as kb
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from chat_bot.utilite import message_text, status
from database import db_func
from vk_api_func.vk_class import Vkfunc
import re


class Basic:

    def start(self, event):
        try:
            return Vkfunc.write_msg(
                event.user_id,
                f'Хай, {db_func.user_info(event.user_id)["first_name"]}!',
                kb.start_keyboard(dict())
            )
        except NoResultFound:
            db_func.add_to_users(Vkfunc.get_user(event.user_id))
            return self.start(event)

    def stop(self, event, cls):
        cls.search_params.clear()
        return Vkfunc.write_msg(event.user_id, 'Пока((')


class Liked:

    def __init__(self):
        self.whitelist = iter(list())
        self.pair_id = int()

    def show(self, event):
        try:
            self.whitelist = iter(db_func.show_whitelist(event.user_id))
            self.pair_id, name, photos, url = next(self.whitelist)
            return Vkfunc.write_msg(
                event.user_id,
                f'{name}, {url}',
                attachment=photos,
                keyboard=kb.whitelist_keyboard(url)
            )
        except StopIteration:
            return Vkfunc.write_msg(
                        event.user_id,
                        f'Список понравившихся пуст &#128532;',
                        kb.back_button()
                    )

    def next(self, event):
        try:
            self.pair_id, name, photos, url = next(self.whitelist)
            return Vkfunc.write_msg(
                event.user_id,
                f'{name}, {url}',
                attachment=photos,
                keyboard=kb.whitelist_keyboard(url)
            )
        except StopIteration:
            return self.show(event)

    def remove(self, event):
        try:
            db_func.remove_from_whitelist(self.pair_id)
            self.next(event)
        except StopIteration:
            return self.show(event)
        except NoResultFound:
            return self.show(event)


class Search:

    def __init__(self):
        self.search_params = dict()
        self.search_list = iter(list())
        self.pair_id = int()
        self.marked_list = list()

    def clarify_message(self, event):
        return Vkfunc.write_msg(
            event.user_id,
            f'Уточните параметры поиска или нажмите начать поиск:\n{message_text(self.search_params)}',
            kb.start_keyboard(self.search_params)
        )

    def what_age(self, event):
        return Vkfunc.write_msg(event.user_id, f'Введите возраст в формате "от _ до _"')

    def age(self, event, request):
        if 'от ' in request and 'до ' in request:
            self.search_params['age_from'] = re.findall(r'\d+', request)[0]
            self.search_params['age_to'] = re.findall(r'\d+', request)[1]
            return self.clarify_message(event)
        elif 'от ' in request:
            self.search_params['age_from'] = re.findall(r'\d+', request)[0]
            return self.clarify_message(event)
        elif 'до ' in request:
            self.search_params['age_to'] = re.findall(r'\d+', request)[0]
            return self.clarify_message(event)

    def what_sex(self, event):
        return Vkfunc.write_msg(event.user_id, f'Выберите пол', kb.sex_keyboard())

    def sex(self, event, request):
        if request == 'ж':
            self.search_params['sex'] = '1'
        elif request == 'м':
            self.search_params['sex'] = '2'
        elif request == 'м/ж':
            self.search_params['sex'] = None
        return self.clarify_message(event)

    def what_status(self, event):
        return Vkfunc.write_msg(event.user_id, f'Выберите статус', kb.status_keyboard())

    def status(self, event, request):
        self.search_params['status'] = status[request]
        return self.clarify_message(event)

    def what_city(self, event):
        return Vkfunc.write_msg(event.user_id, f'Введите название города')

    def city(self, event, request):
        self.search_params['city'] = Vkfunc.get_city(request)
        return self.clarify_message(event)

    def reset(self, event):
        self.search_params.clear()
        self.search_list = iter(list())
        self.pair_id = int()
        return self.clarify_message(event)

    def incorrect_input(self, event):
        return Vkfunc.write_msg(
            event.user_id,
            f'Не поняла вашего ответа... &#129300;',
            kb.start_keyboard(self.search_params)
        )

    def search_message(self, event, url, photos):
        return Vkfunc.write_msg(
            event.user_id,
            f'{" ".join(Vkfunc.get_user_name(self.pair_id))}\n{url}',
            kb.main_keyboard(),
            attachment=photos
        )

    def search(self, event, offset=None):
        self.search_list = iter(Vkfunc.search_users(self.search_params, offset=offset))
        self.marked_list = db_func.marked_ids(event.user_id)
        try:
            self.pair_id, url = next(self.search_list)
            while self.pair_id in self.marked_list:
                self.pair_id, url = next(self.search_list)
            photos = ','.join([f'photo{self.pair_id}_{photo}' for photo in Vkfunc.get_photos(self.pair_id)])
            return self.search_message(event, url, photos)
        except StopIteration:
            return Vkfunc.write_msg(
                event.user_id,
                f'По такому запросу никого не найдено &#128532;',
                kb.back_button()
            )

    def like(self, event):
        if self.pair_id:
            try:
                photos = ','.join([f'photo{self.pair_id}_{photo}' for photo in Vkfunc.get_photos(self.pair_id)])
                name = " ".join(Vkfunc.get_user_name(self.pair_id))
                try:
                    db_func.add_to_whitelist(event.user_id, self.pair_id, photos, name, Vkfunc.get_url(self.pair_id))
                except IntegrityError:
                    db_func.add_to_users(Vkfunc.get_user(event.user_id))
                    db_func.add_to_whitelist(event.user_id, self.pair_id, photos, name, Vkfunc.get_url(self.pair_id))
                self.pair_id, url = next(self.search_list)
                while self.pair_id in self.marked_list:
                    self.pair_id, url = next(self.search_list)
                photos = ','.join([f'photo{self.pair_id}_{photo}' for photo in Vkfunc.get_photos(self.pair_id)])
                return self.search_message(event, url, photos)
            except StopIteration:
                self.search(event, offset=len(list(self.search_list)))
        else:
            return self.clarify_message(event)

    def not_like(self, event):
        if self.pair_id:
            try:
                try:
                    db_func.add_to_blacklist(event.user_id, self.pair_id)
                except IntegrityError:
                    db_func.add_to_users(Vkfunc.get_user(event.user_id))
                    db_func.add_to_blacklist(event.user_id, self.pair_id)
                self.pair_id, url = next(self.search_list)
                while self.pair_id in self.marked_list:
                    self.pair_id, url = next(self.search_list)
                photos = ','.join([f'photo{self.pair_id}_{photo}' for photo in Vkfunc.get_photos(self.pair_id)])
                return self.search_message(event, url, photos)
            except StopIteration:
                self.search(event, offset=len(list(self.search_list)))
        else:
            return self.clarify_message(event)
