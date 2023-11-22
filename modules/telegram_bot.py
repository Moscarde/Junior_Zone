import requests
from pprint import pprint


class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.api_url = f"https://api.telegram.org/bot{token}/"

    def get_updates(self, offset=None, timeout=30):
        method = "getUpdates"
        params = {"timeout": timeout, "offset": offset}
        response = requests.get(self.api_url + method, params)
        return response.json()["result"]

    def send_message(self, chat_id, content):
        if type(content) == str:
            content = [content]
        for text in content:
            method = "sendMessage"
            params = {
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "MarkdownV2",
                "disable_web_page_preview": True,
            }
            response = requests.post(self.api_url + method, params)
            self.print_response_status(response)

    def send_image(self, chat_id, file_opened):
        method = "sendPhoto"
        params = {"chat_id": chat_id}
        files = {"photo": file_opened}
        response = requests.post(self.api_url + method, params, files=files)
        self.print_response_status(response)

    def print_response_status(self, response):
        if response.json()["ok"]:
            print(
                f"SUCCESS - Message sent to \"{response.json()['result']['chat']['title']}\"\n"
            )
        else:
            print(f"FAIL - Error code: {response.json()['error_code']}")
            print(f"Description: {response.json()['description']}\n")



if __name__ == "__main__":
    from dotenv import load_dotenv
    from datetime import datetime
    import os

    load_dotenv()
    token = os.environ["TOKEN"]

    jj = TelegramBot(token)
    jj.send_message_test_group(f"teste")
    # jj.send_photo("-4059537333", open("pictures/img_test.jpg", "rb"))
