import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

TIKTOK_BASE_URL = "https://www.tiktok.com/"
URL_FOR_FOUND = TIKTOK_BASE_URL + "search/video?lang=ru-RU&q="


def write_comment(driver, video_url, comment):
    try:
        driver.get(video_url)

        editor = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div[data-e2e='comment-input'] div[contenteditable='true']"))
        )
        slow_writer(editor, comment)
        editor.send_keys(Keys.RETURN)
    except Exception as e:
        print(f"Ошибка: {e}")

def slow_writer(editor, text, delay=0.3):
    for char in text:
        editor.send_keys(char)
        time.sleep(delay)
