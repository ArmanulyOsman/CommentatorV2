from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import time
import re

TIKTOK_BASE_URL = "https://www.tiktok.com/"
URL_FOR_FOUND = TIKTOK_BASE_URL + "search/video?lang=ru-RU&q="
LOGIN_EMAIL_URL = TIKTOK_BASE_URL + "login/phone-or-email/email"
LOGIN_PHONE_URL = TIKTOK_BASE_URL + "login/phone-or-email/phone-password"

def login(driver, username, password):
    try:
        if is_valid_email(username):
            driver.get(LOGIN_EMAIL_URL)
        else:
            driver.get(LOGIN_PHONE_URL)

        editor = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']")))
        slow_writer(editor, username)
        editor = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Пароль']")))
        slow_writer(editor, password)

        editor.send_keys(Keys.ENTER)
    except Exception as e:
        print(f"Ошибка: {e}")

def is_valid_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def send_comment_to_founded_videos(driver, search, comment, limit=3):
    driver.get(URL_FOR_FOUND + search)

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-e2e='search_video-item-list']"))
    )

    processed_videos = 0
    attempts = 0
    max_attempts = 5

    while processed_videos < limit and attempts < max_attempts:
        video_items = driver.find_elements(By.CSS_SELECTOR, "div[data-e2e='search_video-item-list'] > div")
        new_videos_processed = False

        for index, video in enumerate(video_items):
            try:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", video)
                time.sleep(1)

                # Открываем видео
                video.click()
                time.sleep(2)

                # Просто отправляем текст напрямую
                actions = ActionChains(driver)
                actions.send_keys(comment)
                actions.send_keys(Keys.RETURN)
                actions.perform()

                processed_videos += 1
                new_videos_processed = True
                print(f"Комментарий отправлен на видео {index + 1}")

                # Возвращаемся назад
                driver.back()
                time.sleep(2)

                # Обновляем список элементов
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-e2e='search_video-item-list']"))
                )

                if processed_videos >= limit:
                    break

            except Exception as e:
                print(f"Ошибка при обработке видео {index}: {e}")
                continue

        if new_videos_processed:
            attempts = 0
        else:
            attempts += 1

        if processed_videos < limit:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == driver.execute_script("return window.pageYOffset + window.innerHeight"):
                attempts = max_attempts

    print(f"Итог: обработано {processed_videos} видео")
    return processed_videos

def send_comment(driver, comment):
    try:
        # Пытаемся найти активное поле ввода
        editor = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-e2e='comment-input']"))
        )

        editor.send_keys(comment)
        time.sleep(0.5)

        editor.send_keys(Keys.RETURN)
        time.sleep(1)

    except Exception as e:
        print(e)

    return False

def slow_writer(editor, text, delay=0.3):
    for char in text:
        editor.send_keys(char)
        time.sleep(delay)
