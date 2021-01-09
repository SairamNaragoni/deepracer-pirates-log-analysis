# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 23:42:27 2021

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

def sign_in(driver,sign_in_url,timeout=90):
    log.info("Waiting %d seconds for Signin ... \nPlease enter the Signip info ...",timeout)
    driver.get(sign_in_url)
    time.sleep(timeout)
    
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

def delete_model(driver,idx,model_name):
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

def init_chrome_selenium():
    # Initializing selenium and chrome browser
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--user-data-dir=C:/Users/Rogue/AppData/Local/Google/Chrome/User Data")
    options.add_experimental_option("excludeSwitches", ['enable-automation']);
    driver = webdriver.Chrome(executable_path="C:\\Users\\Rogue\\Downloads\\Compressed\\chromedriver", chrome_options=options)
    driver.maximize_window()
    return driver  

def init_mozilla_selenium():
    # Initializing selenium and mozilla browser
    options = Options()
    options.headless = False
    profile = webdriver.FirefoxProfile('C:/Users/Rogue/AppData/Roaming/Mozilla/Firefox/Profiles/4ahj70v9.default-release')
    driver = webdriver.Firefox(profile,options=options,executable_path=r'C:/Users/Rogue/Downloads/WebDrivers/geckodriver.exe')
    driver.maximize_window()
    return driver

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

# driver=init_chrome_selenium()
driver=init_mozilla_selenium()
log=init_logger()

# Constants
models_url="https://console.aws.amazon.com/deepracer/home?region=us-east-1#models"
model_base_url="https://console.aws.amazon.com/deepracer/home?region=us-east-1#model/"

# In case you did not configure the user profile, add the sign in url and uncomment the sign_in() call
sign_in_url=""
# sign_in(driver, sign_in_url)

# Retrieve all the models
models=get_all_models(driver, models_url)

# Delete models one by one starting with the oldest
for idx,model in reversed(list(enumerate(models))):
    delete_model(driver,idx,model)
    time.sleep(2)