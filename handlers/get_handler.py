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

            async def send_long_message(text):
                MAX_MESSAGE_LENGTH = 4000
                messages = []
                current_message = ""
                
                for line in text.split('\n'):
                    if len(current_message) + len(line) + 1 > MAX_MESSAGE_LENGTH:
                        messages.append(current_message)
                        current_message = line + '\n'
                    else:
                        current_message += line + '\n'
                
                if current_message:
                    messages.append(current_message)
                
                for message in messages:
                    await msg.reply(message, parse_mode='html')

            if len(args) == 0:
                # Display all versions and clients from the database
                versions = self.db_session.query(Versions).all()
                res += "<pre><code class=\"language-DataBase\">"
                sorted_versions = sorted(set(v.number for v in versions), reverse=True)
                for version in sorted_versions:
                    res += f"❯ Version: {version}\n"
                    clients = sorted([v for v in versions if v.number == version], key=lambda x: x.name)
                    for client in clients:
                        res += f"    ❖ Client name: {client.name}({client.create_username})\n"
                    res += "\n"
                res += "</code></pre>\n"
                await send_long_message(res)
            elif len(args) == 1:
                # Check if the argument is a version number
                if args[0].isdigit():
                    version = args[0]
                    clients = self.db_session.query(Versions).filter_by(number=version).order_by(Versions.name).all()
                    res += f"<pre><code class=\"language-DataBase\">❯ Version: {version}\n"
                    for client in clients:
                        res += f"    ❖ Client name: {client.name}({client.create_username})\n"
                    res += "</code></pre>"
                    await send_long_message(res)
                else:
                    # Assume it's a client name
                    client_name = args[0]
                    versions = self.db_session.query(Versions).filter_by(name=client_name).order_by(Versions.number.desc()).all()
                    res += f"<pre><code class=\"language-DataBase\">❯ Client name: {client_name}\n"
                    for version in set(v.number for v in versions):
                        res += f"    ❖ Version: {version}\n"
                    res += "</code></pre>"
                    await send_long_message(res)
            elif len(args) == 2:
                # Display a specific version and client from the database
                version = args[0]
                client_name = args[1]
                client = self.db_session.query(Versions).filter_by(number=version, name=client_name).first()
                if client:
                    await msg.reply(f"❯ Version: {version}\n    ❖ Client name: {client.name}({client.create_username})")
                else:
                    await msg.reply(f"Client name: {client_name} not found for version {version}")
