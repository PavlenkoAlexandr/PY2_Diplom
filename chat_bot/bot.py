import vk_api
import settings
from vk_api.longpoll import VkLongPoll, VkEventType
from chat_bot import commands, utilite


def main():
    vk = vk_api.VkApi(token=settings.COMMUNITY_TOKEN)
    longpoll = VkLongPoll(vk)

    Liked = commands.Liked()
    Search = commands.Search()
    Basic = commands.Basic()

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:

                request = event.text.lower()

                if request == 'привет' or request == 'начать':
                    Basic.start(event)

                elif request == 'назад':
                    Search.clarify_message(event)

                elif request == 'понравившиеся':
                    Liked.show(event)

                elif request == 'следующий':
                    Liked.next(event)

                elif request == 'удалить':
                    Liked.remove(event)

                elif request == 'возраст':
                    Search.what_age(event)

                elif 'от ' in request or 'до ' in request:
                    Search.age(event, request)

                elif request == 'пол':
                    Search.what_sex(event)

                elif request == 'м' or request == 'ж' or request == 'м/ж':
                    Search.sex(event, request)

                elif request == 'семейное положение':
                    Search.what_status(event)

                elif request in utilite.status:
                    Search.status(event, request)

                elif request == 'город':
                    Search.what_city(event)

                elif request in utilite.cities:
                    Search.city(event, request)

                elif request == 'сброс':
                    Search.reset(event)

                elif request == 'поиск':
                    Search.search(event)

                elif request == 'нравится':
                    Search.like(event)

                elif request == 'не нравится':
                    Search.not_like(event)

                elif request == 'пока':
                    Basic.stop(event, Search)

                else:
                    Search.incorrect_input(event)


if __name__ == '__main__':
    main()
