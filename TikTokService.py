import re
import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

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


def process_video_comments(driver, search, comment, templates, limit=3):
    """Основная функция для обработки видео с возможностью ответа на комментарии"""
    if not open_search_page(driver, search):
        return 0

    processed_count = 0
    attempts = 0

    if not open_first_video(driver):
        return 0

    while processed_count < limit:
        if send_comment(driver, comment):
            if templates:
                response_by_template(
                    driver=driver,
                    templates=templates,
                    comment=comment,
                    max_comments_to_check=40,
                    max_scroll_attempts=3
                )

    print(f"Итог: обработано {processed_count} видео")
    return processed_count

def open_first_video(driver):
    """Открывает первое видео в результатах поиска"""
    try:
        first_video = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div[data-e2e='search_video-item-list'] > div:first-child"))
        )
        first_video.click()
        time.sleep(2)
        return True
    except Exception as e:
        print(f"Не удалось открыть первое видео: {e}")
        return False


def scroll_searched_videos(driver):
    """Скролл найденных видео"""
    try:
        url = "https://www.tiktok.com/@marudeesu/video/7450164012181982469?q=axis&t=1745139751813"
        driver.get(url)
        while True:
            next_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-e2e='arrow-right']"))
            )
            next_button.click()
            time.sleep(2)
        return True
    except Exception as e:
        print(f"Не удалось перейти к следующему видео: {e}")
        return False


def send_comment(driver, comment):
    """Отправляет комментарий на текущем видео"""
    try:
        time.sleep(1)

        actions = ActionChains(driver)
        actions.send_keys(comment)
        actions.send_keys(Keys.RETURN)
        actions.perform()

        time.sleep(1)
        return True
    except Exception as e:
        print(f"Ошибка при отправке комментария: {e}")
        return False

def scroll_to_element(driver, element):
    """Прокручивает страницу к указанному элементу"""
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

def get_video_elements(driver):
    """Возвращает список элементов видео на текущей странице"""
    try:
        return driver.find_elements(By.CSS_SELECTOR, "div[data-e2e='search_video-item-list'] > div")
    except Exception:
        return []

def scroll_page(driver):
    """Прокручивает страницу вниз и проверяет успешность прокрутки"""
    try:
        last_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        return new_height != last_height
    except Exception:
        return False

def open_search_page(driver, search):
    """Открывает страницу поиска и проверяет загрузку"""
    try:
        driver.get(URL_FOR_FOUND + search)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-e2e='search_video-item-list']"))
        )
        return True
    except Exception as e:
        print(f"Ошибка при загрузке страницы поиска: {e}")
        return False


def response_by_template(driver, templates, comment, max_comments_to_check=30, max_scroll_attempts=3):
    """
    Анализирует комментарии с поддержкой скроллинга и отвечает по шаблонам

    :param driver: WebDriver
    :param templates: list - список фраз для поиска
    :param comment: str - ответный комментарий
    :param max_comments_to_check: int - максимум комментариев для анализа
    :param max_scroll_attempts: int - максимум попыток скроллинга
    :return: bool - был ли отправлен ответ
    """
    try:
        # Ожидаем загрузки комментариев
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.css-1i7ohvi-DivCommentItemContainer"))
        )

        collected_comments = []
        scroll_attempts = 0
        last_height = driver.execute_script("return document.documentElement.scrollHeight")

        while len(collected_comments) < max_comments_to_check and scroll_attempts < max_scroll_attempts:
            # Собираем текущие комментарии
            current_comments = driver.find_elements(By.CSS_SELECTOR, "div.css-1i7ohvi-DivCommentItemContainer")

            # Добавляем только новые комментарии
            for cmt in current_comments:
                if cmt not in collected_comments:
                    collected_comments.append(cmt)
                    if len(collected_comments) >= max_comments_to_check:
                        break

            # Скроллим вниз если нужно больше комментариев
            if len(collected_comments) < max_comments_to_check:
                driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
                time.sleep(2)

                # Проверяем достигли ли мы конца
                new_height = driver.execute_script("return document.documentElement.scrollHeight")
                if new_height == last_height:
                    scroll_attempts += 1
                last_height = new_height

        # Анализируем собранные комментарии
        for comment_element in collected_comments[:max_comments_to_check]:
            try:
                comment_text = comment_element.find_element(
                    By.CSS_SELECTOR, "p[data-e2e='comment-level-1']"
                ).text.lower()

                if any(template.lower() in comment_text for template in templates):
                    # Скроллим к нужному комментарию перед взаимодействием
                    driver.execute_script(
                        "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});",
                        comment_element
                    )
                    time.sleep(1)

                    reply_button = comment_element.find_element(
                        By.CSS_SELECTOR, "span[data-e2e='reply']"
                    )
                    reply_button.click()
                    time.sleep(1)

                    if send_reply(driver, comment):
                        return True

            except Exception as e:
                print(f"Ошибка при обработке комментария: {e}")
                continue

        print(f"Проверено {len(collected_comments)} комментариев, совпадений не найдено")
        return False

    except Exception as e:
        print(f"Ошибка в response_by_template: {e}")
        return False


def send_reply(driver, comment):
    """
    Отправляет ответ на комментарий
    """
    try:
        # Находим поле ввода ответа
        reply_input = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-e2e='reply-input']")))

        # Вводим текст
        reply_input.click()
        actions = ActionChains(driver)
        actions.send_keys(comment)
        actions.send_keys(Keys.RETURN)
        actions.perform()

        print("Ответ успешно отправлен: {}", comment)
        time.sleep(2)
        return True

    except Exception as e:
        print(f"Ошибка при отправке ответа: {e}")
        return False

def go_to_next_video(driver):
    """Переходит к следующему видео используя кнопку вправо"""
    try:
        next_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-e2e='arrow-right']"))
        )
        next_button.click()
        time.sleep(2)  # Ожидание загрузки следующего видео
        return True
    except Exception as e:
        print(f"Не удалось перейти к следующему видео: {e}")
        return False

def slow_writer(editor, text, delay=0.3):
    for char in text:
        editor.send_keys(char)
        time.sleep(delay)
