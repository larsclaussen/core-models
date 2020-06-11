from contextlib import contextmanager

from pathlib import Path
from functools import cached_property
from django.conf import settings
from sqlalchemy import create_engine
from sqlalchemy.event import listen
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# db = settings.DATABASES["default"]["NAME"]
db = '/code/future/templates/threedi_model_template.sqlite'

Base = declarative_base()


def load_spatialite(dbapi_conn, connection_record):
    dbapi_conn.enable_load_extension(True)
    dbapi_conn.load_extension('/usr/lib/x86_64-linux-gnu/mod_spatialite.so')


class SqliteDatabase:

    def __init__(self, sqlite_db: Path):
        self.sqlite_db = sqlite_db
        listen(self.engine, 'connect', load_spatialite)
        self._session = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    @cached_property
    def engine(self):
        return create_engine(
            f'sqlite:///{self.sqlite_db}',
            echo=True,
            connect_args={
                "check_same_thread": False
            }
        )

    @contextmanager
    def session(self):
        s = self._session()
        try:
            yield s
        finally:
            s.close()
