from .database import SessionLocal, engine
from . import models
from sqlalchemy.orm import Session
from sqlalchemy.sql import select, func


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# dev function
def get_connection_node(node_id: int):
    db = next(get_db())
    return db.query(models.ConnectionNode).filter(models.ConnectionNode.id == node_id).first()


def _create_db():
    conn = engine.connect()
    conn.execute(select([func.InitSpatialMetaData()]))


def create_template_db():
    _create_db()
    # TODO enable once the models are define or run with alembic
    # models.Base.metadata.create_all(bind=engine)
