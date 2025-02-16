# functions/blob_storage_trigger.py
import logging
import azure.functions as func

def main(myblob: func.InputStream):
    logging.info(f"BlobStorageTrigger processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")
    content = myblob.read().decode('utf-8')
    logging.info(f"Report Content: {content}")