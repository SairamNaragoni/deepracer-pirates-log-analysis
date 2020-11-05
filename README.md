# deepracer-pirates-log-analysis
We built custom interactive graphs using plotly graphing library on top of basic log-analysis provided by the community

## Log Analysis Features
* Accommodated the new log folder structure that we download from console.
* Added entropy graph.
* Added graphs to provide insights on First 25% and last 25% of the training data (works with both simulation_agg and complete_ones dataframes).
* All the plotly functions are present in [`plotly_graph_utils.py`](https://github.com/SairamNaragoni/deepracer-pirates-log-analysis/blob/main/Notebooks/python/plotly_graph_utils.py). Feel free to make changes to according to your requirement.

## Track Generation from Waypoints
* A [Utility](https://github.com/SairamNaragoni/deepracer-pirates-log-analysis/blob/main/Notebooks/track_calculation_from_waypoints.ipynb) to generate new tracks using waypoints that deepracer provides.

## Auto Submission Tools
* Use either the [python file](https://github.com/SairamNaragoni/deepracer-pirates-log-analysis/blob/main/Auto%20Submission%20Tool/AutoSubmit.py) or the [notebook](https://github.com/SairamNaragoni/deepracer-pirates-log-analysis/blob/main/Notebooks/pirates_auto_submission.ipynb) to submit multiple models to multiple races.
### Usage of Auto Submission Tool : 
* The tool runs on google chrome using selenium.
* Download chrome driver from https://chromedriver.chromium.org/ for your version of chrome.
* Log in to your AWS Account on chrome and close the browser.
* Replace the below variables in the script :
  1. The first argument points to the Default profile in chrome. You can find yours by hitting `chrome://version` in your chrome browser.
  2. The second argument is the path to the chrome driver.  
  `options.add_argument("--user-data-dir=C:/Users/Rogue/AppData/Local/Google/Chrome/User Data")`
  `webdriver.Chrome(executable_path="C:\\Users\\Rogue\\Downloads\\Compressed\\chromedriver", chrome_options=options)`
* Define your race link/s and model list(refer script on how to). The script supports submissions to multiple races and multiple models to single race in succession.
* The Race Times for each model in each iteration are logged in `logRaceTimes.txt`. (You can make it csv if you'd like by not printing the iteration number)

## References :
* [Basic Deepracer Notebook](https://github.com/aws-samples/aws-deepracer-workshops/tree/master/log-analysis)
* [RayG's Deepracer Analysis](https://github.com/TheRayG/deepracer-log-analysis)
