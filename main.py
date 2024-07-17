from modules.gupy_scraper import GupyScraper
from modules.data_handler import DataHandler
from modules.data_handler import update_google_sheets_dataset
from modules.telegram_message import TelegramMessage
from modules.telegram_bot import TelegramBot
from dotenv import load_dotenv

import os, sys


load_dotenv()
TOKEN = os.environ["TOKEN"]
MAIN_GROUP_CHAT_ID = os.environ["MAIN_GROUP_CHAT_ID"]
TEST_GROUP_CHAT_ID = os.environ["TEST_GROUP_CHAT_ID"]


def detect_environment() -> int:
    """
    Detects the environment based on command line arguments and returns the corresponding group chat ID.

    Returns:
        int: The group chat ID.
    """
    if "--dev" in sys.argv:
        print(">> DEVELOPMENT ENVIRONMENT SELECTED")
        return TEST_GROUP_CHAT_ID

    elif "--prod" in sys.argv:
        print(">> PRODUCTION ENVIRONMENT SELECTED")
        return MAIN_GROUP_CHAT_ID

    else:
        return select_environment()


def select_environment() -> int:
    """
    Prompts the user to select an environment and returns the corresponding chat ID.

    Returns:
        int: The chat ID of the selected environment.
    """
    print("NO ENVIRONMENT SELECTED, PLEASE SELECT ONE:")
    groups_id = {1: MAIN_GROUP_CHAT_ID, 2: TEST_GROUP_CHAT_ID}

    print("ENVIRONMENTS:\n" "[1] PRODUCTION GROUP\n" "[2] DEVELOPMENT GROUP")
    option = int(input(">> SELECT ENVIRONMENT: "))

    if option in groups_id:
        chat_id = groups_id[option]
        return chat_id

    else:
        print("INVALID OPTION")
        select_environment()


def request_data() -> None:
    """
    Requests data from GupyScraper and saves it.
    """
    filter_labels = [
        "analista",
        "dados",
        "python",
        "data",
        "Desenvolvedor",
        "Dev",
        "Front",
        "Back",
        "Full Stack",
        "FullStack",
        "Software",
        "DevOps",
        "Business Intelligence",
        "Machine Learning",
        "Inteligência Artificial",
        "Power BI",
    ]
    scraper = GupyScraper(filter_labels)
    scraper.request_and_save()


def process_and_publish_responses(chat_id: int) -> None:
    """
    Process and publish responses.

    Args:
        chat_id (int): The ID of the chat.

    Returns:
        None
    """
    data_handler = DataHandler()
    filtered_vacancies_dfs = data_handler.filtered_dfs

    telegram_message = TelegramMessage(filtered_vacancies_dfs)

    send_message(
        message_content=telegram_message.header,
        message_type="text",
        chat_id=chat_id,
        disable_notification=False,
    )

    send_message(
        message_content=telegram_message.section_dados_image,
        message_type="image",
        chat_id=chat_id,
    )
    send_message(
        message_content=telegram_message.section_dados_messages,
        message_type="text",
        chat_id=chat_id,
    )

    send_message(
        message_content=telegram_message.section_dev_image,
        message_type="image",
        chat_id=chat_id,
    )
    send_message(
        message_content=telegram_message.section_dev_messages,
        message_type="text",
        chat_id=chat_id,
    )

    if tag_data_as_submitted():
        data_handler.tag_as_submitted()
        print("TAGED!")


def send_message(
    message_content: (str, bytes),
    message_type: str,
    chat_id: int,
    disable_notification: bool = True,
) -> None:
    """
    Sends a message to a chat on Telegram.

    Args:
        message_content (str | bytes): The content of the message. It can be either a text message or an image file.
        message_type (str): The type of the message. It can be either "text" or "image".
        chat_id (int): The ID of the chat.
        disable_notification (bool, optional): Whether to disable notification for the message. Defaults to True.
    """
    junior_bot = TelegramBot(TOKEN)

    if message_type == "text":
        junior_bot.send_message(chat_id, message_content, disable_notification)

    if message_type == "image":
        junior_bot.send_image(chat_id, message_content, disable_notification)


def tag_data_as_submitted() -> bool:
    """
    Prompts the user to tag the data as submitted.

    Returns:
        bool: True if the data is tagged as submitted, False otherwise.
    """
    if __name__ == "__main__":
        print("\nTAG DATA AS SUBMITTED?\n" "[1] YES\n" "[2] NO")
        tag = int(input(">> ANSWER:"))
        if tag == 1:
            return True
        else:
            return False
    else:
        return True


def send_custom_text(chat_id: int) -> None:
    """
    Prompts the user to enter a custom text and sends it to the specified chat ID.

    Args:
        chat_id (int): The ID of the chat.

    Returns:
        None
    """
    text: str = input("\n>> ENTER CUSTON TEXT: ")
    converted_message: str = TelegramMessage.formatter_string(text)
    send_message(converted_message, "text", chat_id)


def send_image(chat_id: int) -> None:
    """
    Prompts the user to enter a file name and sends an image to the specified chat ID.

    Args:
        chat_id (int): The ID of the chat.

    Returns:
        None
    """
    file_name: str  = input(">> FILE NAME IN PICTURES FOLDER: ")
    content: bytes = open(f"pictures/{file_name}", "rb")
    send_message(content, "image", chat_id)


def update_sheets_dataset() -> None:
    """
    Update the Google Sheets dataset.

    Returns:
        None
    """
    update_google_sheets_dataset()
    print("UPDATED!")


def main(chat_id: int) -> None:
    """
    Main function to handle user input and execute corresponding options.
    
    Args:
        chat_id (int): The ID of the chat.
    """
    options = {
        1: request_data,
        2: lambda: process_and_publish_responses(chat_id),
        3: lambda: send_custom_text(chat_id),
        4: lambda: send_image(chat_id),
        5: update_sheets_dataset,
        6: lambda: exit(),
    }
    print(
        "\n"
        "[--MAIN MENU--]\n"
        "[1] REQUEST DATA\n"
        "[2] PROCESS AND SEND LAST REQUEST\n"
        "[3] SEND CUSTOM TEXT\n"
        "[4] SEND IMAGE\n"
        "[5] UPDATE SHEETS DATASET\n"
        "[6] EXIT"
    )
    option: int = int(input(">> SELECT FUNCTION: "))

    if option in options:
        options[option]()
    else:
        print("INVALID OPTION")

    main(chat_id)


if __name__ == "__main__":
    print(
        """
.·:''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''':·.
: :           #                                  #######                          : :
: :           # #    # #    # #  ####  #####          #   ####  #    # ######     : :
: :           # #    # ##   # # #    # #    #        #   #    # ##   # #          : :
: :           # #    # # #  # # #    # #    #       #    #    # # #  # #####      : :
: :     #     # #    # #  # # # #    # #####       #     #    # #  # # #          : :
: :     #     # #    # #   ## # #    # #   #      #      #    # #   ## #          : :
: :      #####   ####  #    # #  ####  #    #    #######  ####  #    # ######     : :
'·:...............................................................................:·'
"""
    )
    chat_id = detect_environment()
    main(chat_id)
