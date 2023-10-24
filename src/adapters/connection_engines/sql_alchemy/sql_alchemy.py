from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from ports.connection_engine import ConnectionEngine


class SQLAlchemy(ConnectionEngine):
    def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
        self.session_maker = session_maker

    @classmethod
    def start(cls, db_credentials: dict):
        database_url = URL.create(**db_credentials)
        engine = create_async_engine(database_url, echo=False, pool_size=10, max_overflow=20)
        async_session = async_sessionmaker(engine, expire_on_commit=False, autoflush=False, autocommit=False)
        return cls(async_session)
