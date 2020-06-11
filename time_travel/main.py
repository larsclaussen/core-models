from typing import List
from legacy.models import V2ConnectionNode
from future.main import get_db
from future.models import ConnectionNode
from future.main import create_db


def swap_node_data():
    create_db()
    c = []
    future_fields = ConnectionNode.__table__.columns.keys()
    qs = V2ConnectionNode.objects.all().only(*future_fields)
    for entry in qs:
        kwargs = {}
        for k, v in entry.__dict__.items():
            if k.startswith("_"):
                continue
            if "geom" in k:
                kwargs[k] = v.ewkt
                continue
            else:
                kwargs[k] = v
        # kwargs = {k: v for k, v in entry.__dict__.items() if not k.startswith("_")}
        cn_future = ConnectionNode(**kwargs)
        c.append(cn_future)
    add_nodes(c)


def add_nodes(nodes: List):
    session = next(get_db())
    session.add_all(nodes)
    session.commit()
