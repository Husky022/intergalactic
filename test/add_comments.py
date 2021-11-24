import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
url_login = 'http://127.0.0.1:8077/auth/login/'  # урл входа
url_article = 'http://127.0.0.1:8077/article_page/11/'  # урл статьи где будут оставлены комменты
driver = webdriver.Chrome(executable_path=r'C:\chromedriver.exe', options=chrome_options)  # путь до веб драйвера
user = 'admin'
password = 'intergalactic'

users_data = []

driver.get(url_login)

try:
    driver.find_element_by_name('username').send_keys(user)
    driver.find_element_by_name('password').send_keys(password)
    enter_btn = driver.find_element_by_xpath("//input[@type='submit']")
    enter_btn.send_keys(Keys.ENTER)
except:
    print('проверьте логин/пароль')

driver.get(url_article)

try:
    driver.find_element_by_name('text_comment').send_keys('Я бот')
    send_btn = driver.find_element_by_xpath("//input[@type='submit']")
    send_btn.send_keys(Keys.ENTER)
except:
    print('не удалось оставить коммент')

for _ in range(50):
    try:
        driver.find_element_by_xpath("//*[contains(text(), 'Ответить')]").send_keys(Keys.ENTER)
        driver.find_element_by_name('text_subcomment').send_keys('Я бот')
        send_btn = driver.find_element_by_xpath("//div[contains(@class, 'text-right')]/button")
        send_btn.send_keys(Keys.ENTER)
    except:
        print('не удалось оставить подкоммент')

driver.close()
driver.quit()
