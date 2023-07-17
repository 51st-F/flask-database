import pandas as pd
from google.cloud import storage

df = pd.read_csv('test.csv')

client = storage.Client.from_service_account_json('fluentd.json')
export_bucket = client.get_bucket('gcs_bucket')

blob = export_bucket.blob('folder/test.csv')
blob.upload_from_string(df.to_csv(index=False),'text/csv')