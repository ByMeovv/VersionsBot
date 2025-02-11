from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from telethon import events

from logs.logger import log
from utils.ArgsFromAddAndRm import get_args_from_add_and_rm
from db.database import get_db, Versions
from data.cfg import Config


class Add:
    def __init__(self,
                 client,
                 db_session: Session = next(get_db())):

        """
        Initialize the Add handler with the client.

        :param client: The Telegram client
        :type client: :class:`telethon.TelegramClient`
        """

        self.client = client
        self.db_session = db_session
        self.staff_ids: list = Config.get_value('bot')['staff_ids']

    def add_handler(self):

        @self.client.on(events.NewMessage(pattern=r'^\/(?i:add)(.*)'))
        async def add_handler(msg):

            """
            Handles the /add command by extracting the version and client name from the message text, and
            then processes them according to your logic. It interacts with the database and saves the client version.

            Parameters
            ----------

            :param msg: The Telegram message containing the /add command
            :type msg: :class:`telethon.tl.custom.message.Message`
            """

            if msg.sender_id not in self.staff_ids:
                await msg.reply("You don't have permission to use this command.")
                log.warning(f"User ID: {str(msg.sender_id)} tried to use add_handler but was not in staff_id list")
                return

            log.info(f"User ID: {str(msg.sender_id)} using add_handler")

            parser = get_args_from_add_and_rm(msg)

            args = msg.text.split()[1:]

            try:
                parsed_args = parser.parse_args(args)
                version = parsed_args.version
                name_client = parsed_args.name_client

                log.info(f"Version: {version}, Client Name: {name_client}")

                # Interact with the database and save the client version
                try:
                    self.db_session.query(Versions).filter_by(number=version, name=name_client).one()
                    log.warning(f"Client with Version: {version}, Client Name: {name_client} already exists in the database.")
                except NoResultFound:
                    client_record = Versions(number=version,
                                             name=name_client,
                                             create_id=msg.sender_id,
                                             create_username=msg.sender.username)
                    self.db_session.add(client_record)
                    self.db_session.commit()
                    self.db_session.refresh(client_record)
                    log.debug(f"Client with Version: {version}, Client Name: {name_client} added to the database successfully.")

                await msg.reply(f"Client with Version: {version}, Client Name: {name_client} processed successfully.")

            except SystemExit:
                await msg.reply("Invalid arguments. Usage: <code>/add &lt;version (int)&gt; &lt;name_client (str)&gt;</code>", parse_mode='html')

                log.error("Invalid arguments. Usage: /add <version (int)> <name_client (str)>")
