


import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import numpy as np
from random import randint

import importlib





plt.rcParams['axes.grid'] = True


def creating_data_summary(df):
    """Create a datframe to display the most relevant data summary for the period
    """
    dataframe = pd.DataFrame(columns=['Question_1', 'Answer_1',"Answer_1.1", "Question_2", "Answer_2","Answer_2.1"])
    number_total_accidents = len(df.num_incident.unique())
    number_total_victims =df['num_victims'].sum()
    number_total_deaths = int(df['num_deaths'].sum())
    deaths_per_day = df.groupby(pd.Grouper(key='datetime', freq='D'))['num_deaths'].sum().sort_values(ascending=False)
    number_total_days = len(deaths_per_day)
    df['year'] = [int(x) for x in df['year']]
    
    for i in range(0,22):
        if i <13:
            
            dataframe.at[1, 'Question_1'] = "Total accidents: "
            dataframe.at[1, 'Answer_1'] = str(number_total_accidents)
            dataframe.at[2,'Question_1'] = "Total injuries: "
            dataframe.at[2,'Answer_1'] = str(number_total_victims)
            dataframe.at[3, 'Question_1'] = "Total deaths: "
            dataframe.at[3, 'Answer_1'] = str(number_total_deaths)
            dataframe.at[4, 'Question_1'] = 'Accidents per day:'
            dataframe.at[4, 'Answer_1']= round(number_total_accidents/number_total_days,2)
            dataframe.at[5, 'Question_1'] = 'Deaths per accident(100):'
            dataframe.at[5, 'Answer_1'] =round(number_total_deaths*100/number_total_accidents,2)
            dataframe.at[6, 'Question_1'] = "Injured per accident:"
            dataframe.at[6, 'Answer_1'] =round(number_total_victims/number_total_accidents,2)
            dataframe.at[7, 'Question_1'] = "Year with the highest number of accidents:"
            dataframe.at[7,'Answer_1'] = int(df.groupby('year')['num_incident'].count().sort_values(ascending=False).index[0])
            # dataframe.at[8, 'Question_1']='Accidents: '
            dataframe.at[7,'Answer_1.1'] =df.groupby('year')['num_incident'].count().sort_values(ascending=False).values[0]
            dataframe.at[8, 'Question_1'] = "Year with the highest number of injured:"
            dataframe.at[8,'Answer_1'] = int(df.groupby('year')['num_victims'].sum().sort_values(ascending=False).index[0])
            dataframe.at[8,'Answer_1.1'] =df.groupby('year')['num_victims'].sum().sort_values(ascending=False).values[0]
            dataframe.at[9,'Question_1'] = "Year with the highest number of deaths:"
            dataframe.at[9, 'Answer_1'] =int(df.groupby('year')['num_deaths'].sum().sort_values(ascending=False).index[0])
            dataframe.at[9,'Answer_1.1'] = int(df.groupby('year')['num_deaths'].sum().sort_values(ascending=False).values[0])
        else:
            dataframe.at[1, 'Question_2'] = "Month with the highest number of accidents:"
            dataframe.at[1, 'Answer_2'] = df.groupby(['month'])['num_incident'].count().sort_values(ascending=False).index[0]
           # dataframe.at[2, 'Question_2'] = 'Accidents:'
            dataframe.at[1,'Answer_2.1'] =int(df.groupby(['month'])['num_incident'].count().sort_values(ascending=False).values[0])
            
            dataframe.at[2, 'Question_2'] = "Month with the highest number of injured:"
            dataframe.at[2, 'Answer_2'] = df.groupby(['month'])['num_victims'].sum().sort_values(ascending=False).index[0]
            dataframe.at[2,'Answer_2.1'] =int(df.groupby(['month'])['num_victims'].sum().sort_values(ascending=False).values[0])
            dataframe.at[3, 'Question_2'] = "Month with the highest number of deaths:"
            dataframe.at[3, 'Answer_2'] = df.groupby(['month'])['num_deaths'].sum().sort_values(ascending=False).index[0]
            dataframe.at[3,'Answer_2.1'] =int(df.groupby(['month'])['num_deaths'].sum().sort_values(ascending=False).values[0])
            dataframe.at[4, 'Question_2'] = "Weekday with the highest number of accidents:"
            dataframe.at[4, 'Answer_2'] = df.groupby(['weekday'])['num_incident'].count().sort_values(ascending=False).index[0]
            dataframe.at[4,'Answer_2.1'] =int(df.groupby(['weekday'])['num_incident'].count().sort_values(ascending=False).values[0])
            dataframe.at[5, 'Question_2'] = "Weekday with the highest number of injured:"
            dataframe.at[5, 'Answer_2'] = df.groupby(['weekday'])['num_victims'].sum().sort_values(ascending=False).index[0]
            dataframe.at[5,'Answer_2.1'] =int(df.groupby(['weekday'])['num_victims'].sum().sort_values(ascending=False).values[0])
            dataframe.at[6, 'Question_2'] = "Weekday with the highest number of deaths:"
            dataframe.at[6, 'Answer_2'] = df.groupby(['weekday'])['num_deaths'].sum().sort_values(ascending=False).index[0]
            dataframe.at[6,'Answer_2.1'] =int(df.groupby(['weekday'])['num_deaths'].sum().sort_values(ascending=False).values[0])
            dataframe.at[7, 'Question_2'] = "Hour with the highest number of accidents:"
            dataframe.at[7, 'Answer_2'] = df.groupby(['hour'])['num_incident'].count().sort_values(ascending=False).index[0]
            dataframe.at[7,'Answer_2.1'] =int(df.groupby(['hour'])['num_incident'].count().sort_values(ascending=False).values[0])
            dataframe.at[8, 'Question_2'] = "Hour with the highest number of injured:"
            dataframe.at[8, 'Answer_2'] = df.groupby(['hour'])['num_victims'].sum().sort_values(ascending=False).index[0]
            dataframe.at[8,'Answer_2.1'] =int(df.groupby(['hour'])['num_victims'].sum().sort_values(ascending=False).values[0])
            dataframe.at[9, 'Question_2'] = "Hour with the highest number of deaths:"
            dataframe.at[9, 'Answer_2'] = df.groupby(['hour'])['num_deaths'].sum().sort_values(ascending=False).index[0]
            dataframe.at[9,'Answer_2.1'] =int(df.groupby(['weekday'])['num_deaths'].sum().sort_values(ascending=False).values[0])

    dataframe.fillna('',inplace=True)
    return dataframe

