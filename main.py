from modules.gupy_scraper import GupyScraper
from modules.data_handler import DataHandler
from modules.telegram_bot import TelegramBot
from datetime import datetime
from dotenv import load_dotenv
import os


load_dotenv()
TOKEN = os.environ["TOKEN"]
MAIN_GROUP_CHAT_ID = os.environ["MAIN_GROUP_CHAT_ID"]
TEST_GROUP_CHAT_ID = os.environ["TEST_GROUP_CHAT_ID"]


def main():
    date = datetime.now().date()

    print(">> SCRAP DATA?")
    option = int(input(" [1] YES | [2] NO\n"))
    if option == 1:
        scraper = GupyScraper()
        scraper.request_and_save(["analista", "dados", "python", "data"])

    print("\n>> SELECT DATASET")
    option = int(
        input(
            " [1] PROCESS LAST REQUEST | [2] PROCESS CUSTOM DATE REQUEST | [3] CUSTOM TEXT | [4] PHOTO \n"
        )
    )
    if option == 1:
        data_handler = DataHandler(date)
        text = data_handler.telegram_text


    elif option == 2:
        date = input(">> DATE (YYYY-MM-DD): ")
        data_handler = DataHandler(date)
        text = data_handler.telegram_text

    elif option == 3:
        text = input(">> TEXT: ")

    elif option == 4:
        file_name = input(">> FILE NAME IN PICTURES FOLDER: ")
        text = open(f"pictures/{file_name}", "rb")
    

    else:
        print("INVALID OPTION")
        return

    print("\n>> SEND TO")
    option = int(input(" [1] MAIN GROUP | [2] TEST GROUP\n"))
    if option == 1:
        chat_id = MAIN_GROUP_CHAT_ID

    elif option == 2:
        chat_id = TEST_GROUP_CHAT_ID

    else:
        print("INVALID OPTION")
        return

    junior_bot = TelegramBot(TOKEN)
    if type(text) == str:
        junior_bot.send_message(chat_id=chat_id, text=text)
    else:
        junior_bot.send_photo(chat_id=chat_id, file_opened=text)

    print("\n>> DONE")
    print("\n>> SEND ANOTHER MESSAGE?")
    option = int(input(" [1] YES | [2] NO\n"))
    if option == 1:
        main()



if __name__ == "__main__":
    main()
    # res = junior_bot.send_message_main_group("*bold*")
