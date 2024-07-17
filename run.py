import webbrowser
import time
import subprocess
import os
from dotenv import load_dotenv
from main import request_data, process_and_publish_responses, update_sheets_dataset

def main():
    # load_dotenv()
    # MAIN_GROUP_CHAT_ID = os.environ["MAIN_GROUP_CHAT_ID"]

    # request_data()

    # process_and_publish_responses(MAIN_GROUP_CHAT_ID)

    # update_sheets_dataset()
    
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "Daily update"], check=True)
    subprocess.run(["git", "push", "origin", "automation"], check=True)

    print(">> WAITING 20s FOR THE PROCESS TO FINISH")
    time.sleep(20)

    url = "https://bit.ly/planilhaJuniorZone1"
    webbrowser.open(url)

    exit()


if __name__ == "__main__":
    main()
