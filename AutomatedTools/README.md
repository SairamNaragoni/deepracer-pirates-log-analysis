# AutoMated Tool:
### Usage of Auto Submission Tool : 
* The tool has a support for Mozilla and Chrome only and runs on selenium. With the latest versions, both Mozilla and Chrome supports existing profile import in headless mode. 
* Install the python packages by running `pip3 install -r requirements.txt`
* Download web drivers from https://chromedriver.chromium.org/ or https://github.com/mozilla/geckodriver/releases for your version of chrome or Mozilla. Add them to either any of the directory which is in Environment Path or pass the path as `driver.path` in `config.yml`.
* Log in to your AWS Account and close the browser.
* Replace the below variables in the script (Similar process for Mozilla):
  1. The first argument points to the Default profile in chrome. You can find yours by hitting `chrome://version` in your chrome browser.
  2. The second argument is the path to the chrome driver.  
  `options.add_argument("--user-data-dir=C:/Users/Rogue/AppData/Local/Google/Chrome/User Data")`
  `webdriver.Chrome(executable_path="C:\\Users\\Rogue\\Downloads\\Compressed\\chromedriver", chrome_options=options)`
* Define your race link/s and model list(refer script on how to). The script supports submissions to multiple races and multiple models to single race in succession.
* The Race Times for each model in each iteration are logged in `logRaceTimes-{timestamp}.txt`. (You can make it csv if you'd like by not printing the iteration number)

### Usage of Automated Deletion Tool :
* [deleteModels.py](https://github.com/SairamNaragoni/deepracer-pirates-log-analysis/blob/main/Automated%20Tools/deleteModels.py) helps in deleting all the models created in the account.
* Configure the selenium driver for mozilla firefox - `init_mozilla_selenium()` or google chrome - `init_chrome_selenium()` in the python file as stated above and run the script.
* Deletion logs are recorded in the file `delete-{timestamp}.log`

## References :
* [Basic Deepracer Notebook](https://github.com/aws-samples/aws-deepracer-workshops/tree/master/log-analysis)
* [RayG's Deepracer Analysis](https://github.com/TheRayG/deepracer-log-analysis)
