import json
import logging
import ijson  # Better for large JSON files
from cassandra.cluster import Cluster
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def ingest_business_data(file_path: str, limit: int = 1000):
    logger.info(f"Connecting to Cassandra at {settings.CASSANDRA_CONTACT_POINTS}...")
    cluster = Cluster([settings.CASSANDRA_CONTACT_POINTS])
    session = cluster.connect(settings.CASSANDRA_KEYSPACE)

    # 1. Pre-prepared Statements
    # Metadata Insert
    metadata_stmt = session.prepare("""
        INSERT INTO business_metadata (business_id, name, address, city, state, stars, review_count, is_open)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """)

    # Attribute (EAV) Insert
    attribute_stmt = session.prepare("""
        INSERT INTO business_attributes (business_id, attribute_key, attribute_value)
        VALUES (?, ?, ?)
    """)

    count = 0
    with open(file_path, 'r') as f:
        # Each line is a JSON object in the Yelp dataset
        for line in f:
            if count >= limit:
                break
            
            try:
                data = json.loads(line)
                
                # Insert metadata
                session.execute(metadata_stmt, (
                    data['business_id'],
                    data['name'],
                    data.get('address', ''),
                    data.get('city', ''),
                    data.get('state', ''),
                    float(data.get('stars', 0.0)),
                    int(data.get('review_count', 0)),
                    int(data.get('is_open', 1))
                ))

                # Insert attributes (EAV Layout)
                attributes = data.get('attributes', {})
                if attributes:
                    for key, value in attributes.items():
                        # Flatten dictionary values (e.g., {'WiFi': 'free'} -> WiFi: free)
                        if isinstance(value, str) and value.startswith('{'):
                            try:
                                nested_val = json.loads(value.replace("'", '"'))
                                for k, v in nested_val.items():
                                    session.execute(attribute_stmt, (data['business_id'], f"{key}_{k}", str(v)))
                            except:
                                session.execute(attribute_stmt, (data['business_id'], key, str(value)))
                        else:
                            session.execute(attribute_stmt, (data['business_id'], key, str(value)))

                count += 1
                if count % 100 == 0:
                    logger.info(f"Ingested {count} businesses...")

            except Exception as e:
                logger.error(f"Error ingesting business: {e}")
                continue

    logger.info(f"Ingestion complete. Total: {count} businesses.")
    cluster.shutdown()

if __name__ == "__main__":
    file_path = "yelp-dataset/yelp_academic_dataset_business.json"
    ingest_business_data(file_path, limit=5000)
