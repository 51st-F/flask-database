import time
from google.cloud import bigquery

table_id = 'project_id.dataset.table'
client = bigquery.Client.from_service_account_json('fluentd.json')

job_config = bigquery.LoadJobConfig(
    source_format = bigquery.SourceFormat.CSV,
    skip_leading_rows = 1,
    # autodetect = True
)

### trunc table
delete_sql = f"TRUNCATE TABLE { table_id }"
client.query(delete_sql)

### import data
with open('test.csv',"rb") as f:
    job = client.load_table_from_file(f, table_id, job_config=job_config)

print(job.state)

while job.state != 'DONE':
    time.sleep(3)
    job.reload()
    print(job.state)

print(job.result())

table = client.get_table(table_id)
print(
    f"Loaded {table.num_rows} rows and {len(table.schema)} columns to {table_id}"
)