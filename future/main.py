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


def get_connection_node(node_id: int):
    db = next(get_db())
    return db.query(models.ConnectionNode).filter(models.ConnectionNode.id == node_id).first()


def _create_db():
    conn = engine.connect()
    conn.execute(select([func.InitSpatialMetaData()]))
    models.Base.metadata.create_all(bind=engine)


def create_template_db():
    conn = engine.connect()
    conn.execute(select([func.InitSpatialMetaData()]))
    models.Base.metadata.create_all(bind=engine)
