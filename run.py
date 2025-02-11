from bot import VersionsBot
from handlers import add_handler, rm_handler, get_handler, base_handlers


if __name__ == "__main__":
    UserBot_instance = VersionsBot()
    base_handlers.BaseHandlers(UserBot_instance.client).base_handlers()
    add_handler.Add(UserBot_instance.client).add_handler()
    rm_handler.Remove(UserBot_instance.client).rm_handler()
    get_handler.Get(UserBot_instance.client).get_handler()
    UserBot_instance.start()