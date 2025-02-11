from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, func, BigInteger, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from data.cfg import Config

DATABASE_URL = f"postgresql://{Config.get_value('db')['postgres_user']}:{Config.get_value('db')['postgres_password']}@{Config.get_value('db')['host_name']}:{Config.get_value('db')['port']}/{Config.get_value('db')['postgres_db']}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

current_date = datetime.now()
formatted_date = current_date.strftime("%Y-%m-%d %H:%M:%S")


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
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
