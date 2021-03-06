# deepracer-pirates-log-analysis
We built custom interactive graphs using plotly graphing library on top of basic log-analysis provided by the community

## Log Analysis Features
* Accommodated the new log folder structure that we download from console.
* Accomodated log-analysis for DRFC trainings with multiple robomakers streamed from cloud watch.
* Accomodated log-analysis for DRFC trainings with multiple robomakers inside the EC2 instance itself.
* For local and DRFC trainings, added **reward-progress distribution** over iterations as seen on deepracer console.
* Added entropy and surrogate loss graphs.
* Added graphs to provide insights on **First n% and Last n%** of the training data (works with both simulation_agg and complete_ones dataframes).
* All the plotly functions are present in [`plotly_graph_utils.py`](https://github.com/SairamNaragoni/deepracer-pirates-log-analysis/blob/main/Notebooks/python/plotly_graph_utils.py). Feel free to make changes to according to your requirement.
* Added **Custom Logging Feature**
* Added **Object Avoidance Plot**

## Custom Logging  
`Ex : print("PIRATES_TRACE_LOG:%f;%f;%s;%s;%f" % (botx, boty, objects_location, objects_distance,reward_avoid))`
> Note : Please use delimiter as `;` since array logs are printed using `,`
* Add the print statement in your reward function for variables or arrays that are you would like to later analyse.
* Use a `logger-prefix` as shown in the example (not necessarily the same).
* In the [Training_analysis_with_custom_logging](https://github.com/SairamNaragoni/deepracer-pirates-log-analysis/blob/main/Notebooks/Training_analysis_with_custom_logging.ipynb) Notebook, configure the properties - `logger_prefix, custom_headers, array_headers`.
* The Notebook Auto detects the `data_type` of all the fields, with an exception of arrays. Hence you'll have specify the `array_headers` from `custom_headers` as shown in the Notebook so that they can be properly parsed.
* The given example in the Notebook is useful to plot objects on the track for log-analysis.
> Note : If you are log too many custom arrays, it would increase the log-file size and also the time to parse the arrays. Disable `custom_config` when it is not necessary.

## Track Generation from Waypoints
* A [Utility](https://github.com/SairamNaragoni/deepracer-pirates-log-analysis/blob/main/Notebooks/track_calculation_from_waypoints.ipynb) to generate new tracks using waypoints that deepracer provides.

## Automated Tools
* Use either the [python file](https://github.com/SairamNaragoni/deepracer-pirates-log-analysis/blob/main/Auto%20Submission%20Tool/AutoSubmit.py) (preferred) or the [notebook](https://github.com/SairamNaragoni/deepracer-pirates-log-analysis/blob/main/Notebooks/pirates_auto_submission.ipynb) to submit multiple models to multiple races.
### Usage of Auto Submission Tool : 
* The tool runs on mozilla firefox - `init_mozilla_selenium()` or google chrome - `init_chrome_selenium()` using selenium. *(Mozilla - runs in headless)*
* Download web driver from https://chromedriver.chromium.org/ for your version of chrome or geckodriver for Mozilla.
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
