# AutoMated Tools:
### Features
* The tool has support for Mozilla and Chrome only and runs on selenium. With the latest versions, both Mozilla and Chrome supports existing profile import in headless mode. 
* JPMC employees are advised to use [auto_submit_jpmc.py](https://github.com/SairamNaragoni/deepracer-pirates-log-analysis/blob/main/AutomatedTools/auto_submit_jpmc.py). Be it headless or not, you can login to AWS account from the terminal itself. 
* General public should provide profile info if they are using headless mode. In normal mode the script will timeout for 90sec by default for the user to enter login information if not already found.
* Refer to respective sample_config ymls for more information.

### Usage of Auto Submission Tool : 
* Install the required python packages by running `pip3 install -r requirements.txt`
* Download web drivers from https://chromedriver.chromium.org/ or https://github.com/mozilla/geckodriver/releases for your version of chrome or Mozilla. Add them the `Environment Path` or pass the webdriver location as `driver.path` in `config.yml`.
* If you provide profile info, log in to your AWS Account before starting the script and close the browser.
* You can find the profile info in similar locations as given in sample config files. In Chrome, you can find your profile by hitting `chrome://version` in your chrome browser.
* Define your race link/s(the one where you see the leaderboard for a given race) and model list under `submissions.<key>.*` (refer sample config file on how to). The script supports submissions to multiple races and multiple models to single race in succession.
* The Race Times for each model in each iteration are logged in `logRaceTimes-{timestamp}.txt`. (You can make it csv if you'd like by not printing the iteration number)

### Usage of Automated Deletion Tool :
* [deleteModels.py](https://github.com/SairamNaragoni/deepracer-pirates-log-analysis/blob/main/AutomatedTools/delete_models.py) helps in deleting all the models created in the account.
* Follow the same steps as stated above to configure selenium drivers.
* Deletion logs are recorded in the file `delete-{timestamp}.log`

### Full config reference :
<table>
  <tr>
    <td>Property</td>
    <td>Optional</td>
    <td>Default</td>
    <td>Description</td>
  </tr>
  <tr>
    <td>timeout</td>
    <td>Y</td>
    <td>360</td>
    <td>Time the script will sleep between each submission attempt.</td>
  </tr>
  <tr>
    <td>driver.login_url</td>
    <td>Y</td>
    <td>https://console.aws.amazon.com/</td>
    <td>Redirect URL if found that user is not logged in</td>
  </tr>
  <tr>
    <td>driver.type</td>
    <td>Y</td>
    <td>mozilla</td>
    <td>Which driver to use ? Either chrome or mozilla.</td>
  </tr>
  <tr>
    <td>driver.path</td>
    <td>Y</td>
    <td>None</td>
    <td>If the driver is not in Environment path, this property is a required field.</td>
  </tr>
  <tr>
    <td>driver.headless</td>
    <td>Y</td>
    <td>False</td>
    <td>If brower needs to run in headless mode or spawn window.</td>
  </tr>
  <tr>
    <td>driver.profile</td>
    <td>Y</td>
    <td>None</td>
    <td>In headless mode this property is a mandatory for general folks.</td>
  </tr>
  <tr>
    <td>submissions.{key}.link</td>
    <td>N</td>
    <td>None</td>
    <td>Race link for which you want to run the submissions</td>
  </tr>
  <tr>
    <td>submissions.{key}.model</td>
    <td>N</td>
    <td>None</td>
    <td>model/s which you want to submit in successions. Do not give comma separated values if you are providing a list. In case a list is provided, models will be submitted one after the other in round robin fasion</td>
  </tr>
  <tr>
    <td>user.sid</td>
    <td>Y</td>
    <td>None</td>
    <td>Required for JPMC employees</td>
  </tr>
  <tr>
    <td>user.domain</td>
    <td>Y</td>
    <td>None</td>
    <td>Required for JPMC employees</td>
  </tr>
</table>

```yml
timeout: 400
driver:
  login_url: 'https://console.aws.amazon.com/'
  type: chrome
  path: 'E:/WebDrivers/chromedriver.exe'
  headless: False
  profile: "C:/Users/narag/AppData/Local/Google/Chrome/User Data"
submissions:
  race1:
    link: "https://console.aws.amazon.com/deepracer/home?region=us-east-1#league/arn%3Aaws%3Adeepracer%3A%3A%3Aleaderboard%2F3f4f0e17-37eb-4363-bb9a-3bf1eafdc96b"
    model: "rogue-morgan-pro-OA-17"
  race2:
    link: "https://console.aws.amazon.com/deepracer/home?region=us-east-1#league/arn%3Aaws%3Adeepracer%3A%3A%3Aleaderboard%2F3f4f0e17-37eb-4363-bb9a-3bf1eafdc96b"
    model: 
      - "rogue-reinvent-OA-1"
      - "rogue-reinvent-OA-2"
```
