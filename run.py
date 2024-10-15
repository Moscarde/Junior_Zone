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

    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Daily update"], check=True)
        subprocess.run(["git", "push", "origin", "automation"], check=True)
    except subprocess.CalledProcessError as e:
        print("Erro ao executar comandos git:", e)
        return

    print(">> WAITING 20s FOR THE PROCESS TO FINISH")
    time.sleep(20)

    url = "https://bit.ly/planilhaJuniorZone1"
    try:
        webbrowser.open(url)
    except webbrowser.Error as e:
        print("Erro ao abrir o navegador:", e)

    exit()

if __name__ == "__main__":
    main()