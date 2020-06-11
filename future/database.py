from django.conf import settings
from sqlalchemy import create_engine
from sqlalchemy.event import listen
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# db = settings.DATABASES["default"]["NAME"]
db = './alch.sqlite'


def load_spatialite(dbapi_conn, connection_record):
    dbapi_conn.enable_load_extension(True)
    dbapi_conn.load_extension('/usr/lib/x86_64-linux-gnu/mod_spatialite.so')


engine = create_engine(
    f'sqlite:///{db}',
    echo=True,
    connect_args={
        "check_same_thread": False
    }
)

listen(engine, 'connect', load_spatialite)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
