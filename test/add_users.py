import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
url = 'http://127.0.0.1:8077/auth/login/'  # урл по которому происходит переход на регистрацию
driver = webdriver.Chrome(executable_path=r'C:\chromedriver.exe', options=chrome_options)  # путь до веб драйвера

users_data = []

for i in range(1000):
    users_data.append({
        'user': f'user{i}',
        'first_name': f'first_name{i}',
        'password': 'intergalactic',
        'email': f'user{i}@mail.ru',
        'age': random.randint(18, 80),
    })

driver.get(url)
try:
    for data in users_data:
        register = driver.find_element_by_id('register').get_attribute('href')
        driver.get(register)

        driver.find_element_by_name('username').send_keys(data['user'])
        driver.find_element_by_name('first_name').send_keys(data['first_name'])
        driver.find_element_by_name('password1').send_keys(data['password'])
        driver.find_element_by_name('password2').send_keys(data['password'])
        driver.find_element_by_name('email').send_keys(data['email'])
        driver.find_element_by_name('age').send_keys(data['age'])
        driver.find_element_by_xpath("//input[@type='submit']").send_keys(Keys.ENTER)


except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
