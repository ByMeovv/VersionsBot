from sqlalchemy.event import listens_for
from sqlalchemy.exc import DisconnectionError
from sqlalchemy.exc import PendingRollbackError
from sqlalchemy.pool import Pool
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime, BigInteger, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from data.cfg import Config

db_conf = Config.get_value('bot')['db']

DATABASE_URL = f"postgresql://{db_conf['user']}:{db_conf['password']}@{db_conf['host']}:{db_conf['port']}/{db_conf['db']}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

current_date = datetime.now()
formatted_date = current_date.strftime("%Y-%m-%d %H:%M:%S")


@listens_for(Pool, "checkout")
def ping_connection(dbapi_connection, connection_record, connection_proxy):
    """Event listener that pings every new database connection.

    This function will run for each new connection, and will ensure that the
    connection is still alive.

    If the connection is dead (i.e. the server went down), then a new connection
    will be attempted.
    """
    cursor = dbapi_connection.cursor()
    try:
        cursor.execute("SELECT 1")
    except:
        # If the connection is dead, then raise a DisconnectionError.
        raise DisconnectionError()
    cursor.close()


class Versions(Base):

    """
    Table for clients versions

    Attributes:
        number (int): Client number
        name (str): Client name
        version (int): Client version
        create_id (int): Telegram ID of user who created the record
        create_username (str): Telegram username of user who created the record
        created_at (datetime): Date when record was created
    """

    __tablename__ = "clients"

    _id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, nullable=False, index=True)
    name = Column(VARCHAR, index=True)
    create_id = Column(BigInteger, nullable=False, index=True)
    create_username = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, default=formatted_date)


Base.metadata.create_all(bind=engine)

def get_db():
    """
    Yields a database session.

    This function is a generator. It starts a database session, yields it,
    and then closes the session when the generator is exhausted.

    Examples
    --------
    >>> with get_db() as db:
    ...     version = db.query(Versions).first()
    """
    while True:
        db = None
        try:
            db = SessionLocal()
            yield db
        except DisconnectionError:
            if db is not None:
                db.close()
            continue
        except PendingRollbackError:
            if db is not None:
                db.rollback()
            continue
        except Exception as e:
            if db is not None:
                db.rollback()
            raise e
        finally:
            if db is not None:
                db.close()
        break
