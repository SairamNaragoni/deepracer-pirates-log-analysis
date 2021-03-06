# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 11:58:02 2020

@author: Rogue
"""
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import datetime
from selenium.webdriver import ActionChains
    
def submit_to_race(driver, event, model):
    try:
        actionChains = ActionChains(driver)     
        driver.get(event)

        try:
            wait = WebDriverWait(driver, 5)
            model_name = wait.until(EC.presence_of_element_located((By.ID, "PLCHLDR_latest_model_name"))).text
            race_time = driver.find_element_by_id("PLCHLDR_latest_model_time").text
            # logs data as model,time
            log_data = model_name+" , "+race_time+"\n"
            log_file = open("logRaceTimes.txt", "a")
            log_file.write(log_data)
            log_file.close()
        except Exception as e :
            print("Failed to log race times for the model - ",model,e)

        wait = WebDriverWait(driver, 60)
        # Wait till element is found and click the race again button
        race_again_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "awsui-button-variant-primary")))
        driver.execute_script("arguments[0].click();", race_again_button)
        
        # Wait till element is found and click the dropdown
        dropdown = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "awsui-select-keyboard-area")))
        actionChains.move_to_element(dropdown).perform()
        dropdown.click()
        time.sleep(1)
    
        # Select the model
        selected_model = driver.find_element_by_xpath("//span[@class='awsui-select-option-label' and text()='"+model+"']")
        selected_model.click()
        
        # Click Submit model
        submit_button = driver.find_element_by_class_name("awsui-button-variant-primary")
        driver.execute_script("arguments[0].click();", submit_button)       
    except Exception as e :
        print("Unable to submit to the race for the model - ",model,e)
        return     

# Initializing selenium and chrome browser
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--user-data-dir=C:/Users/Rogue/AppData/Local/Google/Chrome/User Data")
options.add_experimental_option("excludeSwitches", ['enable-automation']);
driver = webdriver.Chrome(executable_path="C:\\Users\\Rogue\\Downloads\\Compressed\\chromedriver", chrome_options=options)
driver.maximize_window()

# Give the race link here
fin_tech="give your race link here"

# Define the models you want to submit in succession.
model_list=["model1","model2"]

timeout=420
itr=0
while True:
    log_file = open("logRaceTimes.txt", "a")
    log_file.write("Running Iteration : "+ str(itr)+"\n")
    log_file.close()
    print("Running Iteration : ",itr)


    driver.get("https://google.co.in")
    submit_to_race(driver, fin_tech, model_list[itr%len(model_list)])
    
    # # Uncomment and configure to submit to more races 
    # driver.get("https://google.co.in")
    # submit_to_race(driver, fin_tech, model_list[itr%len(model_list)])
    
    time.sleep(1)
    print("Time : ",datetime.datetime.now().time(),", sleeping for ",round(timeout/60,2)," minutes")
    time.sleep(timeout)
    itr+=1
