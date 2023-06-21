from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os 
from dotenv import load_dotenv
load_dotenv()



slack_token = os.getenv("slack_scraper_token")
channel =os.getenv("channel_id")
# print( slack_token)
# print(channel)

# Set the path to the file you want to send
file_path = r"Glassdoor_jobs.csv"
# file_path1= r"Glassdoor_jobs.xlsx"
# file_list= [file_path1, file_path]

# #Setting up an Automated Text
message ="Here is the Glassdoor scrapped Jobs"

# Initialize the Slack WebClient
client = WebClient(token=slack_token)

def send_message():
     try:
        response = client.chat_postMessage(
            channel=channel,
            text = message
        )
        if response["ok"]:
            print("File uploaded successfully.")
        else:
            print("Failed to upload file.")
     except SlackApiError as e:
         print(f"Error uploading file: {e.response['error']}")


#Function to send the file
def send_file():
     for element in file_path:
         response =client.files_upload_v2(
            channel = channel,
            file= element,
         )
     if response['ok']:
        print (f"File sent successful")
    
     else:
        print(f"Error sending file ")
    