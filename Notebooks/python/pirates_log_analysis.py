
from datetime import datetime
from decimal import *

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
from shapely.geometry.polygon import LineString
from sklearn.preprocessing import MinMaxScaler
import math


def load_data(fname):
    from os.path import isfile
    data = []

    i = 1
    while isfile('%s.%s' % (fname, i)):
        load_file('%s.%s' % (fname, i), data)
        i+=1

    load_file(fname, data)

    print("Loaded %s log files (logs rolled over)" % i)

    return data


def load_file(fname, data):
    with open(fname, 'r') as f:
        for line in f:
            if "PIRATES_TRACE_LOG" in line :
                nextline = next(f) 
                if "SIM_TRACE_LOG" in nextline:
                    pirate_parts = line.split("PIRATES_TRACE_LOG:")[1].split('\t')[0].split(",")
                    sim_parts = nextline.split("SIM_TRACE_LOG:")[1].split('\t')[0].split(",")
                    parts = np.concatenate((sim_parts,pirate_parts))
                    data.append(",".join(parts))
                    
                    
def convert_to_pandas(data, episodes_per_iteration=20):
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
    
    #arg1 = distance_from_optimal_race_line, 
    #arg2 = difference_direction_heading, 
    #arg3 = difference_speed,
    #arg4 = difference_time,
    #arg5 = closest_race_point,
    #arg6 = is_left_of_center,
    #arg7 = reward_dist
    #arg8 = reward_spd
    #arg9 = reward_dirc
    #arg10 = reward_time
    #arg11 = reward_prgs
    """

    df_list = list()

    # ignore the first two dummy values that coach throws at the start.
    for d in data[2:]:
        parts = d.rstrip().split(",")
        episode = int(parts[0])
        steps = int(parts[1])
        x = 100 * float(parts[2])
        y = 100 * float(parts[3])
        yaw = float(parts[4])
        steer = float(parts[5])
        throttle = float(parts[6])
        action = float(parts[7])
        reward = float(parts[8])
        done = 0 if 'False' in parts[9] else 1
        all_wheels_on_track = parts[10]
        progress = float(parts[11])
        closest_waypoint = int(parts[12])
        track_len = float(parts[13])
        tstamp = Decimal(parts[14])
        distance_from_optimal_race_line = float(parts[16])
        difference_direction_heading = float(parts[17])
        difference_speed =  float(parts[18])
        difference_time = float(parts[19])
        closest_race_point = int(parts[20])
        is_left_of_center = bool(parts[21])
        reward_dist =  float(parts[22])
        reward_spd =  float(parts[23])
        reward_dirc =  float(parts[24])
        reward_time =  float(parts[25])
        reward_prgs =  float(parts[26])
        
        

        iteration = int(episode / episodes_per_iteration) + 1
        df_list.append((iteration, episode, steps, x, y, yaw, steer, throttle,
                        action, reward, done, all_wheels_on_track, progress,
                        closest_waypoint, track_len, tstamp,
                        distance_from_optimal_race_line,difference_direction_heading,
                        difference_speed,difference_time,closest_race_point,
                        is_left_of_center,reward_dist,reward_spd,reward_dirc,reward_time,
                        reward_prgs))

    header = ['iteration', 'episode', 'steps', 'x', 'y', 'yaw', 'steer',
              'throttle', 'action', 'reward', 'done', 'on_track', 'progress',
              'closest_waypoint', 'track_len', 'timestamp',
              'dis_opt_line', 'diff_heading', 'diff_speed','diff_time','closest_point',
              'is_left','r_dist','r_spd','r_dirc','r_time','r_prgs']

    df = pd.DataFrame(df_list, columns=header)
    return df



def load_pirates_file(fname, data):
    with open(fname, 'r') as f:
        for line in f.readlines():
            if "PIRATES_TRACE_LOG" in line:
                parts = line.split("PIRATES_TRACE_LOG:")[1].split('\t')[0].split(",")
                data.append(",".join(parts))

                
                
def convert_to_pirates_pandas(data, episodes_per_iteration=20):

    df_list = list()
    # ignore the first two dummy values that coach throws at the start.
    for d in data:
        parts = d.rstrip().split(",")
        distance_from_optimal_race_line = float(parts[0])
        difference_direction_heading = float(parts[1])
        difference_speed =  float(parts[2])
        difference_time = float(parts[3])
        closest_race_point = int(parts[4])
        is_left_of_center = bool(parts[5])
        reward_dist =  float(parts[6])
        reward_spd =  float(parts[7])
        reward_dirc =  float(parts[8])
        reward_time =  float(parts[9])
        reward_prgs =  float(parts[10])
        df_list.append((distance_from_optimal_race_line,difference_direction_heading,
                        difference_speed,difference_time,closest_race_point,
                        is_left_of_center,reward_dist,reward_spd,reward_dirc,reward_time,
                        reward_prgs))
        header = ['dis_opt_line', 'diff_heading', 'diff_speed','diff_time','closest_point',
              'is_left','r_dist','r_spd','r_dirc','r_time','r_prgs']

    df = pd.DataFrame(df_list, columns=header)
    return df
    

def simulation_agg(panda, firstgroup='iteration', add_timestamp=False, is_eval=False):
    grouped = panda.groupby([firstgroup, 'episode'])

    by_steps = grouped['steps'].agg(np.max).reset_index()
    by_start = grouped.first()['closest_waypoint'].reset_index() \
        .rename(index=str, columns={"closest_waypoint": "start_at"})
    by_progress = grouped['progress'].agg(np.max).reset_index()
    by_throttle = grouped['throttle'].agg(np.mean).reset_index()
    by_time = grouped['timestamp'].agg(np.ptp).reset_index() \
        .rename(index=str, columns={"timestamp": "time"})
    by_time['time'] = by_time['time'].astype(float)
    result = by_steps \
        .merge(by_start) \
        .merge(by_progress, on=[firstgroup, 'episode']) \
        .merge(by_time, on=[firstgroup, 'episode'])

    if not is_eval:
        if 'new_reward' not in panda.columns:
            print('new reward not found, using reward as its values')
            panda['new_reward'] = panda['reward']
        by_new_reward = grouped['new_reward'].agg(np.sum).reset_index()
        result = result.merge(by_new_reward, on=[firstgroup, 'episode'])

    result = result.merge(by_throttle, on=[firstgroup, 'episode'])

    if not is_eval:
        by_reward = grouped['reward'].agg(np.sum).reset_index()
        result = result.merge(by_reward, on=[firstgroup, 'episode'])

    result['time_if_complete'] = result['time'] * 100 / result['progress']

    if not is_eval:
        result['reward_if_complete'] = result['reward'] * 100 / result['progress']
        result['quintile'] = pd.cut(result['episode'], 5, labels=['1st', '2nd', '3rd', '4th', '5th'])
    
    if add_timestamp:
        by_timestamp = grouped['timestamp'].agg(np.max).astype(float).reset_index()
        by_timestamp['timestamp'] = pd.to_datetime(by_timestamp['timestamp'], unit='s')
        result = result.merge(by_timestamp, on=[firstgroup, 'episode'])
    
    
    by_dis_opt_line = grouped['dis_opt_line'].agg(np.mean).reset_index()
    result = result.merge(by_dis_opt_line,on=[firstgroup, 'episode'])
    
    by_diff_heading = grouped['diff_heading'].agg(np.mean).reset_index()
    result = result.merge(by_diff_heading,on=[firstgroup, 'episode'])
    
    by_diff_speed = grouped['diff_speed'].agg(np.mean).reset_index()
    result = result.merge(by_diff_speed,on=[firstgroup, 'episode'])

    return result

def scatter_aggregates(aggregate_df, title=None, is_eval=False):
        
    fig, axes = plt.subplots(nrows= 5 , ncols=3, figsize=[17, 20])
    if title:
        fig.suptitle(title)

    aggregate_df.plot.scatter('time', 'reward', ax=axes[0, 2])
    aggregate_df.plot.scatter('time', 'new_reward', ax=axes[1, 2])
    aggregate_df.plot.scatter('start_at', 'reward', ax=axes[2, 2])
    aggregate_df.plot.scatter('start_at', 'progress', ax=axes[2, 0])
    aggregate_df.plot.scatter('start_at', 'time_if_complete', ax=axes[2, 1])
    aggregate_df.plot.scatter('time', 'progress', ax=axes[0, 0])
    aggregate_df.hist(column=['time'], bins=20, ax=axes[1, 0])
    aggregate_df.plot.scatter('time', 'steps', ax=axes[0, 1])
    aggregate_df.hist(column=['progress'], bins=20, ax=axes[1, 1])
    aggregate_df.plot.scatter('dis_opt_line','reward',ax=axes[3,0])
    aggregate_df.plot.scatter('diff_heading','reward',ax=axes[3,1])
    aggregate_df.plot.scatter('diff_speed','reward',ax=axes[3,2])
    aggregate_df.plot.scatter('dis_opt_line','new_reward',ax=axes[4,0])
    aggregate_df.plot.scatter('diff_heading','new_reward',ax=axes[4,1])
    aggregate_df.plot.scatter('diff_speed','new_reward',ax=axes[4,2])

    plt.show()
    plt.clf()
    
def scatter_complete_aggregates(aggregate_df, title=None, is_eval=False):
        
    fig, axes = plt.subplots(nrows= 7 , ncols=2, figsize=[15, 40])
    if title:
        fig.suptitle(title)
    aggregate_df.hist(column=['time'], bins=20, ax=axes[0, 0])
    aggregate_df.hist(column=['steps'], bins=20, ax=axes[0, 1])
    aggregate_df.plot.scatter('time', 'steps', ax=axes[1, 0])
    aggregate_df.plot.scatter('time', 'reward', ax=axes[1, 1])
    aggregate_df.plot.scatter('iteration', 'time', ax=axes[2, 0])
    aggregate_df.plot.scatter('iteration', 'steps', ax=axes[2, 1])
    aggregate_df.plot.scatter('iteration', 'reward', ax=axes[3, 1])
    aggregate_df.plot.scatter('iteration', 'dis_opt_line', ax=axes[3, 0])
    aggregate_df.plot.scatter('start_at', 'time', ax=axes[4, 0])
    aggregate_df.plot.scatter('start_at', 'reward', ax=axes[4, 1])
    aggregate_df.plot.scatter('start_at', 'steps', ax=axes[5, 0])
    aggregate_df.plot.scatter('dis_opt_line','reward',ax=axes[5,1])
    aggregate_df.plot.scatter('diff_heading','reward',ax=axes[6,0])
    aggregate_df.plot.scatter('diff_speed','reward',ax=axes[6,1])
    
    # aggregate_df.plot.scatter('time', 'new_reward', ax=axes[1, 2])
    # aggregate_df.plot.scatter('start_at', 'progress', ax=axes[2, 0])
    # aggregate_df.plot.scatter('time', 'progress', ax=axes[0, 0])
   

    

    # aggregate_df.plot.scatter('dis_opt_line','new_reward',ax=axes[4,0])
    # aggregate_df.plot.scatter('diff_heading','new_reward',ax=axes[4,1])
    # aggregate_df.plot.scatter('diff_speed','new_reward',ax=axes[4,2])

    plt.show()
    plt.clf()
    
def plot(ax, df, xval, xlabel, yval, ylabel, title=None):
    df.plot.scatter(xval, yval, ax=ax, s=5, alpha=0.7)
    if title:
        ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)

    plt.grid(True)
    
def analyze_closest_optimal_point(panda,title=None):
    add_new_reward = False
    if 'new_reward' in panda.columns:
        add_new_reward=True
    fig, axes = plt.subplots(nrows= 3, ncols=3, figsize=[17, 12])
    if title:
        fig.suptitle(title)
    panda.plot.scatter('closest_point','dis_opt_line',ax=axes[0,0])
    panda.plot.scatter('closest_point','diff_heading',ax=axes[0,1])
    panda.plot.scatter('closest_point','diff_speed',ax=axes[0,2])
    panda.plot.scatter('closest_point','reward',ax=axes[1,0])
    if add_new_reward :
        panda.plot.scatter('closest_point','new_reward',ax=axes[1,1])
    panda.plot.scatter('steer','closest_point',ax=axes[1,2])
    panda.plot.scatter('action','closest_point',ax=axes[2,0])
    panda.plot.scatter('throttle','closest_point',ax=axes[2,1])
    panda.plot.scatter('yaw','closest_point',ax=axes[2,2])

def analyze_categories(panda, category='quintile', groupcount=5, title=None):
    grouped = panda.groupby(category)
    fig, axes = plt.subplots(nrows=groupcount, ncols=4, figsize=[15, 15])

    if title:
        fig.suptitle(title)

    row = 0
    for name, group in grouped :
        if row<groupcount :
            group.plot.scatter('time', 'reward', ax=axes[row, 0])
            group.plot.scatter('time', 'new_reward', ax=axes[row, 1])
            group.hist(column=['time'], bins=20, ax=axes[row, 2])
            axes[row, 3].set(xlim=(0, 100))
            group.hist(column=['progress'], bins=20, ax=axes[row, 3])
        row += 1

    plt.show()
    plt.clf()

def get_heading(racing_track):
    headings=[]
    n=len(racing_track)
    for idx,point in enumerate(racing_track):
        track_direction = math.degrees(math.atan2(racing_track[(idx+1)%n][1]-point[1], racing_track[(idx+1)%n][0] - point[0]))
        headings.append(round(track_direction,2))
    return headings

def analyse_waypoints_agg(panda, ola, title=None):

    normalized_panda = panda.copy()
    optimal_speeds = [{"closest_point": i, "optimal_speed": val[0]} for i, val in enumerate(np.array(ola)[:, 2:3])]
    optimal_speeds = pd.DataFrame(optimal_speeds)

    complete_episodes = normalized_panda[normalized_panda['progress'] == 100]['episode']
    if len(complete_episodes) == 0:
        return
    normalized_panda = normalized_panda[normalized_panda['episode'].isin(complete_episodes)]

    grouped = normalized_panda.groupby('closest_point')

    by_dis_opt_line = grouped['dis_opt_line'].agg(np.mean).reset_index()
    by_diff_heading = grouped['diff_heading'].agg(np.mean).reset_index()
    by_diff_speed = grouped['diff_speed'].agg(np.mean).reset_index()
    by_x = grouped['x'].agg(np.mean).reset_index()
    by_y = grouped['y'].agg(np.mean).reset_index()
    by_speed = grouped['throttle'].agg(np.mean).reset_index()
    by_yaw = grouped['yaw'].agg(np.mean).reset_index()
    
    headings = get_heading(ola)
    headings = [{"closest_point": i, "heading": val} for i, val in enumerate(headings)]
    headings = pd.DataFrame(headings)
    
    result = by_dis_opt_line \
        .merge(by_diff_heading, on=['closest_point']) \
        .merge(by_diff_speed, on=['closest_point']) \
        .merge(by_x, on=['closest_point']) \
        .merge(by_y, on=['closest_point']) \
        .merge(by_speed, on=['closest_point']) \
        .merge(optimal_speeds, on=['closest_point']) \
        .merge(by_yaw,on=['closest_point']) \
        .merge(headings,on=['closest_point'])

    fig, axes = plt.subplots(nrows= 6, ncols=1, figsize=[25, 35])
    if title:
        fig.suptitle(title)

    result.plot.bar('closest_point', ['x', 'y'], ax=axes[0])
    result.plot.bar('closest_point', 'dis_opt_line', ax=axes[1])
    result.plot.bar('closest_point', 'diff_heading', ax=axes[2])
    result.plot.bar('closest_point', 'diff_speed', ax=axes[3])
    result.plot.bar('closest_point', ['throttle', 'optimal_speed'], ax=axes[4])
    result.plot.bar('closest_point', ['yaw', 'heading'], ax=axes[5])
    
    return result



def plot_coords(ax, ob):                                                        
    x, y = ob.xy                                                                
    ax.plot(x, y, '.', color='#999999', zorder=1)                               
                                                                                
def plot_bounds(ax, ob):                                                        
    x, y = zip(*list((p.x, p.y) for p in ob.boundary))                          
    ax.plot(x, y, '.', color='#000000', zorder=1)                               
                                                                                
def plot_line(ax, ob):                                                          
    x, y = ob.xy                                                                
    ax.plot(x, y, color='cyan', alpha=0.7, linewidth=3, solid_capstyle='round', zorder=2)
                                                                                
def print_border(ax, new_optimal_line, inner_border_waypoints, outer_border_waypoints):

    line = LineString(new_optimal_line)                                                
    plot_coords(ax, line)                                                       
    plot_line(ax, line)                                                       
                                                                                
    line = LineString(inner_border_waypoints)                                   
    plot_coords(ax, line)                                                       
    plot_line(ax, line)                                                         
                                                                                
    line = LineString(outer_border_waypoints)                                   
    plot_coords(ax, line)                                                       
    plot_line(ax, line)
    
    line = LineString(outer_border_waypoints)                                   
    plot_coords(ax, line)                                                       
    plot_line(ax, line)
    
def action_breakdown(df, iteration_ids, track_breakdown, center_line,
                     inner_border, outer_border,
                     action_names=['0', '1', '2', '3',
                                   '4', '5', '6', '7', 
                                   '8', '9', '10', '11', 
                                   '12', '13', '14', '15',
                                   '16', '17', '18', '19', '20']):
    fig = plt.figure(figsize=(16, 32))

    if type(iteration_ids) is not list:
        iteration_ids = [iteration_ids]

    wpts_array = center_line

    for iter_num in iteration_ids:
        # Slice the data frame to get all episodes in that iteration
        df_iter = df[(iter_num == df['iteration'])]
        n_steps_in_iter = len(df_iter)
        print('Number of steps in iteration=', n_steps_in_iter)
        th = 2.5
        for idx in range(len(action_names)):
            ax = fig.add_subplot(21, 2, 2 * idx + 1)
            print_border(ax, center_line, inner_border, outer_border)

            df_slice = df_iter[df_iter['reward'] >= th]
            df_slice = df_slice[df_slice['action'] == idx]

            ax.plot(df_slice['x'], df_slice['y'], 'b.')

            for idWp in track_breakdown.vert_lines:
                ax.text(wpts_array[idWp][0],
                        wpts_array[idWp][1] + 20,
                        str(idWp),
                        bbox=dict(facecolor='red', alpha=0.5))

            # ax.set_title(str(log_name_id) + '-' + str(iter_num) + ' w rew >= '+str(th))
            ax.set_ylabel(action_names[idx])

            # calculate action way point distribution
            action_waypoint_distribution = list()
            for idWp in range(len(wpts_array)):
                action_waypoint_distribution.append(
                    len(df_slice[df_slice['closest_waypoint'] == idWp]))

            ax = fig.add_subplot(21, 2, 2 * idx + 2)

            # Call function to create error boxes
            _ = make_error_boxes(ax,
                                 track_breakdown.segment_x,
                                 track_breakdown.segment_y,
                                 track_breakdown.segment_xerr,
                                 track_breakdown.segment_yerr)

            for tt in range(len(track_breakdown.track_segments)):
                ax.text(track_breakdown.track_segments[tt][0],
                        track_breakdown.track_segments[tt][1],
                        track_breakdown.track_segments[tt][2])

            ax.bar(np.arange(len(wpts_array)), action_waypoint_distribution)
            ax.set_xlabel('waypoint')
            ax.set_ylabel('# of actions')
            ax.legend([action_names[idx]])
            ax.set_ylim((0, 150))

    plt.show()
    plt.clf()


def parse_sagemaker_logs(sagemaker_log):
    trn_data = []
    last_iteration_id = 0
    with open(sagemaker_log, 'r') as f:
        for line in f.readlines():
            if "Training> Name=main_level/agent, " in line:
                parts = line.split("Training> Name=main_level/agent, ")[1].split('\t')[0].split('\n')[0].split(',')
                last_iteration_id = [parts[-1].split('=')[1]]
            if "Policy training> " in line:
                parts = line.split("Policy training> ")[1].split('\t')[0].split('\n')[0].split(',')
                parts = [x.split('=')[1] for x in parts]
                trn_data.append(",".join(last_iteration_id + parts))
    # Parse the policy training data
    df_list = list()
    
    for d in trn_data:
        parts = d.rstrip().split(",")
        iteration = int(parts[0]) + 1 # add 1 so as to match model.pb (training iteration n == model.pb n+1)
        surrogate_loss = float(parts[1])
        kl_divergence = float(parts[2])
        entropy = float(parts[3])
        training_epoch = int(parts[4]) + 1
        learning_rate = float(parts[5])
    
        df_list.append((iteration, surrogate_loss, kl_divergence, entropy, training_epoch, learning_rate))
    
    header = ['iteration', 'surrogate_loss', 'kl_divergence', 'entropy', 'training_epoch', 'learning_rate']
    trn_df = pd.DataFrame(df_list, columns=header)
    return trn_df
                
        



