# AutoSubmission Tool:
### Features
* The tool has support for Mozilla and Chrome only and runs on selenium. With the latest versions, both Mozilla and Chrome supports existing profile import in headless mode. 
* JPMC employees are advised to use [auto_submit_jpmc.py](https://github.com/SairamNaragoni/deepracer-pirates-log-analysis/blob/main/AutomatedTools/auto_submit_jpmc.py). Be it headless or not, you can login to AWS account from the terminal itself. 
* General public should provide profile info if they are using headless mode. In normal mode the script will timeout for 90sec by default for the user to enter login information if not already found.
* Refer to respective sample_config ymls for more information.

### Usage of Auto Submission Tool : 
* Install the required python packages by running `pip3 install -r requirements.txt`
* Download web drivers from https://chromedriver.chromium.org/ or https://github.com/mozilla/geckodriver/releases for your version of chrome or Mozilla. Add them the Environment Path or pass the webdriver location as `driver.path` in `config.yml`.
* If you provide profile info, log in to your AWS Account before starting the script and close the browser.
* You can find the profile info in similar locations as given in sample config files. In Chrome, you can find your profile by hitting `chrome://version` in your chrome browser.
* Define your race link/s(the one where you see the leaderboard for a given race) and model list under `submissions.<key>.*` (refer sample config file on how to). The script supports submissions to multiple races and multiple models to single race in succession.
* The Race Times for each model in each iteration are logged in `logRaceTimes-{timestamp}.txt`. (You can make it csv if you'd like by not printing the iteration number)

### Usage of Automated Deletion Tool :
* [deleteModels.py](https://github.com/SairamNaragoni/deepracer-pirates-log-analysis/blob/main/AutomatedTools/delete_models.py) helps in deleting all the models created in the account.
* Follow the same steps as stated above to configure selenium drivers.
* Deletion logs are recorded in the file `delete-{timestamp}.log`
