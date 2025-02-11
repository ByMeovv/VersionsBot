# Author: "ByMeow"
# __version__ = 1.0

from telethon import TelegramClient
from logs.logger import log
from data.cfg import Config


class VersionsBot:

    def __init__(self,
                session: str = Config.get_value('bot')['env']['session'],
                api_id: int = Config.get_value('bot')['env']['api_id'],
                api_hash: str = Config.get_value('bot')['env']['api_hash'],
                token: str = Config.get_value('bot')['env']['token']) -> None:

        """
        Initialize a new instance of the Telegram client.

        :param session: Telegram session name.
        :type session: str
        :param api_id: Telegram API ID.
        :type api_id: int
        :param api_hash: Telegram API Hash.
        :type api_hash: str
        :param token: Token to use for the Telegram client.
        :type token: str

        Initialize the Telegram client with the provided credentials.
        """

        self.SESSION = session
        self.API_ID = api_id
        self.API_HASH = api_hash
        self.TOKEN = token
        self.client = TelegramClient(self.SESSION, self.API_ID, self.API_HASH)

    def start(self):

        """
        Initialize and start the Telegram client session.

        This method starts the Telegram client using the provided token,
        logs the start of the Bot, and keeps the client running until
        disconnected. Once disconnected, it logs the stop of the Bot.
        """

        self.client.start(bot_token=self.TOKEN)
        log.info("> Starting Bot")
        self.client.run_until_disconnected()
        log.info("> Stopping Bot")
