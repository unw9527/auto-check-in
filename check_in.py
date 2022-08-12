import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Checkin():
    def __init__(self, email, password, url):
        self.email = email
        self.password = password
        self.url = url
    
    def tnt_check(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get("https://www.google.com")
        driver.get(self.url)
        
        # login
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'email'))).send_keys(self.email)
        driver.find_element(By.ID, 'password').send_keys(self.password)
        driver.find_element(By.XPATH, '//*[@id="login-form"]/button').click()
        
        # click close button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="tos_notify"]/div/div/div/div/div/button'))).click()
        
        # click check in button
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'checkin'))).click()
            time.sleep(10)
        except:
            print('Has checked in today!')
        driver.quit()

if __name__ == '__main__':
    tnt_username = os.environ['TNT_USERNAME']
    tnt_password = os.environ['TNT_PASSWORD']
    tnt_url = os.environ['TNT_URL']
    Checkin(tnt_username, tnt_password, tnt_url).tnt_check()
    