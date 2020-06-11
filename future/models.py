from geoalchemy2.types import Geometry
from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import MetaData

from .database import Base

srid = 4326

metadata = MetaData()


class ConnectionNode(Base):

    __tablename__ = "connection_nodes"

    id = Column(Integer, primary_key=True)
    storage_area = Column(Float)
    initial_waterlevel = Column(Float)
    the_geom = Column(
        Geometry(geometry_type="POINT", srid=srid, spatial_index=True, management=True),
        nullable=False,
    )
