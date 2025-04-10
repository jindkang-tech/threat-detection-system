import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Dict, Any

from ..core.config import get_settings

settings = get_settings()

# Use SQLite for development
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, 'dev.db')
engine = create_engine(f'sqlite:///{DB_PATH}', connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Mock MongoDB client for development
class MockMongoClient:
    def __init__(self):
        self.data: Dict[str, Dict[str, Any]] = {}
    
    def get_default_database(self):
        return self
    
    def __getattr__(self, name):
        if name not in self.data:
            self.data[name] = {}
        return self
    
    async def insert_one(self, document):
        collection = self.data.get(self.__collection__, {})
        collection[str(len(collection))] = document
        self.data[self.__collection__] = collection
        return type('ObjectId', (), {'inserted_id': str(len(collection) - 1)})()
    
    async def find_one(self, query):
        collection = self.data.get(self.__collection__, {})
        for doc in collection.values():
            if all(doc.get(k) == v for k, v in query.items()):
                return doc
        return None

# Use mock clients
mongo_client = MockMongoClient()
mongo_db = mongo_client.get_default_database()
async_mongo_client = MockMongoClient()
async_mongo_db = async_mongo_client.get_default_database()

def get_db():
    """Get PostgreSQL database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_mongo_db():
    """Get MongoDB database connection"""
    return mongo_db

def get_async_mongo_db():
    """Get async MongoDB database connection"""
    return async_mongo_db
