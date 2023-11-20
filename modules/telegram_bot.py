import requests

class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.api_url = f"https://api.telegram.org/bot{token}/"

    def get_updates(self, offset=None, timeout=30):
        method = "getUpdates"
        params = {"timeout": timeout, "offset": offset}
        resp = requests.get(self.api_url + method, params)
        result = resp.json()["result"]
        return result

    def send_message(self, chat_id, text):
        method = "sendMessage"
        params = {"chat_id": chat_id, "text": text, "parse_mode": "MarkdownV2"}
        resp = requests.post(self.api_url + method, params)
        print(resp)

    def send_photo(self, chat_id, file_opened):
        method = "sendPhoto"
        params = {"chat_id": chat_id}
        files = {"photo": file_opened}
        resp = requests.post(self.api_url + method, params, files=files)
        print(resp)

    def send_message_main_group(self, text):
        chat_id = "-1001984744184"
        self.send_message(chat_id, text)


if __name__ == "__main__":
    from dotenv import load_dotenv
    from datetime import datetime
    import os
    load_dotenv()
    token = os.environ["TOKEN"]

    jj = TelegramBot(token)
    jj.send_message_main_group(f"teste")
    jj.send_photo("-1001984744184", open('img_test.jpg', 'rb'))