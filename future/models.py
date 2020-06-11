from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, MetaData
from sqlalchemy.orm import relationship
from geoalchemy2.types import Geometry
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from .database import Base



srid = 4326

metadata = MetaData()


class ConnectionNode(Base):
    __tablename__ = "connection_nodes"

    # why does connection node not has a code and zoom_category???

    id = Column(Integer, primary_key=True)
    storage_area = Column(Float)
    initial_waterlevel = Column(Float)
    the_geom = Column(
        Geometry(geometry_type="POINT", srid=srid, spatial_index=True, management=True),
        nullable=False,
    )
