import logging
from elasticsearch import Elasticsearch
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_elasticsearch():
    logger.info(f"Connecting to Elasticsearch at {settings.ELASTICSEARCH_URL}...")
    
    # Simple connection for local development over HTTP (no SSL)
    es = Elasticsearch(
        [settings.ELASTICSEARCH_URL],
        basic_auth=("elastic", "changeme"), # Dummy credentials
        verify_certs=False
    )

    index_name = "yelp_reviews"

    # Define the Review Index Mapping
    # Supports Hybrid Search: Keyword (BM25) + Semantic (Dense Vector)
    mapping = {
        "mappings": {
            "properties": {
                "review_id": {"type": "keyword"},
                "business_id": {"type": "keyword"},
                "user_id": {"type": "keyword"},
                "stars": {"type": "float"},
                "text": {
                    "type": "text", 
                    "analyzer": "standard",
                    "fields": {
                        "keyword": {"type": "keyword", "ignore_above": 256}
                    }
                },
                "date": {"type": "date"},
                # For semantic search over review text (e.g., using OpenAI embeddings)
                "text_vector": {
                    "type": "dense_vector",
                    "dims": 1536,  # Standard OpenAI embedding dimension
                    "index": True,
                    "similarity": "cosine"
                }
            }
        }
    }

    if es.indices.exists(index=index_name):
        logger.info(f"Index {index_name} already exists. Skipping creation.")
    else:
        logger.info(f"Creating index: {index_name}")
        es.indices.create(index=index_name, body=mapping)
        logger.info(f"Elasticsearch index {index_name} created successfully.")

if __name__ == "__main__":
    setup_elasticsearch()
