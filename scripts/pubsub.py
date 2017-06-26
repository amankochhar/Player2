# requirement - google-cloud-pubsub==0.25.0
# example code for the pubsub messages to bigquery table
import config

def toBigQuery(bigquery, project_id, dataset_id, table_name, row,
                           num_retries=5):
    insert_all_data = {
        'rows': [{
            'json': row,
            # Generate a unique id for each row so retries don't accidentally
            # duplicate insert
            'insertId': str(uuid.uuid4()),
        }]
    }
    # saved to both the tables processed and raw
    return bigquery.tabledata().insertAll(
        projectId=project_id,
        datasetId=dataset_id,
        tableId=table_name,
        body=insert_all_data).execute(num_retries=num_retries)

def post():
    # get data from the message and process it as per the column names for both raw and the processed table
    # sample data - the incoming messages are in query string format
    bigquery = json.dumps(challenge_lvl=5&player_id=12345&interaction_time="2017-05-02 02:25:01")
    project_id = config.PROJECT_ID
    project_id = config.PROJECT_ID
    dataset_id = config.BQ_PROCESSED_DATASET_ID # same for the raw dataset as well
    table_name = config.BQ_PROCESSED_TABLE_ID # same for the raw table id as well
    toBigQuery(bigquery, project_id, dataset_id, table_name, row,
                           num_retries=5)
    return