def set_of_colors(n):
    color = []
    for i in range(n):
        color.append('#%06X' % randint(0, 0xFFFFFF))    
    return color


def viz_per_time_period(df, time_period, period_list, chart_type='line'):
#weekdays_list=['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    period_groupby=df.groupby(time_period)[['num_incident','num_victims','num_deaths','target']].\
                        agg({'num_incident':'count',
                             'num_victims':'sum',
                             'num_deaths':'sum',
                             'target': 'sum',
                             
                                                                        }).reindex(period_list)
    
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(14, 4))
    sub_axis = (ax1, ax2, ax3, ax4)
    
    if chart_type =='line':
        ax1.plot(period_groupby.index,
                 period_groupby.iloc[:,0],
                 c='blue',
                 linewidth=2)
    elif chart_type=='bar':
        ax1.bar(period_groupby.index,
                period_groupby.iloc[:,0],
                color=set_of_colors(len(period_list)),
                linewidth=2)
    ax1.set_title(f'Accidents per {time_period}')
    if chart_type =='line':
        ax2.plot(period_groupby.index,
                 period_groupby.iloc[:,1],
                 color='#F29775',
                 linewidth=2)
    elif chart_type=='bar':
        ax2.bar(period_groupby.index,
                period_groupby.iloc[:,1],
                color=set_of_colors(len(period_list)),
                linewidth=2)
    ax2.set_title(f'Victims per {time_period}')
    if chart_type =='line':
        ax3.plot(period_groupby.index,
                 period_groupby.iloc[:,2],
                 color='#8B0000',
                 linewidth=2)
    elif chart_type =='bar':
        ax3.bar(period_groupby.index,
                period_groupby.iloc[:,2],
                color=set_of_colors(len(period_list)),
                linewidth=2)
    ax3.set_title(f'Deaths per {time_period}')
    if chart_type =='line':
        ax4.plot(period_groupby.index,
                 period_groupby.iloc[:,3],
                 color='#006400',
                 linewidth=2)
    elif chart_type =='bar':
        ax4.bar(period_groupby.index,
                period_groupby.iloc[:,3],
                color=set_of_colors(len(period_list)),
                linewidth=2)
    
    ax4.set_title(f'Target per {time_period}')
    for ax in sub_axis:
        if time_period == 'year':
            ax.set_xticks(np.arange(min(period_list), max(period_list) + 1, 5))
        elif time_period == 'hour':
            ax.set_xticks(np.arange(min(period_list), max(period_list) + 1, 6))
        elif time_period == 'month':
            ax.set_xticks(['Jan','','','Apr','','','Jul','','','Oct','','Dec'])
        else:
            ax.set_xticks(period_list)
    
    
    #Let's do it per collision:
    period_by_collision = (period_groupby.div(period_groupby['num_incident'], axis=0).iloc[:,1:])*100
    # period_by_collision=(period_groupby*(100/df.shape[0])).iloc[:,1:]

    fig, ax5 = plt.subplots(figsize=(12, 4))
    # Plot the first chart
    if chart_type == 'line':
        chart1 = ax5.plot(period_by_collision.index,
                          period_by_collision.iloc[:,0],
                          color='#F29775',
                          label='Victims per accident',linewidth=3)
    elif chart_type =='bar':
        chart1 = ax5.bar(period_by_collision.index,
                         period_by_collision.iloc[:,0], 
                         color=set_of_colors(len(period_list)),
                         label='Victims per accident',
                         linewidth=3)
    ax4.set_xlabel(time_period)
    ax4.set_ylabel('Victims per 100 Accidents')
    ax4.tick_params('y',labelcolor='#F29775')
    # Create a second axes that shares the same x-axis
    ax6 = ax5.twinx()
    
    # Plot the second chart
    if chart_type == 'line':
        chart2 = ax6.plot(period_by_collision.index,
                          period_by_collision.iloc[:,1],
                          color='#8B0000',
                          label='Deaths per 100 accident',
                          linewidth=3)
    elif chart_type =='bar':
        chart2 = ax6.bar(period_by_collision.index, 
                         period_by_collision.iloc[:,1],
                         color=set_of_colors(len(period_list)),
                         label='Deaths per accident',
                         linewidth=3)
    ax5.set_ylabel('Deaths per 100 Accidents' )
    ax5.tick_params('y',labelcolor = '#8B0000')
    ax5.grid(False)
    # Create a third axes that shares the same x-axis
    ax7 = ax5.twinx()
    
    # Plot the second chart
    if chart_type =='line':
        chart3 = ax7.plot(period_by_collision.index,
                          period_by_collision.iloc[:,2],
                          color='#006400',
                          label='Target per accident',
                          linewidth=5)
    elif chart_type == 'bar':
        chart3 = ax7.bar(period_by_collision.index,
                         period_by_collision.iloc[:,2],
                         color=set_of_colors(len(period_list)),
                         label='Target per accident',
                         linewidth=5)
    ax6.set_ylabel('Target per 100 Accidents' )
    ax6.tick_params('y',labelcolor = '#006400')
    ax6.grid(False)
    ax6.spines['right'].set_position(('outward', 60))
    
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    
    # Combine the handles and labels
    handles = handles1 + handles2
    labels = labels1 + labels2
    
    # Create a single legend for both axes
    plt.legend(handles, labels)
    
    
    # Show the plot
    plt.title('Combined Plot')
    #plt.grid(False)
    
    plt.show()
