from telethon import events

from logs.logger import log


class BaseHandlers:
    def __init__(self,client):

        self.client = client

    def base_handlers(self):
        @self.client.on(events.NewMessage(pattern=r'^\/(?i:start)'))
        async def start_handler(msg):
            """
            Handles the /start command by sending a welcome message to the user.
            """
            log.info(f"User ID: {str(msg.sender_id)} using start_handler.")

            welcome_message = "Welcome to the bot! Use /help to view available commands."
            await msg.reply(welcome_message)

        @self.client.on(events.NewMessage(pattern=r'^\/(?i:help)'))
        async def help_handler(msg):
            """
            Handles the /help command by listing all available commands and their descriptions.
            """
            log.info(f"User ID: {str(msg.sender_id)} using help_handler.")

            help_message = (
                "<b>Available Commands:</b>\n"
                "/start [no args] - Welcome message and bot information\n"
                "/help [no args] - Show this help message\n"
                "/add &lt;version&gt; &lt;client_name&gt; - Add a new client version\n"
                "/rm &lt;version&gt; &lt;client_name&gt; - Remove a client version\n"
                "/get [no args] | &lt;version&gt; | &lt;client_name&gt; | &lt;version&gt; &lt;client_name&gt; - Get information about client versions\n"
            )
            await msg.reply(help_message, parse_mode='html')
