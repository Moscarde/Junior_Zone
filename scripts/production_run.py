import webbrowser
import time
import subprocess
import os
from dotenv import load_dotenv
from main import request_data, process_and_publish_responses, update_sheets_dataset

def main():
    load_dotenv()
    MAIN_GROUP_CHAT_ID = os.environ["MAIN_GROUP_CHAT_ID"]

    request_data()

    process_and_publish_responses(MAIN_GROUP_CHAT_ID)

    update_sheets_dataset()

    subprocess.call(["scripts/git_commit.bat"])

    print(">> WAITING 20s FOR THE PROCESS TO FINISH")
    time.sleep(20)

    url = "https://bit.ly/planilhaJuniorZone1"
    webbrowser.open(url)

    input(">> PRESS ENTER TO EXIT")
    exit()


if __name__ == "__main__":
    main()