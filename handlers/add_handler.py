from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import func
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

    def add(self):

        @self.client.on(events.NewMessage(pattern=r'^\/(?i:add)(.*)'))
        async def add_handler(msg):
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

                # Check if the record already exists
                existing_record = self.db_session.query(Versions).filter_by(number=version, name=name_client).first()

                if existing_record:
                    log.warning(f"Client with Version: {version}, Client Name: {name_client} already exists in the database.")
                    await msg.reply(f"Client with Version: {version}, Client Name: {name_client} already exists in the database.")
                else:
                    # Add new record
                    client_record = Versions(number=version,
                                             name=name_client,
                                             create_id=msg.sender_id,
                                             create_username=msg.sender.username)
                    # New tip added to the database
                    try:
                        self.db_session.add(client_record)
                        self.db_session.commit()
                        self.db_session.refresh(client_record)
                        log.debug(f"Client with Version: {version}, Client Name: {name_client}, added to the database successfully.")
                        await msg.reply(f"Client with Version: {version}, Client Name: {name_client}, added to the database successfully.")
                    except IntegrityError:
                        self.db_session.rollback()
                        log.error(f"Failed to add client with Version: {version}, Client Name: {name_client}, to the database.")
                        # Find the next available _id
                        while True:
                            _id = self.db_session.query(func.max(Versions._id)).scalar() + 1
                            client_record._id = _id
                            try:
                                self.db_session.add(client_record)
                                self.db_session.commit()
                                self.db_session.refresh(client_record)
                                log.debug(f"Client with Version: {version}, Client Name: {name_client}, added to the database successfully with _id: {_id}.")
                                await msg.reply(f"Client with Version: {version}, Client Name: {name_client}, added to the database successfully with _id: {_id}.")
                                break
                            except IntegrityError:
                                self.db_session.rollback()
                                log.error(f"Failed to add client with Version: {version}, Client Name: {name_client}, to the database with _id: {_id}.")

            except SystemExit:
                await msg.reply("Invalid arguments. Usage: <code>/add &lt;version (int)&gt; &lt;name_client (str)&gt;</code>", parse_mode='html')
                log.error("Invalid arguments. Usage: /add <version (int)> <name_client (str)>")
