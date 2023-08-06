import json
from .interface import BotInterface
from .__tool__ import format_to_message


class LineBITF(BotInterface):
    LINE_PUSH_ENDPOINT = '/v2/bot/message'

    def __init__(self, access_token, channel_secret):
        self.LINE_CHANNEL_ACCESS_TOKEN = access_token
        self.LINE_CHANNEL_SECRET = channel_secret

    def reply(self, says: [str], reply_token):
        messages = format_to_message(says)

        data = {
            'replyToken': reply_token,
            'messages': messages,
            'notificationDisabled': False,
        }

        self.__send_to_line__(
            f"{self.LINE_PUSH_ENDPOINT}/reply", data=json.dumps(data)
        )

    def push(self, userId, text):
        messages = format_to_message(text)

        #
        data = {
            'to': userId,
            'messages': messages,
            'notificationDisabled': False,
        }

        return self.__send_to_line__(
            f"{self.LINE_PUSH_ENDPOINT}/push", data=json.dumps(data)
        )

    def get_content(self, request) -> dict:
        body = request.body.decode('utf-8')
        body_json = json.loads(body)

        return body_json

    def get_user_info(self, user_id):
        res = self.__send_to_line__(f"/v2/bot/profile/{user_id}", method="GET")
        return res.json()

    ##
    def __send_to_line__(self, path, data=None, method="POST"):
        url = 'https://api.line.me' + path
        headers = {'Content-Type': 'application/json',
                   'Authorization': f'Bearer {self.LINE_CHANNEL_ACCESS_TOKEN}',
                   'User-Agent': 'line-bot-sdk-python/1.19.0'}

        response = self.request(url, method, headers, data)
        # self.__check_error(response)
        return response
