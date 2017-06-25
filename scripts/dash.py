# called by the main.py not to be called directly 
import json
import plotly
import numpy as np
import config

# to communicate with Google BigQuery
from pandas.io import gbq
#time
from datetime import timedelta

# project details to be used when quering the database and calculating isStuck
# should be set to correct credentials and predictive analytics parameters must be set correctly

database = "["+config.PROJECT_ID+":"+config.BQ_PROCESSED_DATASET_ID+"."+config.BQ_PROCESSED_TABLE_ID+"]"
# sample query SELECT * FROM database WHERE player_id = 12345 LIMIT 100

# final result saved here
isStuckCounter = 0
isStoppedCounter = 0
isOngoingCounter = 0

funnelResults = []

# wrapper code for the predictive model
def plotStuck():
    query = "SELECT * FROM " +database+ " WHERE time >= \"" +str(config.isStuckDate)+ "\";"
    # Building the dataframe from the query
    stuckDf = gbq.read_gbq(query, project_id=config.PROJECT_ID)
    results = funnel(stuckDf, "player_id")
    return results

def funnel(df, columnName):
    # NOTE - not the actual method, just an example
    # sorting by the latest record first, required to calculate the progress
    all_id = df[columnName].unique()
    for an_id in all_id:
        each_df = df.loc[df[columnName] == an_id]
        isStuck(each_df)
        isStopped(each_df)
        isOngoing(each_df)
    return "results"

def isStuck(df):
    uniqueDates = df["time"].unique()[:config.isStuckDays]
    df.loc[df['time'].isin(uniqueDates)]
    if True not in df["passed"]:
        return "Player Stuck"
    
def isStopped(df):
    if config.currentDate - config.isStoppedDate > timedelta(days=config.isStoppedDays):
        return "Stopped Playing"
    
def isOngoing(df):
    uniqueDates = df["time"].unique()[:config.isOngoingDays]
    df.loc[df['time'].isin(uniqueDates)]
    if len(df["time"].unique()) > config.ongoingActivity:
        return "Still Playing"

def custom(query, X, Y):
    # building the query
    if(query == "Null"):
        graphs = dict(
                custom=[
                    dict(
                        # wrapper plot
                        x=np.random.normal(20, 0.25, 50),
                        y=np.random.normal(20, 0.25, 50),
                        type='histogram'
                    ),
                ],
                customLayout=dict(
                    title='Random Graph',
                    xaxis=dict(title='Random Values'),
                    yaxis=dict(title='Random Values'),
                    bargap=0.2,
                    bargroupgap=0.1
                )
            )
    else:
        # Building the dataframe from the query
        df = gbq.read_gbq(query, project_id=config.PROJECT_ID)

        graphs = dict(
                custom=[
                    dict(
                        x=df[X],
                        y=df[Y],
                    ),
                ],
                customLayout=dict(
                    title='Custom Graph',
                    xaxis=dict(title=X),
                    yaxis=dict(title=Y),
                    bargap=0.2,
                    bargroupgap=0.1
                )
            )

    # Convert the figures to JSON
    # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
    # objects to their JSON equivalents
    customJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    return customJSON 

def index():
    # getting results from stuck method
    stuckY = plotStuck()
    # plots for the player and the challenge page
    # plotly counts automatically to create the plot
    graphs = [
        dict(
            player=[
                dict(
                    # wrapper plots
                    x=np.random.normal(10, 0.1, 500),
                    type='histogram'
                ),
            ],
            playerLayout=dict(
                title='Player Vs. Challenge',
                xaxis=dict(title='Challenge Level'),
                yaxis=dict(title='No. of Players'),
                bargap=0.2,
                bargroupgap=0.1
            )
        ),
        dict(
            challenge=[
                dict(
                    # wrapper plots
                    x=np.random.normal(5, 0.05, 500),
                    type='histogram'
                ),
            ],
            challengeLayout=dict(
                title='Failure Vs. Challenge',
                xaxis=dict(title='Challenge Level'),
                yaxis=dict(title='No. of Failures'),
                bargap=0.2,
                bargroupgap=0.1
            )
        ),
        dict(
            stuck=[
                dict(
                    # wrapper plot
                    x=stuckY,
                    type='histogram'
                ),
            ],
            stuckLayout=dict(
                title='Players Stuck',
                xaxis=dict(title='Number of players'),
                yaxis=dict(title='Status'),
                bargap=0.2,
                bargroupgap=0.1
            )
        )
    ]

    # Convert the figures to JSON
    # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
    # objects to their JSON equivalents
    staticJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return staticJSON
