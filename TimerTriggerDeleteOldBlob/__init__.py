from datetime import datetime, timezone
import logging
import os
import azure.functions as func
from azure.storage.blob import ContainerClient


def main(mytimer: func.TimerRequest, outputQueueItem: func.Out[func.QueueMessage]) -> None:
    utc_timestamp = datetime.utcnow().replace(tzinfo=timezone.utc)

    logging.info('Python timer trigger function ran at %s', utc_timestamp.isoformat())

    storage_connection_string = os.environ["AzureWebJobsStorage"]
    container = ContainerClient.from_connection_string(conn_str=storage_connection_string, container_name="image-input")
    blob_list = container.list_blobs()
    
    for blob in blob_list:
        
        diff = utc_timestamp - blob.creation_time
        # If the blob is older than X days/minutes/seconds, delete it

        if(diff.seconds > 120):
            blob_client = container.get_blob_client(blob)
            blob_client.delete_blob()
    
            # Store it in the queue output binding
            outputQueueItem.set(blob.name)
