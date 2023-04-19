import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

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
        driver.get(self.url)
        
        # login
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'email'))).send_keys(self.email)
        driver.find_element(By.ID, 'password').send_keys(self.password)
        driver.find_element(By.XPATH, '/html/body/div[1]/section/div/div/div/div[2]/form/div/div[5]/button').click()
        
        # click close button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/div/div/div[3]/button'))).click()
        
        # click check in button
        try:
            WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn btn-icon icon-left btn-primary'))).click()
            time.sleep(10)
            print('Check in successfully!')
        except TimeoutException:
            if EC.element_to_be_clickable((By.CLASS_NAME, 'btn btn-icon disabled icon-left btn-primary')):
                print('Has already checked in today!')
            else:
                raise Exception('Check in failed!')
        driver.quit()

if __name__ == '__main__':
    tnt_username = os.environ['TNT_USERNAME']
    tnt_password = os.environ['TNT_PASSWORD']
    tnt_url = os.environ['TNT_URL']
    Checkin(tnt_username, tnt_password, tnt_url).tnt_check()
    
