# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 10:42:27 2021

@author: Rogue
"""
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import logging 
import time
import datetime
import yaml
import getpass
import psutil

def load_config():
    with open("config.yml", "r") as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as ex:
            print("Failed to load config file",ex)
        return config
    
def get_all_models(driver,models_url):
    models=[]
    try:
        log.info("Loading the models page ...")
        models=[]
        driver.get(models_url)
        # Wait until the page is completely loaded
        wait = WebDriverWait(driver, 300)
        wait.until(EC.presence_of_element_located((By.XPATH, "//li[@class='awsui-table-pagination-page-number']")))
        # Extract the last page number
        pagination = driver.find_elements_by_xpath("//li[@class='awsui-table-pagination-page-number']//button")
        max_page = int(pagination[len(pagination)-1].text)
        # Iterate through all the pages and store the name of the models
        log.info("Retrieving all models ...")
        for page in range(1,max_page+1):
            try:
                driver.find_element_by_xpath("//li[@class='awsui-table-pagination-page-number']//button[text()="+str(page)+"]").click()
                model_elements = driver.find_elements_by_xpath("//a[@data-analytics='model_list_to_model']")
                for element in model_elements:
                    models.append(element.text)
            except Exception as e:
                log.exception("Failed to retrieve models on page : %s \n%s",page,e)
        
        log.info("Total models found : %d",len(models))
    except Exception as e:
        log.exception("Failed to retrieve models \n%s",e)
        
    return models

def delete_model(driver,idx,model_name,model_base_url):
    try:
        # Load the model page, and delete the model
        model_url = model_base_url+model_name
        driver.get(model_url)
        wait = WebDriverWait(driver, 60)
        actions_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@awsui-button-region='text' and text()='Actions']")))
        actions_dropdown.click()
        driver.find_element_by_xpath("//li[@aria-label='Delete' and text()='Delete']").click()
        log.info("Deleting model : %s , index : %d",model_name,idx)
        driver.find_element_by_xpath("//span[@awsui-button-region='text' and text()='Delete']").click()
    except Exception as e:
        log.error("Failed to delete the model : %s \n%s",model_name,e)  

def init_chrome_selenium(driver_config):
    # Initializing selenium and chrome browser
    options = webdriver.ChromeOptions()
    options.headless = driver_config.get('headless',False)
    options.add_argument('--ignore-certificate-errors')
    if 'profile' in driver_config:
        options.add_argument("--user-data-dir="+driver_config.get('profile'))
    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    prefs = {"credentials_enable_service": False,
     "profile.password_manager_enabled": False}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(executable_path=driver_config.get('path','chromedriver'), options=options)
    driver.maximize_window()
    return driver  

def init_mozilla_selenium(driver_config):
    # Initializing selenium and mozilla browser
    options = Options()
    options.headless = driver_config.get('headless',False)
    fp = webdriver.FirefoxProfile(driver_config.get('profile',None))
    fp.set_preference("dom.disable_beforeunload", True)
    fp.set_preference("browser.tabs.warnOnClose", False)
    driver = webdriver.Firefox(fp,options=options,executable_path=driver_config.get('path','geckodriver'))
    driver.maximize_window()
    return driver

def sign_in(driver,login_url,timeout=90):
    print("Waiting %d seconds for Login ... \nPlease enter the Login info in the browser ..."%(timeout))
    driver.get(login_url)
    time.sleep(timeout)
    
def test_login(driver,login_url):
    base_url = "https://console.aws.amazon.com/deepracer/home?region=us-east-1#league"
    driver.get(base_url)
    time.sleep(2)
    if base_url != driver.current_url:
        raise Exception("Could not locate user login data !!")

def kill_driver_process(driver):
    driver_process = psutil.Process(driver.service.process.pid)
    if driver_process.is_running():
        browser_process = driver_process.children(recursive=True)
        if browser_process:
            browser_process = browser_process[0]
            if browser_process.is_running():
                print("driver is running, attempting to quit...")
                driver.quit()
            else:
                print("Let's kill the process")
                browser_process.kill()
        else:
            print("driver has died")

def init_logger():
    time_utc = str(int(time.time()));
    log_file = "delete-"+time_utc+".log"
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt='%H:%M:%S',
        handlers=[
            logging.FileHandler(log_file,"w"),
            logging.StreamHandler()
        ]
    )
    log=logging.getLogger() 
    log.setLevel(logging.INFO)
    return log

config = load_config()
timeout = config.get('timeout',360)
login_url = config['driver'].get('login_url','https://console.aws.amazon.com/')
log=init_logger()

# Constants
models_url="https://console.aws.amazon.com/deepracer/home?region=us-east-1#models"
model_base_url="https://console.aws.amazon.com/deepracer/home?region=us-east-1#model/"

if config['driver'].get('type', 'mozilla') == 'mozilla':
    driver = init_mozilla_selenium(config['driver'])
else:
    driver = init_chrome_selenium(config['driver'])

try:
    headless = config['driver'].get('headless',False)
    profile = config['driver'].get('profile',None)
    
    if headless == True and profile == None:
         raise Exception("Profile is needed in headless mode")
    
    try:
        test_login(driver,login_url)
    except Exception as e:
        if headless == True:
            raise e
        sign_in(driver,login_url)

    # Retrieve all the models
    models=get_all_models(driver, models_url)

    # Delete models one by one starting with the oldest
    for idx,model in reversed(list(enumerate(models))):
        delete_model(driver,idx,model,model_base_url)
        time.sleep(2)

except Exception as e:
    print("Exception while running the script - ",e)
finally:
    print("Closing driver")
    kill_driver_process(driver)
