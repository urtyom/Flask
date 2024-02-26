import atexit
import datetime
import os
from sqlalchemy import create_engine, String, DateTime, func
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped


POSTGRES_USER = os.getenv("POSTGRES_USER", "app")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "secret")
POSTGRES_DB = os.getenv("POSTGRES_DB", "app")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5431")

PG_DSN = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

engine = create_engine(PG_DSN)
Session = sessionmaker(bind=engine)

atexit.register(engine.dispose)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "app_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    registration_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    title: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(5000), unique=True, nullable=False)

    @property
    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'registration_time': self.registration_time.isoformat(),
            'title': self.title,
            'description': self.description
        }


Base.metadata.create_all(bind=engine)