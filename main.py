import random

import undetected_chromedriver as uc

import TikTokService


def get_comment():
    commments = [
        "Приобрела по артикулу 246752538 — оригинальный товар, рекомендую!",
        "Артикул 246752538 — покупкой довольна, это оригинал, рекомендую.",
        "Взяла по артикулу 246752538, качество отличное, оригинал, советую!",
        "Покупала по артикулу 246752538 — всё отлично, товар оригинальный, рекомендую.",
        "Заказала по артикулу 246752538, получила оригинал — рекомендую к покупке.",
        "Купила по артикулу 246752538, пришёл оригинал, рекомендую однозначно."
    ]
    return commments[random.randint(0, len(commments) - 1)]

templates = [
    'Артикул',
    'Вб',
    'Вайлбериз',
    'wb',
    'wilberries',
]
if __name__ == '__main__':
    driver = uc.Chrome()

    # phone = input("Почта или телефон(без +77): ")
    # password = input("Пароль: ")
    phone = "476283763"
    password = "0u0p4M4u@!"



    TikTokService.login(driver, phone, password)

    query = input("Запрос: ")

    TikTokService.process_video_comments(driver, query, get_comment(), templates)

    driver.quit()

