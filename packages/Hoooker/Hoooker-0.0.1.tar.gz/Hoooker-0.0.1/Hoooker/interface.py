import json
import requests


class BotInterface(object):
    def get_content(self, request) -> dict:
        raise NotImplementedError

    def reply(self, *args, **kwargs):
        raise NotImplementedError

    def push(self, *args, **kwargs):
        raise NotImplementedError

    @staticmethod
    def __check_error(response):
        if 200 <= response.status_code < 300:
            pass
        else:
            raise RuntimeError(json.dumps(response.json(), ensure_ascii=False))

    @staticmethod
    def __WebhookPayload_2_dict__(obj) -> dict:
        return {
            "events": obj.events,
            "user_id": obj.destination
        }

    @staticmethod
    def request(url, method, headers, data=None):
        response = None
        if method == "POST":
            response = requests.post(
                url, headers=headers, data=data, timeout=30
            )

        elif method == "GET":
            response = requests.get(
                url, headers=headers, timeout=30
            )

        return response
