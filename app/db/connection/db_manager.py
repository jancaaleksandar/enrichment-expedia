from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from sqlalchemy.orm.scoping import ScopedSession
from .connection_monitoring import setup_connection_monitoring


class DatabaseManager:
    _instance: Optional["DatabaseManager"] = None
    _engine: Optional[Engine] = None
    _session_factory: Optional[ScopedSession[Session]] = None
    
    @classmethod
    def get_database_url(cls) -> str:
        engine = "postgresql"
        username = "postgres"
        password = "fahsar-feSsys-zudfa7"
        host = "db.tocnkoahcwoqpsviisgk.supabase.co"
        port = "5432"
        dbname = "postgres"
        database_url = f"{engine}://{username}:{password}@{host}:{port}/{dbname}"
        return database_url

    @classmethod
    def get_instance(cls) -> "DatabaseManager":
        if cls._instance is None:
            cls._instance = DatabaseManager()
        return cls._instance

    def get_engine(self, pool_size: int = 1, max_overflow: int = 0) -> Engine:
        """
        Get or create a database engine with specified connection pool settings.

        Args:
            pool_size (int): The number of connections to keep open in the pool
            max_overflow (int): The maximum number of connections to allow in the pool "overflow"

        Returns:
            Engine: SQLAlchemy engine instance
        """
        # If we're requesting different pool settings and already have an engine,
        # dispose it to create a new one with the requested settings
        if self._engine is not None and (pool_size != 1 or max_overflow != 0):
            self.dispose_engine()

        if self._engine is None:
            try:

                database_url: str = self.get_database_url()

                # Configure engine with the specified connection pool settings
                self._engine = create_engine(
                    database_url,
                    pool_size=pool_size,
                    max_overflow=max_overflow,
                    pool_recycle=3600,
                    pool_pre_ping=True,
                    pool_use_lifo=True,
                    echo_pool=True
                )

                # Set up monitoring
                setup_connection_monitoring(self._engine)

                print(f"Database engine created with pool_size={pool_size}, max_overflow={max_overflow}")

            except Exception as e:
                print(f"Error creating database engine: {e}")
                raise ValueError(f"Error creating database engine: {e}")

        # mypy/pyright: self._engine is ensured to be set above
        assert self._engine is not None
        return self._engine

    def create_session(self, pool_size: int = 1, max_overflow: int = 0) -> Session:
        """
        Create a new database session with specified connection pool settings.

        Args:
            pool_size (int): The number of connections to keep open in the pool
            max_overflow (int): The maximum number of connections to allow in the pool "overflow"

        Returns:
            Session: SQLAlchemy session instance
        """
        # Get engine with specified pool settings
        engine = self.get_engine(
            pool_size=pool_size, max_overflow=max_overflow)

        # Create a new session factory if needed
        if self._session_factory is None:
            self._session_factory = scoped_session(sessionmaker(bind=engine))
        else:
            # Ensure the session factory is using the current engine
            self._session_factory.configure(bind=engine)

        session: Session = self._session_factory()
        print(f"Database session created with pool_size={pool_size}, max_overflow={max_overflow}")
        return session

    def dispose_engine(self) -> None:
        if self._engine is not None:
            try:
                self._engine.dispose()
                print("Database engine and connection pool disposed")
                self._engine = None
                self._session_factory = None
            except Exception as e:
                print(f"Error disposing database engine: {e}")

# Wrapper functions for backwards compatibility


def create_database_connection(pool_size: int = 1, max_overflow: int = 0) -> Session:
    """
    Create a new database session with specified connection pool settings.

    Args:
        pool_size (int): The number of connections to keep open in the pool
        max_overflow (int): The maximum number of connections to allow in the pool "overflow"

    Returns:
        Session: SQLAlchemy session instance
    """
    return DatabaseManager.get_instance().create_session(pool_size=pool_size, max_overflow=max_overflow)


def dispose_engine() -> None:
    DatabaseManager.get_instance().dispose_engine()
