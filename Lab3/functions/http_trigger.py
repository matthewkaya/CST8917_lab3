# functions/http_trigger.py
import logging
import json
import requests
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("HTTPTrigger function processed a request.")
    
    # List of URLs updated to your provided URLs
    url_list = [
        "https://canadasfer.com/",
        "https://devopsfer.com/",
        "https://digisfer.com/"
    ]
    
    # URL for DurableFanOutInTrigger function
    durable_fanout_url = "https://funccst8917lab3.azurewebsites.net/api/DurableFanOutInTrigger"
    
    try:
        headers = {"Content-Type": "application/json"}
        response = requests.post(durable_fanout_url, headers=headers, data=json.dumps({"urls": url_list}))
        logging.info("DurableFanOutInTrigger invoked with status: %s", response.status_code)
    except Exception as e:
        logging.error("Error invoking DurableFanOutInTrigger: %s", e)
    
    return func.HttpResponse("HTTPTrigger executed successfully.", status_code=200)