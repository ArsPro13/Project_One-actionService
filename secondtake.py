from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.remote.webdriver import WebDriver
from time import sleep
import random
import codecs


with codecs.open("E:/test.txt", "r", "utf-8") as f:
    for line in f:
        drv = webdriver.Chrome()
        drv.get("https://google.ru/")
        sleep(1)
        onl = line[:-1] +' онлайн'
        dow = line[:-1] +' скачать'
        
        drv.find_element(By.XPATH,"/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input").send_keys(onl)
        drv.find_element(By.XPATH,"/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input").send_keys(Keys.ENTER)
        onl = 'e:\\'+ onl + '.png'
        drv.save_screenshot(onl)
        drv.close()
        
        drv2 = webdriver.Chrome()
        drv2.get("https://google.ru/")
        sleep(1)
        
        drv2.find_element(By.XPATH,"/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input").send_keys(dow)
        drv2.find_element(By.XPATH,"/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input").send_keys(Keys.ENTER)
        dow = 'e:\\'+ dow + '.png'
        drv.save_screenshot(dow)
        drv2.close()
