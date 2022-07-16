from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

service = Service('./chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.get('https://scrapingclub.com/exercise/basic_login/')

WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'id_name')))

login = driver.find_element(by=By.XPATH, value="//input[@id='id_name']")
password = driver.find_element(by=By.ID, value="id_password")

login.send_keys('scrapingclub')
password.send_keys('scrapingclub')

button_login = driver.find_element(by=By.XPATH, value="//button[@type='submit']").click()

WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//p[text()[contains(.,'Congratulations')]]")))

driver.quit()
