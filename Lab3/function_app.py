import azure.functions as func
from functions.time_trigger import main as time_trigger_main
from functions.http_trigger import main as http_trigger_main
from functions.durable_fanoutin_trigger import main as durable_fanoutin_trigger_main
from functions.servicebus_queue_trigger import main as servicebus_queue_trigger_main
from functions.blob_storage_trigger import main as blob_storage_trigger_main

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Timer Trigger with arg_name specified
@app.function_name(name="TimeTrigger")
@app.timer_trigger(arg_name="mytimer", schedule="0 0 0 * * *")  # Cron expression for daily execution at UTC midnight
def TimeTrigger(mytimer: func.TimerRequest) -> None:
    return time_trigger_main(mytimer)

# HTTP Trigger: Triggered by HTTP GET or POST requests.
@app.function_name(name="HTTPTrigger")
@app.route(route="HTTPTrigger", methods=["GET", "POST"])
def HTTPTrigger(req: func.HttpRequest) -> func.HttpResponse:
    return http_trigger_main(req)

# Durable Fan-Out/In Trigger: Processes a list of URLs.
@app.function_name(name="DurableFanOutInTrigger")
@app.route(route="DurableFanOutInTrigger", methods=["POST"])
def DurableFanOutInTrigger(req: func.HttpRequest) -> func.HttpResponse:
    return durable_fanoutin_trigger_main(req)

# Service Bus Queue Trigger: Simulated via HTTP for local testing.
@app.function_name(name="ServiceBusQueueTrigger")
@app.route(route="ServiceBusQueueTrigger", methods=["POST"])
def ServiceBusQueueTrigger(req: func.HttpRequest) -> func.HttpResponse:
    return servicebus_queue_trigger_main(req)

# Blob Storage Trigger: Triggered when a new blob is added.
@app.function_name(name="BlobStorageTrigger")
@app.blob_trigger(arg_name="myblob", path="lab3blobcontainer/{name}", connection="AzureWebJobsStorage")
def BlobStorageTrigger(myblob: func.InputStream):
    return blob_storage_trigger_main(myblob)