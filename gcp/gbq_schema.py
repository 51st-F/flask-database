from google.cloud import bigquery

dataset_id = 'gbq-dataset'
table_id = 'gbq-table'

client = bigquery.Client.from_service_account_json('fluentd.json')

schema = [
    bigquery.SchemaField("test", "STRING")
]

# Define the table reference
table_ref = client.dataset(dataset_id).table(table_id)

# Define the table schema
table = bigquery.Table(table_ref, schema=schema)

# Create the table
client.create_table(table)