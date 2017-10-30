import requests
import logging


logger = logging.getLogger(__name__)


class TelegramBot:
    API_URL = "https://api.telegram.org/"

    def __init__(self, bot_token, channel_id):

        self.bot_token = bot_token
        self.channel_id = channel_id
        self.send_request("/getMe")

    def send_request(self, path, **kwargs):
        url_path = self.API_URL + "bot" + self.bot_token + path
        with requests.session() as s:
            response = s.get(url_path, params=kwargs)
            logger.debug("making request to {}".format(response.url))
        return response.json()

    def send_message(self, text):
        data = {}
        data['text'] = text
        data['chat_id'] = self.channel_id
        result = self.send_request("/sendMessage", **data)
        logger.debug(result)