"""
Utilty module to store all the model functions.
"""
from datetime import datetime
from cassandra.cluster import Cluster


def _get_session():
    cluster = Cluster(['cassandra1'])
    session = cluster.connect(keyspace='eagle')
    return session


def get_flights():
    session = _get_session()
    rows = session.execute("""SELECT id, acid, state, update_time
    FROM eagle.flights""")
    return rows


def save_flight(acid, state):
    session = _get_session()    
    session.execute(
        """
        INSERT INTO eagle.flights (id, acid, state, update_time)
        VALUES (now(), %s, %s, %s)
        """,
        (acid, state, datetime.now())
        )
