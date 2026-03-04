import logging
from cassandra.cluster import Cluster
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_cassandra():
    logger.info(f"Connecting to Cassandra at {settings.CASSANDRA_CONTACT_POINTS}...")
    cluster = Cluster([settings.CASSANDRA_CONTACT_POINTS])
    session = cluster.connect()

    # 1. Create Keyspace
    logger.info(f"Creating keyspace: {settings.CASSANDRA_KEYSPACE}")
    session.execute(f"""
        CREATE KEYSPACE IF NOT EXISTS {settings.CASSANDRA_KEYSPACE}
        WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': '1'}}
    """)

    session.set_keyspace(settings.CASSANDRA_KEYSPACE)

    # 2. Create Business Attributes Table (EAV Layout)
    # This allows for high-scale, flexible attribute storage without schema migrations.
    logger.info("Creating business_attributes table...")
    session.execute("""
        CREATE TABLE IF NOT EXISTS business_attributes (
            business_id text,
            attribute_key text,
            attribute_value text,
            PRIMARY KEY (business_id, attribute_key)
        )
    """)

    # 3. Create Business Metadata Table (Static facts)
    logger.info("Creating business_metadata table...")
    session.execute("""
        CREATE TABLE IF NOT EXISTS business_metadata (
            business_id text PRIMARY KEY,
            name text,
            address text,
            city text,
            state text,
            stars float,
            review_count int,
            is_open int
        )
    """)

    logger.info("Cassandra setup complete.")
    cluster.shutdown()

if __name__ == "__main__":
    setup_cassandra()
