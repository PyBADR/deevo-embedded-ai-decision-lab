from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from app.config import settings
from app.utils.logging import get_logger
from datetime import datetime
from typing import Optional

logger = get_logger(__name__)

class MongoDBClient:
    def __init__(self):
        self.client: Optional[MongoClient] = None
        self.db: Optional[Database] = None
        self.collection: Optional[Collection] = None
        self._connect()
    
    def _connect(self):
        try:
            self.client = MongoClient(settings.MONGODB_URI)
            self.db = self.client.get_default_database()
            self.collection = self.db.raw_claims
            logger.info("MongoDB connected successfully")
        except Exception as e:
            logger.error(f"MongoDB connection failed: {e}")
            self.client = None
    
    def is_connected(self) -> bool:
        return self.client is not None
    
    def store_claim(self, claim_id: str, customer_id: str, payload: dict, decision_id: str):
        if not self.is_connected():
            logger.warning("MongoDB not connected, skipping claim storage")
            return
        
        try:
            document = {
                "claim_id": claim_id,
                "customer_id": customer_id,
                "payload": payload,
                "decision_id": decision_id,
                "received_at": datetime.utcnow()
            }
            self.collection.insert_one(document)
            logger.info(f"Stored claim {claim_id} in MongoDB")
        except Exception as e:
            logger.error(f"Failed to store claim in MongoDB: {e}")

mongo_client = MongoDBClient()
