import requests
import json
import logging
import os
import pytz
from datetime import datetime

WEBHOOK_URL = os.environ["WEBHOOK_URL"]

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def send_slack(color, message):
    slack_payload = {
        "username": "AWS Console Login 알림",
        "icon_emoji": ":envelope:",
        "attachments": [
            {
                "color": color,
                "text" : message
            }
        ]
    }
    
    try:
        req = requests.post(
            WEBHOOK_URL, 
            data = json.dumps(slack_payload),
            headers = {"Content-Type": "application/json"}
            )
        logger.info(f"response: {req.text}")
    except Exception as e:
        logger.error(f"Error: {e}")


def lambda_handler(event, context):
    
    logger.info(f"Event: {event}")
    payload = event["detail"]
    account = payload["userIdentity"]["accountId"]
    user_name = payload["userIdentity"]["userName"]
    source_ip = payload["sourceIPAddress"]
    event_name = payload["eventName"]
    login_time_utc = payload["eventTime"]
    
    time_format = "%Y-%m-%dT%H:%M:%SZ"

    utc_time = datetime.strptime(login_time_utc, time_format)

    utc_zone = pytz.utc
    utc_time = utc_zone.localize(utc_time)

    kst_zone = pytz.timezone("Asia/Seoul")

    kst_time = utc_time.astimezone(kst_zone)

    login_time_kst = kst_time.strftime(time_format)
    
    if event_name == "ConsoleLogin":
        login_status_check = payload["responseElements"]["ConsoleLogin"]
        if login_status_check == "Success":
            color = "good"
            message = f"Login Time: `{login_time_kst}`\nAccount: `{account}`\nUser: `{user_name}`\nSource IP: `{source_ip}`"
            send_slack(color, message)
        elif login_status_check == "Failure":
            color = "danger"
            failure_message = payload["errorMessage"]
            message = f"Login Time: `{login_time_kst}`\nAccount: `{account}`\nUser: `{user_name}`\nSource IP: `{source_ip}`\nFailure Message: `{failure_message}`"
            send_slack(color, message)
    else:
        logger.error("Not Found ConsoleLogin Event")