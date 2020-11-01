# deepracer-pirates-log-analysis
We built custom interactive graphs using plotly graphing library on top of basic log-analysis provided by the community

## Log Analysis Features
* Accommodated the new log folder structure that we download from console.
* Added entropy graph.
* Added graphs to provide insights on First 25% and last 25% of the training data (works with both simulation_agg and complete_ones dataframes).
* All the plotly functions are present in [`plotly_graph_utils.py`](https://github.com/SairamNaragoni/deepracer-pirates-log-analysis/blob/main/Notebooks/python/plotly_graph_utils.py). Feel free to make changes to according to your requirement.

## Track Generation from Waypoints
* Utility to generate new tracks using waypoints that deepracer provides

## Auto Submission Tools
* Use either [python file](https://github.com/SairamNaragoni/deepracer-pirates-log-analysis/blob/main/Auto%20Submission%20Tool/AutoSubmit.py) or the [notebook](https://github.com/SairamNaragoni/deepracer-pirates-log-analysis/blob/main/Notebooks/pirates_auto_submission.ipynb) to submit multiple models to multiple races.
