from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import TikTokService

if __name__ == '__main__':
    # Путь к профилю Firefox
    FIREFOX_PROFILE_PATH = "/Users/armanlyosman/Library/Application Support/Firefox/Profiles/ryt4a4ms.default-release"

    # Настройка опций
    options = Options()
    options.set_preference("dom.webnotifications.enabled", False)
    options.set_preference("profile", FIREFOX_PROFILE_PATH)
    options.set_preference("profile.default_content_setting_values.notifications", 2)
    options.set_preference("useAutomationExtension", False)
    options.set_preference("dom.webdriver.enabled", False)
    options.set_preference("general.useragent.override", "Mozilla/5.0")
    options.set_preference("general.useragent.override",
                           "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0")

    # Важно: явно указать путь к профилю
    options.profile = FIREFOX_PROFILE_PATH

    # Запуск драйвера
    driver = webdriver.Firefox(options=options)

    comment = "Очень понравился результат на вб: 246752538"
    url = "https://www.tiktok.com/@axisy/video/7350598350099451144?lang=ru-RU&q=Asix-Y"
    TikTokService.write_comment(driver, url, comment)

    driver.quit()

