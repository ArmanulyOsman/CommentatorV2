import re
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

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
        input("Is log?: ")
    except Exception as e:
        print(f"Ошибка: {e}")

def is_valid_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def process_video_comments(driver, search, comments, templates, username, tracker, limit=200):
    """Основная функция для обработки видео с возможностью ответа на комментарии"""
    if not open_search_page(driver, search):
        return 0

    processed_count = 0
    attempts = 0

    if not open_first_video(driver):
        return 0
    close_some_icon(driver)

    while processed_count < limit and attempts < 5:
        try:
            comment = comments[random.randint(0, len(templates) - 1)]
            # Получаем текущий URL видео
            current_url = driver.current_url
            video_id = tracker.extract_video_id(current_url)

            if not video_id:
                print("Не удалось извлечь ID видео")
                attempts += 1
                continue

            if tracker.already_commented(video_id):
                print(f"Видео {video_id} уже комментировалось")
                attempts += 1
            else:
                if send_comment(driver, comment):
                    tracker.mark_as_commented(video_id, comment, username)
                    processed_count += 1
                    print(f"Комментарий отправлен ({processed_count}/{limit})")
                    attempts = 0
                else:
                    attempts += 1
                # if templates:
                #     print("Проверяем комментарии на совпадения...")
                #     replies_sent = response_by_template(
                #         driver=driver,
                #         templates=templates,
                #         reply_comments=comments,
                #         username=username
                #     )
                #     print(f"На видео {processed_count} отправлено {replies_sent} ответов")
            # Переход к следующему видео
            if not go_to_next_video(driver):
                break

            if processed_count < limit and not go_to_next_video(driver):
                break

        except Exception as e:
            print(f"Ошибка в основном цикле: {e}")
            attempts += 1
            continue

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

def close_some_icon(driver):
    try:
        close_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div[class='css-mp9aqo-DivIconCloseContainer e1vz198y6']")))
        close_btn.click()
    except Exception as e:
        print(f"Some icon not found: {str(e)} ")

def send_comment(driver, comment):
    """
    Улучшенная функция отправки комментария с обработкой "element not interactable"

    :param driver: WebDriver
    :param comment: Текст комментария
    :return: True, если комментарий отправлен, иначе False
    """
    try:
        comment_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@data-e2e="comment-input"]'))
        )
        comment_box.click()

        # Вводим текст комментария
        comment_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"]'))
        )
        comment_input.send_keys(comment)

        # Отправляем комментарий
        post_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@data-e2e="comment-post"]'))
        )
        post_button.click()

        print("Комментарий успешно отправлен!")

        print(f"✅ Sent comment: {comment}")
        time.sleep(1)  # Пауза перед следующим действием
        return True

    except Exception as e:
        print(f"⚠️ Comment can't sent: {str(e)}")
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

def response_by_template(driver, templates, username, reply_comments, max_comments=100):
    """
    Анализирует комментарии, игнорируя свои, и отвечает по шаблонам

    :param driver: WebDriver
    :param templates: list - фразы для поиска в комментариях
    :param reply_text: str - текст ответа
    :param username: str - ваш username (чтобы игнорировать свои комментарии)
    :param max_comments: int - макс. комментариев для проверки
    :return: bool - был ли отправлен ответ
    """
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.css-1i7ohvi-DivCommentItemContainer")))

        replies_sent = 0
        comments = driver.find_elements(By.CSS_SELECTOR, "div.css-1i7ohvi-DivCommentItemContainer")[:max_comments]

        for comment in comments:
            try:
                # Пропускаем комментарии текущего пользователя
                if username:
                    comment_author = comment.find_element(By.CSS_SELECTOR, "span[data-e2e='comment-username-1']").text
                    if comment_author.lower() == username.lower():
                        continue

                # Получаем текст комментария
                comment_text = comment.find_element(
                    By.CSS_SELECTOR, "p[data-e2e='comment-level-1']"
                ).text.lower()
                print(f"Проверить: {comment_text}")

                # Проверяем совпадение с шаблонами
                if any(template.lower() in comment_text for template in templates):
                    # Прокручиваем к комментарию
                    driver.execute_script(
                        "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});",
                        comment
                    )
                    time.sleep(1)

                    # Нажимаем "Ответить"
                    comment.find_element(By.CSS_SELECTOR, "span[data-e2e='comment-reply-1']").click()
                    time.sleep(1)
                    reply_text = reply_comments[random.randint(0, len(reply_comments) - 1)]

                    # Отправляем ответ
                    if send_reply(driver, reply_text):
                        replies_sent += 1
                        print(f"✅ Ответ отправлен на комментарий: {comment_text[:50]}...")
            except Exception as e:
                print(f"⚠️ Ошибка при обработке комментария: {e}")
                continue

        print("🔍 Совпадений с шаблонами не найдено (или все подходящие комментарии - свои)")
        return replies_sent

    except Exception as e:
        print(f"❌ Ошибка в response_by_template: {e}")
        return 0

def send_reply(driver, comment):
    """
    Отправляет ответ на комментарий
    """
    try:
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
        print("Переход к следеещему видео")
        driver.find_element(By.CSS_SELECTOR, 'button[data-e2e="arrow-right"]').click()
        time.sleep(3)  # Ожидание загрузки следующего видео
        return True
    except Exception as e:
        print(f"Не удалось перейти к следующему видео: {e}")
        return False

def slow_writer(editor, text, delay=0.3):
    for char in text:
        editor.send_keys(char)
        time.sleep(delay)
