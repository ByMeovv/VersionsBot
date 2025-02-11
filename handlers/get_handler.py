from telethon import events
from logs.logger import log
from sqlalchemy.orm import Session
from db.database import get_db, Versions


class Get:
    def __init__(self, client, db_session: Session = next(get_db())):
        """
        Initialize the Get handler with the client.
        """
        self.client = client
        self.db_session = db_session

    def get_handler(self):
        @self.client.on(events.NewMessage(pattern=r'^\/(?i:get)(.*)'))
        async def get_handler(msg):
            log.info(f"User ID: {str(msg.sender_id)} using get_handler")

            args = msg.text.split()[1:]
            res = ""

            if len(args) == 0:
                # Display all versions and clients from the database
                versions = self.db_session.query(Versions).all()
                res += "<pre><code class=\"language-DataBase\">"
                for version in set(v.number for v in versions):
                    res += f"❯ Version: {version}\n"
                    clients = [v for v in versions if v.number == version]
                    for client in clients:
                        res += f"    ❖ Client name: {client.name}({client.create_username})\n"
                    res += "\n"
                res += "</code></pre>\n"
                await msg.reply(res, parse_mode='html')
            elif len(args) == 1:
                # Check if the argument is a version number
                if args[0].isdigit():
                    version = args[0]
                    clients = self.db_session.query(Versions).filter_by(number=version).all()
                    res += f"<pre><code class=\"language-DataBase\">❯ Version: {version}\n"
                    for client in clients:
                        res += f"    ❖ Client name: {client.name}({client.create_username})\n"
                    res += "</code></pre>"
                    await msg.reply(res, parse_mode='html')
                else:
                    # Assume it's a client name
                    client_name = args[0]
                    versions = self.db_session.query(Versions).filter_by(name=client_name).all()
                    res += f"<pre><code class=\"language-DataBase\">❯ Client name: {client_name}\n"
                    for version in set(v.number for v in versions):
                        res += f"    ❖ Version: {version}\n"
                    res += "</code></pre>"
                    await msg.reply(res, parse_mode='html')
            elif len(args) == 2:
                # Display a specific version and client from the database
                version = args[0]
                client_name = args[1]
                client = self.db_session.query(Versions).filter_by(number=version, name=client_name).first()
                if client:
                    await msg.reply(f"❯ Version: {version}\n    ❖ Client name: {client.name}({client.create_username})")
                else:
                    await msg.reply(f"Client name: {client_name} not found for version {version}")
