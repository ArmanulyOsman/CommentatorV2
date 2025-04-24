import ExcelService
import undetected_chromedriver as uc
import TikTokService

if __name__ == '__main__':
    with open("templates.txt", "r", encoding="utf-8") as file:
        templates = [line.rstrip('\n') for line in file]
    print(templates)

    excel_name = input("File name: ")
    creds = ExcelService.extract_data_from_excel(excel_name)

    print()
    print(creds.phone_number)
    print(creds.password)
    print(creds.username)
    print(creds.comments)

    driver = uc.Chrome()

    TikTokService.login(driver, str(creds.phone_number), str(creds.password))

    TikTokService.process_video_comments(driver, str(creds.query),
                                         creds.comments, templates, str(creds.username))

    driver.quit()
