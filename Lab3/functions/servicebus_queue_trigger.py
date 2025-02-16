# functions/servicebus_queue_trigger.py
import logging
import json
import os
import datetime
from azure.storage.blob import BlobServiceClient
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("ServiceBusQueueTrigger function processed a request.")
    
    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)
    
    report = req_body.get("report")
    if not report:
        return func.HttpResponse("No report provided", status_code=400)
    
    # Convert the report to a formatted string.
    report_content = json.dumps(report, indent=4)
    
    # Retrieve the Storage connection string from the environment variable.
    connection_string = os.getenv("AzureWebJobsStorage")
    if not connection_string:
        return func.HttpResponse("Storage connection string not configured", status_code=500)
    
    # Use the blob container name from environment variables.
    container_name = os.getenv("BLOB_CONTAINER_NAME", "lab3blobcontainer")
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    
    # Get the container client (create the container if it does not exist).
    container_client = blob_service_client.get_container_client(container_name)
    try:
        container_client.create_container()
    except Exception as e:
        logging.info("Container already exists or creation error: %s", e)
    
    # Create a unique blob name using the current timestamp.
    blob_name = f"report_{datetime.datetime.utcnow().isoformat()}.txt"
    
    try:
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(report_content)
        logging.info("Report uploaded as blob: %s", blob_name)
    except Exception as e:
        logging.error("Error uploading blob: %s", e)
        return func.HttpResponse("Error uploading blob", status_code=500)
    
    return func.HttpResponse(f"Report successfully uploaded as {blob_name}", status_code=200)