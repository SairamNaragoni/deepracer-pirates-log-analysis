import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
from python import track_utils as tu
import math

def toCms(x):
    return x*100

def get_headings(racing_track):
    headings=[]
    n=len(racing_track)
    for idx,point in enumerate(racing_track):
        track_direction = math.degrees(math.atan2(racing_track[(idx+1)%n][1]-point[1], racing_track[(idx+1)%n][0] - point[0]))
        headings.append(round(track_direction,2))
    return headings

def draw_track_plotly(fig,track_name, center_line=True):
    borderColor = 'rgb(189,189,189)'
    optLineColor = 'rgb(139,195,74)'
    l_center_line,l_inner_border,l_outer_border,road_poly=tu.load_track(track_name,"../")
    headings = get_headings(l_center_line.tolist())
    if center_line :
        fig.add_trace(go.Scatter(x= l_center_line[:,0], y= l_center_line[:,1],
                        mode='lines',
                        line=dict(color=borderColor),
                        name='center_line',showlegend = False,
                        hovertemplate =
                            '<b>%{text}</b>',
                        text = ['{}'.format([idx,heading]) for idx,heading in enumerate(headings)]))
    fig.add_trace(go.Scatter(x= l_inner_border[:,0], y= l_inner_border[:,1],
                        mode='lines+markers',
                        line=dict(color=borderColor),
                        name='inner_border',showlegend = False))
    fig.add_trace(go.Scatter(x= l_outer_border[:,0], y= l_outer_border[:,1],
                        mode='lines+markers',
                        line=dict(color=borderColor),
                        name='outer_border',
                        showlegend = False))

def plot_episode(episode_data,plotly_config):
    fig = go.Figure()
    fig=px.scatter(episode_data,x="x",y="y",color='throttle',
                          hover_data={'throttle' : True,'yaw':True,'x':True,'y':True,'steer':True,'reward':True,'closest_waypoint':True,
                          "steps":True})
    fig.update_layout(width=plotly_config["width"],height=plotly_config["height"])
    draw_track_plotly(fig,plotly_config['track_name'])
    fig.show()

def plot_multiple_laps(df,episode_df,plotly_config,time_start=8,time_end=9,is_complete=True):      
	fig = go.Figure()
	episode_df = episode_df[ (episode_df['time'] >= time_start) & (episode_df['time'] <= time_end)]
	if is_complete == False :
	    episode_df = episode_df[ episode_df['progress'] != 100 ]
	    
	for idx, entry in episode_df.iterrows():
	    episode_no = entry['episode']
	    episode_data = df[df['episode'] == episode_no]
	    reward_arr = episode_data['reward'].tolist()
	    speed_arr = episode_data['throttle'].tolist()
	    hover_arr = [list(x) for x in zip(reward_arr, speed_arr)]
	    fig.add_trace(go.Scatter(x=episode_data['x'],y=episode_data['y'],
	                            mode='markers',
	                            marker=dict(size=4,color = reward_arr),
	                            hovertemplate =
	                                '<b>%{text}</b>',
	                            text = ['{}'.format([ entry[0],entry[1] ]) for entry in hover_arr],
	                            name="ep : "+str(episode_no)))
	fig.update_layout(width=plotly_config["width"],height=plotly_config["height"])	
	draw_track_plotly(fig,plotly_config['track_name'])
	fig.show()

def plot_time_hist(df):
	if len(df) == 0:
		print("No complete laps yet.")
		return  
	fig = go.Figure()
	fig = px.histogram(df, x="time", marginal="rug",
	                   hover_data={'time' : True, 'steps':True, 'iteration':True, 'episode':True, 'start_at':True, 'reward':True, 'quintile':True})
	# fig = px.histogram(df,x = "time")
	fig.update_layout(height=600, width=970, title_text="Time Histogram for complete laps")
	fig.update_xaxes(showgrid=True)
	fig.show()

def plot_complete_lap_analysis(df):
	if len(df) == 0:
		print("No complete laps yet.")
		return  
	fig = go.Figure()
	fig = make_subplots(rows=3, cols=2,subplot_titles=("Time", "Steps", "Time-Steps", "Time-Reward","Start_at-Time","Start_at-Reward"))
	fig.add_trace(
	    go.Histogram(x=df['time'] ,showlegend = False),
	    row=1, col=1
	)
	fig.add_trace(
	    go.Histogram(x=df['steps'] ,showlegend = False),
	    row=1, col=2
	)
	fig.add_trace(
	    go.Scatter(x=df['time'] ,y=df['steps'] , mode="markers",showlegend = False),
	    row=2, col=1
	)
	fig.add_trace(
	    go.Scatter(x=df['time'] ,y=df['reward'] ,mode="markers",showlegend = False),
	    row=2, col=2
	)
	fig.add_trace(
	    go.Scatter(x=df['start_at'] ,y=df['time'] , mode="markers",showlegend = False),
	    row=3, col=1
	)
	fig.add_trace(
	    go.Scatter(x=df['start_at'] ,y=df['reward'] , mode="markers",showlegend = False),
	    row=3, col=2
	)
	fig.update_layout(height=1600, width=980, title_text="Complete Laps Analysis")
	fig.show()

def get_bin_size(plot_type):
	bin_size = 0.0
	if plot_type == "time" :
		bin_size = 0.1


def plot_distribution(df,column = "steps",percent = 25):
	if len(df) == 0:
		print("No complete laps yet.")
		return  
	df_copy = df.copy()
	size = len(df_copy)
	bin_size = get_bin_size(column)
	percent_count = round(size*(percent/100))
	fig = go.Figure()
	fig.add_trace(go.Histogram(x=df_copy[column].iloc[0:percent_count] , name="First "+str(percent)+"%",xbins=dict(size=bin_size)))
	fig.add_trace(go.Histogram(x=df_copy[column].iloc[(size-percent_count):size] , name="Last "+str(percent)+"%",xbins=dict(size=bin_size)))
	fig.update_layout(height=600, width=970,title = column+" distribution in first and last "+ str(percent)+"%",barmode='overlay')
	fig.update_traces(opacity=0.65)
	fig.show()

def plot_reward_distribution(df,percent=25):
	if len(df) == 0:
		print("No complete laps yet.")
		return  
	df_copy = df.copy()
	size = len(df_copy)
	percent_count = round(size*(percent/100))
	fig = go.Figure()
	fig.add_trace(go.Histogram(x=df_copy['reward'].round().iloc[0:percent_count] , name="First "+str(percent)+"%"))
	fig.add_trace(go.Histogram(x=df_copy['reward'].round().iloc[(size-percent_count):size] , name = "Last "+str(percent)+"%"))
	fig.update_layout(title = "Reward Distribution in first and last "+ str(percent)+"%", barmode='overlay')
	fig.update_traces(opacity=0.65)
	fig.show()

def plot_reward_hist(df):
	df_copy = df.copy()	
	fig = go.Figure()
	fig = px.histogram(df_copy['reward'].round(),x = "reward")
	fig.update_xaxes(showgrid=True)
	fig.show()

def plot_training_metrics(df, column="entropy"):
	fig = go.Figure()
	fig = make_subplots(specs=[[{"secondary_y": True}]])
	fig.add_trace(go.Scatter(x=df['iteration'], y=df[column],
	                    mode='lines',name=column,line=dict({'shape': 'spline', 'smoothing': 1.3})),secondary_y=False,)
	fig.show()
