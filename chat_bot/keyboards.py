from vk_api.keyboard import VkKeyboard, VkKeyboardColor


def start_keyboard(values: dict):
    keyboard = VkKeyboard(one_time=True)

    if 'age_from' in values or 'age_to' in values:
        keyboard.add_button('Возраст', color=VkKeyboardColor.POSITIVE)
    elif 'age_from' not in values and 'age_to' not in values:
        keyboard.add_button('Возраст')
    keyboard.add_line()

    if 'sex' in values:
        keyboard.add_button('Пол', color=VkKeyboardColor.POSITIVE)
    elif 'sex' not in values:
        keyboard.add_button('Пол')
    keyboard.add_line()

    if 'status' in values:
        keyboard.add_button('Семейное положение', color=VkKeyboardColor.POSITIVE)
    elif 'status' not in values:
        keyboard.add_button('Семейное положение')
    keyboard.add_line()

    if 'city' in values:
        keyboard.add_button('Город', color=VkKeyboardColor.POSITIVE)
    elif 'city' not in values:
        keyboard.add_button('Город')

    keyboard.add_line()
    keyboard.add_button('Поиск', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Сброс', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button('Понравившиеся', color=VkKeyboardColor.PRIMARY)
    return keyboard.get_keyboard()


def status_keyboard():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Не женат (не замужем)')
    keyboard.add_line()
    keyboard.add_button('Всё сложно')
    keyboard.add_line()
    keyboard.add_button('В активном поиске')
    keyboard.add_line()
    keyboard.add_button('Любое')
    return keyboard.get_keyboard()


def sex_keyboard():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('ж')
    keyboard.add_button('м')
    keyboard.add_button('м/ж')
    return keyboard.get_keyboard()


def main_keyboard():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Нравится', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Не нравится', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button('Понравившиеся', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Назад', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('Сброс', color=VkKeyboardColor.SECONDARY)
    return keyboard.get_keyboard()


def whitelist_keyboard(url):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_openlink_button('Перейти', link=url)
    keyboard.add_line()
    keyboard.add_button('Следующий')
    keyboard.add_button('Удалить', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
    return keyboard.get_keyboard()


def back_button():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
    return keyboard.get_keyboard()