import json
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

service = Service('./chromedriver.exe')
driver = webdriver.Chrome(service=service)
actions = ActionChains(driver)

driver.get('https://scrapingclub.com/exercise/list_infinite_scroll/')

WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'card')))

first_height = driver.execute_script("return document.body.scrollHeight")
#print(first_height)

while True:
    pause_time = random.randint(1, 3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(pause_time)

    new_height = driver.execute_script("return document.body.scrollHeight")
    #print(new_height)
    if new_height == first_height:
        break
    first_height = new_height


items = driver.find_elements(by=By.XPATH, value="//div[@class='card']")
item_list = []
for item in items:
    pic = item.find_element(by=By.XPATH, value=".//a/img").get_attribute('src')
    link = item.find_element(by=By.XPATH, value=".//a").get_attribute('href')
    name = item.find_element(by=By.XPATH,
                             value=".//div[@class='card-body']/h4[@class='card-title']/a").text
    price = item.find_element(by=By.XPATH, value=".//div[@class='card-body']/h5").text

    tmp_dict = {
        'pic': pic,
        'link': link,
        'name': name,
        'price': price
    }
    item_list.append(tmp_dict)


driver.quit()

with open('items_list.json', 'w', encoding='utf-8') as jf:
    json.dump(item_list, jf)
