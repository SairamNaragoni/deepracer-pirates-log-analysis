# deepracer-pirates-log-analysis :
We built custom interactive graphs using plotly graphing library on top of basic log-analysis provided by the community

## Log Analysis Features :
* Install the required python packages by running `pip3 install -r requirements.txt`
* Accommodated the new log folder structure that we download from console.
* Accomodated log-analysis for DRFC trainings with multiple robomakers streamed from cloud watch.
* Accomodated log-analysis for DRFC trainings with multiple robomakers inside the EC2 instance itself.
* For local and DRFC trainings, added **reward-progress distribution** over iterations as seen on deepracer console.
* Added entropy and surrogate loss graphs.
* Added graphs to provide insights on **First n% and Last n%** of the training data (works with both simulation_agg and complete_ones dataframes).
* All the plotly functions are present in [`plotly_graph_utils.py`](https://github.com/SairamNaragoni/deepracer-pirates-log-analysis/blob/main/Notebooks/python/plotly_graph_utils.py). Feel free to make changes to according to your requirement.
* Added **Custom Logging Feature**
* Added **Object Avoidance Plot**
* Added a function to view agent info, network info and hyperparameters
* The Notebook now supports analysis for the following algorithms :
  * PPO with Discrete Action Space (default)
  * PPO with Continuous Action Space
  * SAC with Continuous Action Space
#### Create Logs in DRFC :
* Use [`create_logs.sh`](https://github.com/SairamNaragoni/deepracer-pirates-log-analysis/blob/main/create_logs.sh) to flush the docker logs to the path defined in the script with the name LOG_DIR
* One can clone this repo in their EC2 and use jupyter notebook to run the log-analysis inside the EC2 itself.
* [Coming soon] Ability to get quick useful summary for the training duration on the ec2 terminal itself without having to launch jupyter notebook.

## Custom Logging :
`Ex : print("PIRATES_TRACE_LOG:%f;%f;%s;%s;%f" % (botx, boty, objects_location, objects_distance,reward_avoid))`
> Note : Please use delimiter as `;` since array logs are printed using `,`
* Add the print statement in your reward function for variables or arrays that are you would like to later analyse.
* Use a `logger-prefix` as shown in the example (not necessarily the same).
* In the [Training_analysis_with_custom_logging](https://github.com/SairamNaragoni/deepracer-pirates-log-analysis/blob/main/Notebooks/Training_analysis_with_custom_logging.ipynb) Notebook, configure the properties - `logger_prefix, custom_headers, array_headers`.
* The Notebook Auto detects the `data_type` of all the fields, with an exception of arrays. Hence you'll have specify the `array_headers` from `custom_headers` as shown in the Notebook so that they can be properly parsed.
* The given example in the Notebook is useful to plot objects on the track for log-analysis.
> Note : If you are logging too many custom arrays, it would increase the log-file size and also the time to parse the arrays. Disable `custom_config` when it is not necessary. (This was quickly developed before 2020 Championship Finals for OA and H2H analysis. Haven't found time to optimize it).

## Track Generation from Waypoints :
* A [Utility](https://github.com/SairamNaragoni/deepracer-pirates-log-analysis/blob/main/Notebooks/track_calculation_from_waypoints.ipynb) to generate new tracks using waypoints that deepracer provides.

## Automated Tools :
* Use either the [python file](https://github.com/SairamNaragoni/deepracer-pirates-log-analysis/blob/main/AutomatedTools/auto_submit.py) (preferred) or the [notebook](https://github.com/SairamNaragoni/deepracer-pirates-log-analysis/blob/main/Notebooks/pirates_auto_submission.ipynb) (outdated) to submit multiple models to multiple races.
* Refer to [Automated Tools Readme](https://github.com/SairamNaragoni/deepracer-pirates-log-analysis/tree/develop/AutomatedTools) for how to setup auto submission.

## References :
* [Basic Deepracer Notebook](https://github.com/aws-samples/aws-deepracer-workshops/tree/master/log-analysis)
* [RayG's Deepracer Analysis](https://github.com/TheRayG/deepracer-log-analysis)
