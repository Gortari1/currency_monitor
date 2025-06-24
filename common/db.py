import os
import json
from google.cloud import storage

def write_db(bucket_name: str, blob_name: str, content: dict):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.upload_from_string(
        json.dumps(content),
        content_type="application/json"
    )

    print(f"✅ Saved to {bucket_name}/{blob_name}")