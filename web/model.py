"""
Utilty module to store all the model functions.
"""
from datetime import datetime
from cassandra.cluster import Cluster
import os


def get_fic():
    """
    Returns the FIC for this site.
    """
    return os.environ['FIC']


def _get_session(keyspace='eagle'):
    server = os.environ['CASSANDRA_SERVER']
    cluster = Cluster([server])
    session = cluster.connect(keyspace=keyspace)
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


def init_cassandra():
    session = _get_session(None)
    keyspace_query = """
    CREATE KEYSPACE IF NOT EXISTS eagle 
    WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 1 };
    """

    session.execute(keyspace_query)
    session.execute("DROP TABLE IF EXISTS eagle.flights")

    table_query = """

    CREATE TABLE IF NOT EXISTS eagle.flights (id TIMEUUID PRIMARY KEY, acid text, state text, update_time timestamp);

    """
    session.execute(table_query)
