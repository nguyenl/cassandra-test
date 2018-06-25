from datetime import datetime
from cassandra.cluster import Cluster

cluster = Cluster(['cassandra1'])
session = cluster.connect()

keyspace_query = """
CREATE KEYSPACE IF NOT EXISTS eagle 
   WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 1 };
"""

rows = session.execute(keyspace_query)
rows = session.execute("DROP TABLE IF EXISTS eagle.flights")

table_query = """

CREATE TABLE IF NOT EXISTS eagle.flights (id TIMEUUID PRIMARY KEY, acid text, state text, update_time timestamp);

"""

rows = session.execute(table_query)

session.execute(
    """
    INSERT INTO eagle.flights (id, acid, state, update_time)
    VALUES (now(), %s, %s, %s)
    """,
    ("ABC123", "FILED", datetime.now())
)

rows = session.execute('SELECT id, acid, state, update_time FROM eagle.flights')
for row in rows:
    print(row)
