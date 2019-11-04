# python 3.7.4

import os
import json
import datetime  # for the expiration property: a date string to epoch millisec
import uuid  # for the id property
import requests

from apiclient import discovery
from google.oauth2 import service_account

try:
    ep = (
        lambda yr, mo, dd, hh, mm: int(
            datetime.datetime(yr, mo, dd, hh, mm).timestamp()
        )
        * 1000
    )
    API = "drive"
    API_VERSION = "v3"
    scopes = [
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/drive.file",
    ]
    with open("new-push-service-account.json", "r") as read_file:
        serv_acct_info = json.load(read_file)

    # this needs to change to get credentials from a string object instead of a file
    # i.e. json.loads of a string from AWS SSM
    # https://google-auth.readthedocs.io/en/latest/reference/google.oauth2.service_account.html

    credentials = service_account.Credentials.from_service_account_info(
        serv_acct_info, scopes=scopes
    )
    drive_service = discovery.build(API, API_VERSION, credentials=credentials)

    # more to put in SSM
    url_webhook = "https://noelfonseca.com/notifications"
    gfolder_id = "14gG8_SQwn7zPaRX_AvtyVSe91NbrUQZc"

    """
    if url_webhook and gfolder_id:
        pass
    else:
        raise KeyError
    """

    # request body; note expiration ep is based on local time
    data = {
        "id": str(uuid.uuid4()),
        "expiration": ep(2019, 12, 20, 8, 53),
        "address": url_webhook,
        "type": "web_hook",
    }

    response = drive_service.files().watch(fileId=gfolder_id, body=data).execute()
    print(response)
    print(type(response))

    channel_ID_value = response["id"]
    expiration_date_and_time = response["expiration"]
    identifier_for_the_watched_resource = response["resourceId"]
    version_specific_URI_of_the_watched_resource = response["resourceUri"]

<<<<<<< HEAD
    payload = {
        
=======
    sync_message = {
>>>>>>> parent of de238bf... after office code Oct 22
        "Content-Type": "application/json; utf-8",
        "Content-Length": "0",
        "X-Goog-Channel-ID": channel_ID_value,
        # X-Goog-Channel-Token: channel-token-value
        "X-Goog-Channel-Expiration": expiration_date_and_time,
        "X-Goog-Resource-ID": identifier_for_the_watched_resource,
        "X-Goog-Resource-URI": version_specific_URI_of_the_watched_resource,
        "X-Goog-Resource-State": "sync",
        "X-Goog-Message-Number": "1",
    }
<<<<<<< HEAD
    
=======
>>>>>>> parent of de238bf... after office code Oct 22

    response2 = requests.post(url_webhook, headers=sync_message)
    print(response2)
    print(response2.headers)
    
    #test

    # sample successful request response
    # https://developers.google.com/drive/api/v3/reference/files/watch?authuser=0#response_1

except OSError as e:
    print(e)
