# functions/durable_fanoutin_trigger.py
import logging
import json
import requests
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("DurableFanOutInTrigger function started processing.")
    
    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)
    
    urls = req_body.get("urls", [])
    if not urls:
        return func.HttpResponse("No URLs provided", status_code=400)
    
    report = {}
    # Send a GET request for each URL and record the status code.
    for url in urls:
        try:
            response = requests.get(url, timeout=5)
            report[url] = response.status_code
        except Exception as e:
            report[url] = f"Error: {str(e)}"
    
    # Updated URL for ServiceBusQueueTrigger.
    servicebus_trigger_url = "https://funccst8917lab3.azurewebsites.net/api/ServiceBusQueueTrigger"
    try:
        headers = {"Content-Type": "application/json"}
        response = requests.post(servicebus_trigger_url, headers=headers, data=json.dumps({"report": report}))
        logging.info("ServiceBusQueueTrigger invoked with status: %s", response.status_code)
    except Exception as e:
        logging.error("Error invoking ServiceBusQueueTrigger: %s", e)
    
    return func.HttpResponse("DurableFanOutInTrigger executed successfully.", status_code=200)