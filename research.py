from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.remote.webdriver import WebDriver
from time import sleep

def attach_to_session(executor_url, session_id):
    original_execute = WebDriver.execute
    def new_command_execute(self, command, params=None):
        if command == "newSession":
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return original_execute(self, command, params)
    WebDriver.execute = new_command_execute
    driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
    driver.session_id = session_id
    WebDriver.execute = original_execute
    return driver


   

    
maxdepth=4

def Fill(dictionary,val,num,u,i,depth):
    if ((val in dictionary.keys()) or (depth >= maxdepth)):
        return;
    dictionary[val]=num   
    drv = attach_to_session(u, i)
    drv.get("https://wordstat.yandex.ru/")
    window = "/html/body/div[1]/table/tbody/tr/td[4]/div/div/form/table/tbody/tr[1]/td[1]/span/span/input"
    window_control = drv.find_element(By.XPATH, window)
    button = "/html/body/div[1]/table/tbody/tr/td[4]/div/div/form/table/tbody/tr[1]/td[2]/span/input"
    button_control = drv.find_element(By.XPATH, button)
    window_control.send_keys(val)
    button_control.click()
    s1 = "null"
    s2 = "null"
    s3 = "null"
    s4 = "null"
    s1val = "null"
    s2val = "null"
    s3val = "null"
    s4val = "null"
    sleep(10)
    
                                    
    if (drv.find_elements(By.XPATH, "/html/body/div[2]/div/div/table/tbody/tr/td[4]/div/div/div[2]/div[1]/div/table/tbody/tr[2]/td[1]/span")):
        s1    = drv.find_element(By.XPATH, "/html/body/div[2]/div/div/table/tbody/tr/td[4]/div/div/div[2]/div[1]/div/table/tbody/tr[2]/td[1]/span").text
        s1val = drv.find_element(By.XPATH, "/html/body/div[2]/div/div/table/tbody/tr/td[4]/div/div/div[2]/div[1]/div/table/tbody/tr[2]/td[2]")
        s1val = s1val.text
        
    if (drv.find_elements(By.XPATH, "/html/body/div[2]/div/div/table/tbody/tr/td[4]/div/div/div[2]/div[1]/div/table/tbody/tr[3]/td[1]/span/a")):    
        s2    = drv.find_element(By.XPATH, "/html/body/div[2]/div/div/table/tbody/tr/td[4]/div/div/div[2]/div[1]/div/table/tbody/tr[3]/td[1]").text
        s2val = drv.find_element(By.XPATH, "/html/body/div[2]/div/div/table/tbody/tr/td[4]/div/div/div[2]/div[1]/div/table/tbody/tr[3]/td[2]")
        s2val = s2val.text
        
    if (drv.find_elements(By.XPATH, "/html/body/div[2]/div/div/table/tbody/tr/td[4]/div/div/div[2]/div[2]/div/table/tbody/tr[2]/td[1]/span/a")):    
        s3    = drv.find_element(By.XPATH, "/html/body/div[2]/div/div/table/tbody/tr/td[4]/div/div/div[2]/div[2]/div/table/tbody/tr[2]/td[1]").text
        s3val = drv.find_element(By.XPATH, "/html/body/div[2]/div/div/table/tbody/tr/td[4]/div/div/div[2]/div[2]/div/table/tbody/tr[2]/td[2]")
        s3val = s3val.text

    if (drv.find_elements(By.XPATH, "/html/body/div[2]/div/div/table/tbody/tr/td[4]/div/div/div[2]/div[2]/div/table/tbody/tr[3]/td[1]")):    
        s4    = drv.find_element(By.XPATH, "/html/body/div[2]/div/div/table/tbody/tr/td[4]/div/div/div[2]/div[2]/div/table/tbody/tr[3]/td[1]").text
        s4val = drv.find_element(By.XPATH, "/html/body/div[2]/div/div/table/tbody/tr/td[4]/div/div/div[2]/div[2]/div/table/tbody/tr[3]/td[2]")
        s4val = s4val.text
        
    if (s1!="null"):
        Fill(dictionary,s1,s1val,u,i,depth+1)
    if (s2!="null"):
        Fill(dictionary,s2,s2val,u,i,depth+1)
    if (s3!="null"):
        Fill(dictionary,s3,s3val,u,i,depth+1)
    if (s4!="null"):
        Fill(dictionary,s4,s4val,u,i,depth+1)
    
driver = webdriver.Chrome()
driver.get("https://wordstat.yandex.ru/")
u,i = driver.command_executor._url,driver.session_id
q = input()
dictionary = {}

Fill(dictionary,"калькулятор",'17 578 683',u,i,0)

print(dictionary)
