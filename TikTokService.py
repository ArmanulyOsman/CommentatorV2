from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

def send_comment(driver, video_url, comment):
    driver.get(video_url)

    try:
        editor = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div[data-e2e='comment-text']")
            )
        )
        editor.click()
        editor = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div[data-e2e='comment-input']"))
        )
        editor.send_keys(comment)
        editor.send_keys(Keys.RETURN)
        print(f"Sent comment: {comment} to video {video_url}")
        editor.click()
    except Exception as e:
        print(f"Failed to send comment to {video_url}. Error: {str(e)}")

def send_comment_to_founded_videos(driver, search, comment, limit=3):
    driver.get(URL_FOR_FOUND + search)

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-e2e='search_video-item-list']"))
    )

    seen_links = set()
    last_height = driver.execute_script("return document.body.scrollHeight")

    while len(seen_links) < limit:
        links = driver.find_elements(By.CSS_SELECTOR, "a[class='css-1mdo0pl-AVideoContainer e19c29qe4']")

        for link in links:
            href = link.get_attribute("href")
            send_comment(driver, href, comment)
            if href and href not in seen_links:
                seen_links.add(href)
                if len(seen_links) >= limit:
                    break

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    print(f"Founded {len(seen_links)} videos")
    return list(seen_links)[:limit]

def slow_writer(editor, text, delay=0.3):
    for char in text:
        editor.send_keys(char)
        time.sleep(delay)
