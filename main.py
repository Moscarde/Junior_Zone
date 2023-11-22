from modules.gupy_scraper import GupyScraper
from modules.data_handler import DataHandler
from modules.data_handler import text_converter as telegram_text_converter
from modules.data_handler import compile_to_excel
from modules.telegram_bot import TelegramBot
from datetime import datetime
from dotenv import load_dotenv
import os, io


load_dotenv()
TOKEN = os.environ["TOKEN"]
MAIN_GROUP_CHAT_ID = os.environ["MAIN_GROUP_CHAT_ID"]
TEST_GROUP_CHAT_ID = os.environ["TEST_GROUP_CHAT_ID"]


def request_data():
    scraper = GupyScraper()
    scraper.request_and_save(["analista", "dados", "python", "data"])
    main()


def process_request():
    date = datetime.now().date()
    data_handler = DataHandler(date)

    message_content = data_handler.telegram_text
    send_message(message_content, "text")
    if tag_data_as_submitted():
        data_handler.tag_as_submitted()


def send_message(message_content, message_type):
    chat_id = input_select_group()

    jj = TelegramBot(TOKEN)

    if message_type == "text":
        jj.send_message(chat_id, message_content)
    if message_type == "image":
        jj.send_image(chat_id, message_content)


def input_select_group():
    groups_id = {1: MAIN_GROUP_CHAT_ID, 2: TEST_GROUP_CHAT_ID}
    print("\nGROUPS:\n" "[1] MAIN GROUP\n" "[2] TEST GROUP")
    group_id = int(input(">> SELECT GROUP:"))
    if group_id in groups_id:
        chat_id = groups_id[group_id]
    else:
        print("INVALID OPTION")
        return main()
    return chat_id


def tag_data_as_submitted():
    print("\nTAG DATA AS SUBMITTED?\n" "[1] YES\n" "[2] NO")
    tag = int(input(">> ANSWER:"))
    if tag == 1:
        return True
    else:
        return False


def send_custom_text():
    message = input("\n>> ENTER CUSTON TEXT:")
    converted_message = telegram_text_converter(message)
    send_message(converted_message, "text")
    main()


def send_image():
    file_name = input(">> FILE NAME IN PICTURES FOLDER: ")
    content = open(f"pictures/{file_name}", "rb")
    send_message(content, "image")


def update_sheets_dataset():
    try:
        compile_to_excel()
    except Exception as e:
        print(e)
    finally:
        print("UPDATED!")


def main():
    options = {
        1: request_data,
        2: process_request,
        3: send_custom_text,
        4: send_image,
        5: update_sheets_dataset,
    }
    print(
        "[1] REQUEST DATA\n"
        "[2] PROCESS AND SEND LAST REQUEST\n"
        "[3] SEND CUSTOM TEXT\n"
        "[4] SEND IMAGE\n"
        "[5] UPDATE SHEETS DATASET"
    )
    option = int(input(">> SELECT FUNCTION:"))

    if option in options:
        options[option]()
    else:
        print("INVALID OPTION")


if __name__ == "__main__":
    main()

