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
        time.sleep(4)
        
        model_name = driver.find_element_by_id("PLCHLDR_latest_model_name").text
        race_time = driver.find_element_by_id("PLCHLDR_latest_model_time").text
        
        # logs data as model,time
        log_data = model_name+" , "+race_time+"\n"
        log_file = open("logRaceTimes.txt", "a")
        log_file.write(log_data)
        log_file.close()
        race_again_button = driver.find_element_by_class_name("awsui-button-variant-primary")
        driver.execute_script("arguments[0].click();", race_again_button)
        
        # Wait till element is found and click the dropdown
        wait = WebDriverWait(driver, 60)
        dropdown = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "awsui-select-keyboard-area")))
        actionChains.move_to_element(dropdown).perform()
        dropdown.click()
        time.sleep(1)
    
        # Select the model
        selected_model = driver.find_element_by_xpath("//span[@class='awsui-select-option-label' and text()='"+model+"']")
        selected_model.click()
        
        #Click Submit model
        submit_button = driver.find_element_by_class_name("awsui-button-variant-primary")
        driver.execute_script("arguments[0].click();", submit_button)
        time.sleep(1)         
    except Exception as e :
        print("Unable to submit to the race for the model - ",model,e)
        return     
 
# Initializing selenium
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--user-data-dir=C:/Users/Rogue/AppData/Local/Google/Chrome/User Data")
driver = webdriver.Chrome(executable_path="C:\\Users\\Rogue\\Downloads\\Compressed\\chromedriver", chrome_options=options)
driver.maximize_window()

# Give the race link here
fin_tech="https://console.aws.amazon.com/deepracer/home?region=us-east-1#league/arn%3Aaws%3Adeepracer%3A%3A%3Aleaderboard%2F938a91be-226b-4a34-a401-69d75de8b5b4"

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
    # print("Running Iteration : ",itr)
    # driver.get("https://google.co.in")
    # submit_to_race(driver, fin_tech, model_list[itr%len(model_list)])
    
    time.sleep(1)   
    print("Time : ",datetime.datetime.now().time(),", sleeping for ",round(timeout/60,2)," minutes")
    time.sleep(timeout)
    itr+=1