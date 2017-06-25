# config parmeters for modules of the app

#time
from datetime import datetime, timedelta

# Google Cloud Platform details 
PROJECT_ID = "project id goes here"
BQ_RAW_DATASET_ID = "raw dataset id goes here"
BQ_RAW_TABLE_ID = "raw table id goes here"
BQ_PROCESSED_DATASET_ID = "processed dataset id goes here"
BQ_PROCESSED_TABLE_ID = "processed table id goes here"


# predefined number of days for the predictive analytics
isStuckDays = 0 # number of days after which the player is classified as stuck
isStoppedDays = 0 # number of days after which the player is classified as stopped
# threshold for classifying progress - x number of activities in past y days is progressing
isOngoingDays = 0 #  number of days to calculate progress
ongoingActivity = 0 # number of activities in past isOngoingDays to classify as ongoing


# dates for calculating the progress of the players
# today's date
f = '%Y-%m-%d %H:%M:%S'
currentDate = datetime.now().strftime(f)
currentDate = datetime.strptime(currentDate, f)

# converting days to dates 
isStuckDate = currentDate - timedelta(days=isStuckDays)
isStuckDate.strftime(f)

isStoppedDate = currentDate - timedelta(days=isStoppedDays)
isStoppedDate.strftime(f)

isOngoingDate = currentDate - timedelta(days=isOngoingDays)
isOngoingDate.strftime(f)