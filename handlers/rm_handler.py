from telethon import events
from logs.logger import log
from utils.ArgsFromAddAndRm import get_args_from_add_and_rm
from data.cfg import Config

import argparse


from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from db.database import Versions, get_db


class Remove:
    def __init__(self,
                 client,
                 db_session: Session = next(get_db())):

        self.client = client
        self.staff_ids = Config.get_value('bot')['staff_ids']
        self.db_session = db_session

    def rm_handler(self):
        @self.client.on(events.NewMessage(pattern=r'^\/(?i:rm)(.*)'))
        async def rm_handler(msg):

            if msg.sender_id not in self.staff_ids:
                await msg.reply("You don't have permission to use this command.")
                log.warning(f"User ID: {str(msg.sender_id)} tried to use add_handler but was not in staff_id list")
                return

            log.info(f"User ID: {str(msg.sender_id)} using rm_handler")

            parser = get_args_from_add_and_rm(msg)

            args = msg.text.split()[1:]  # Splitting the message text to extract arguments
            try:
                parsed_args = parser.parse_args(args)
                version = parsed_args.version
                name_client = parsed_args.name_client

                try:
                    # Attempt to delete the record from the database
                    client_record = self.db_session.query(Versions).filter_by(number=version, name=name_client).one()
                    self.db_session.delete(client_record)
                    self.db_session.commit()

                    log.debug(f"Deleted client with Version: {version}, Client Name: {name_client}")
                    await msg.reply(f"Client with Version: {version}, Client Name: {name_client} has been deleted successfully.")

                except NoResultFound:
                    await msg.reply("No record found with the given version and client name.")
                    log.error(f"No record found with Version: {version}, Client Name: {name_client}")

            except SystemExit:
                await msg.reply("Invalid arguments. Usage: <code>/rm &lt;version (int)&gt; &lt;name_client (str)&gt;</code>",
                    parse_mode='html')
                log.warning("Invalid arguments. Usage: /rm <version (int)> <name_client (str)>")
