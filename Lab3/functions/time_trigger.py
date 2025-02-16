# functions/time_trigger.py
import datetime
import logging
import requests
import azure.functions as func

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
    logging.info('TimeTrigger function executed at %s', utc_timestamp)
    
    # Configure the URL for the HTTPTrigger function accordingly
    http_trigger_url = "https://funccst8917lab3.azurewebsites.net/api/HTTPTrigger"
    
    try:
        response = requests.get(http_trigger_url)
        logging.info("HTTPTrigger invoked with status: %s", response.status_code)
    except Exception as e:
        logging.error("Error invoking HTTPTrigger: %s", e)