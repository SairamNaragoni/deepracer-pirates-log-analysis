#!/usr/bin/env python

# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 11:58:02 2020

@author: Rogue
"""
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
import time
import datetime
import getpass
import psutil
import yaml

def load_config():
    with open("config.yml", "r") as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as ex:
            print("Failed to load config file",ex)
        return config

def modal_dismissal(driver):
    try:
        modal_view = driver.find_element_by_class_name("awsui-modal-dismiss-control")
        print("modal overlay found...closing it")
        driver.execute_script("arguments[0].children[0].click();", modal_view)
    except:
        pass

def submit_to_race(driver, event, model):
    try:
        actionChains = ActionChains(driver)     
        driver.get(event)
        wait = WebDriverWait(driver, 120)
        # Wait till element is found and to click the race again button
        race_again_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']/span[text()='Race again']")))
        
        try:
            wait = WebDriverWait(driver, 5)
            model_name = wait.until(EC.presence_of_element_located((By.ID, "PLCHLDR_latest_model_name"))).text
            race_time = driver.find_element_by_id("PLCHLDR_latest_model_time").text
            # logs data as model,time
            log_data = model_name+" , "+race_time+"\n"
            log_file = open(log_file_name, "a")
            log_file.write(log_data)
            log_file.close()
        except Exception as e :
            print("Failed to log race times for the model - ",model,e)
        
        driver.execute_script("arguments[0].click();", race_again_button)
        time.sleep(1)
        modal_dismissal(driver)

        # Wait till element is found and click the dropdown
        #driver.execute_script("document.body.style.zoom='80%'")
        wait = WebDriverWait(driver, 60)
        dropdown = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@type='button']/span[text()='Choose a model']")))
        dropdown = dropdown.find_element_by_xpath("..")
        driver.execute_script("arguments[0].scrollIntoView();", dropdown)
        actionChains.move_to_element(dropdown).perform()
        driver.execute_script("arguments[0].click();", dropdown)
        dropdown.click()
        time.sleep(1)
    
        # Select the model
        selected_model = driver.find_element_by_xpath("//span[text()='"+model+"']")  
        selected_model.click()
        
        # Click Submit model
        submit_button = driver.find_element_by_xpath("//button[@type='submit']/span[text()='Enter race']")
        submit_button.find_element_by_xpath("..")
        driver.execute_script("arguments[0].click();", submit_button)       
    except Exception as e :
        print("Unable to submit to the race for the model - ",model,e)
        return      

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

def test_login(driver):
    base_url = "https://us-east-1.console.aws.amazon.com/deepracer/home?region=us-east-1#league"
    driver.get(base_url)
    time.sleep(2)
    if base_url != driver.current_url:
        raise Exception("Could not locate user login data !!")

def login_jp(driver,user_config,url):
    print("Redirecting to JPMC login page...")
    try:
        driver.get(url)
        driver.find_element_by_id("samAccountNameInput").send_keys(user_config['sid'])
        pwd = getpass.getpass()
        driver.find_element_by_id("passwordInput").send_keys(pwd)
        Select(driver.find_element_by_id("domainInput")).select_by_visible_text(user_config['domain'].upper())
        driver.find_element_by_id("submitButton").click()
        pwd = getpass.getpass(prompt="Passcode: ")
        driver.find_element_by_id("passcodeInput").send_keys(pwd)
        driver.find_element_by_id("submitButton").click()
        time.sleep(5)
        test_login(driver)
        print("Login successful !!")
    except Exception as error:
        print('Error while trying to login : ', error)

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


config = load_config()
timeout = config.get('timeout',400)
login_url = config['driver'].get('login_url','https://console.aws.amazon.com/')

itr=0
time_utc = str(int(time.time()));
log_file_name = "logRaceTimes-"+time_utc+".txt"

if config['driver'].get('type', 'mozilla') == 'mozilla':
    driver = init_mozilla_selenium(config['driver'])
else:
    driver = init_chrome_selenium(config['driver'])
    
try:
    try:
        test_login(driver)
    except Exception:
        login_jp(driver,config['user'],login_url)

    while True:
        try:
            test_login(driver)
        except Exception as e:
            print("Exiting process",e)
            break;
            
        log_file = open(log_file_name, "a")
        log_file.write("Running Iteration : "+ str(itr)+"\n")
        log_file.close()
        print("Running Iteration : ",itr)
        
        for key,value in config['submissions'].items():
            driver.get("https://google.co.in")
            if type(value['model'])==str:
                submit_to_race(driver, value['link'], value['model'])
            else:
                submit_to_race(driver, value['link'], value['model'][itr%len(value['model'])])
        
        time.sleep(1)
        print("Time : ",datetime.datetime.now().time(),", sleeping for ",round(timeout/60,2)," minutes")
        time.sleep(timeout)
        itr+=1
except Exception as e:
    print("Exception while running the script - ",e)
finally:
    print("Closing driver")
    kill_driver_process(driver)