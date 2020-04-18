import logging
import json

import azure.functions as func


def main(msg: func.QueueMessage, SendGridMessage: func.Out[str]) -> None:
    logging.info('Python queue trigger function processed a queue item: %s',
                 msg.get_body().decode('utf-8'))
    
    value = "Old file deleted from the Azure blob container: " + msg.get_body().decode('utf-8')

    message = {
        "personalizations": [ {
          "to": [{
            "email": "<<TO EMAIL>>"
            }]}],
        "from": { "email": "<<FROM EMAIL>>" },
        "subject": "Blob File Deleted",
        "content": [{
            "type": "text/plain",
            "value": value }]}

    SendGridMessage.set(json.dumps(message))
