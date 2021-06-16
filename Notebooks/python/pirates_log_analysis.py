from datetime import datetime
from decimal import *

import numpy as np
import pandas as pd
import math
from io import StringIO
import ast
from python import log_analysis as la

def load_data(fname,custom_config):
    from os.path import isfile
    data = []

    i = 1
    while isfile('%s.%s' % (fname, i)):
        load_file('%s.%s' % (fname, i), data)
        i+=1

    if custom_config["custom_config"]:
        load_file(fname, data, custom_config["logger_prefix"])
    else:
        la.load_file(fname,data)

    print("Loaded %s log files (logs rolled over)" % i)

    return data


def load_file(fname, data, logger_prefix):
    try:
        with open(fname, 'r') as f:
            for line in f:
                if "PIRATES_TRACE_LOG" in line :
                    nextline = next(f) 
                    if "SIM_TRACE_LOG" in nextline:
                        pirate_parts = line.split(logger_prefix)[1].split('\t')[0]
                        sim_parts = nextline.split("SIM_TRACE_LOG:")[1].split('\t')[0].split(",")
                        sim_parts.append(pirate_parts)
                        data.append(",".join(sim_parts))
    except Exception as e:
        print("Exception Occured while Parsing !!",e)

def convert_to_pandas(data, custom_config, episodes_per_iteration=20):

    if custom_config["custom_config"] == False:
       return la.convert_to_pandas(data,episodes_per_iteration)
    custom_headers = custom_config['custom_headers']
    array_headers = custom_config['array_headers']

    """
    stdout_ = 'SIM_TRACE_LOG:%d,%d,%.4f,%.4f,%.4f,%.2f,%.2f,%d,%.4f,%s,%s,%.4f,%d,%.2f,%s\n' % (
            self.episodes, self.steps, model_location[0], model_location[1], model_heading,
            self.steering_angle,
            self.speed,
            self.action_taken,
            self.reward,
            self.done,
            all_wheels_on_track,
            current_progress,
            closest_waypoint_index,
            self.track_length,
            time.time())
        print(stdout_)
    """

    df_list = list()
    idx = 0
    # ignore the first two dummy values that coach throws at the start.
    for d in data[2:]:
        parts_workaround = 0
        d = d.split("\n,")
        parts = d[0].split(",")
        episode = int(parts[0])
        steps = int(parts[1])
        x = 100 * float(parts[2])
        y = 100 * float(parts[3])
        yaw = float(parts[4])
        steer = float(parts[5])
        throttle = float(parts[6])
        try:
            action = int(parts[7])
        except ValueError as e:
            action = -1
            parts_workaround = 1
        reward = float(parts[8+parts_workaround])
        done = 0 if 'False' in parts[9+parts_workaround] else 1
        all_wheels_on_track = parts[10+parts_workaround]
        progress = float(parts[11+parts_workaround])
        closest_waypoint = int(parts[12+parts_workaround])
        track_len = float(parts[13+parts_workaround])
        tstamp = Decimal(parts[14+parts_workaround])

        pirate_parts = d[1].rstrip()
        pirate_parts = StringIO(pirate_parts)
        converted_parts = np.genfromtxt(pirate_parts,dtype=None, encoding=None, delimiter=';',names = custom_headers)
        
        iteration = int(episode / episodes_per_iteration) + 1
        df_list.append([iteration, episode, steps, x, y, yaw, steer, throttle,
                        action, reward, done, all_wheels_on_track, progress,
                        closest_waypoint, track_len, tstamp])
        
        for entry in custom_headers:
            if entry in array_headers :
                conv_arr = ast.literal_eval(converted_parts[entry].tolist())
                df_list[idx].append(conv_arr)
            else :
                df_list[idx].append(converted_parts[entry].tolist())
        idx+=1
                
    df_list = tuple(df_list)
    header = ['iteration', 'episode', 'steps', 'x', 'y', 'yaw', 'steer',
              'throttle', 'action', 'reward', 'done', 'on_track', 'progress',
              'closest_waypoint', 'track_len', 'timestamp'] + custom_headers

    df = pd.DataFrame(df_list, columns=header)
    return df