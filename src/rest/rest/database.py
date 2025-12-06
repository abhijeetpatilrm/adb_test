"""
Database connection management.
Centralizes MongoDB connection logic and provides a single source of truth.
"""
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import logging

logger = logging.getLogger(__name__)


class DatabaseConnection:
    """
    Manages MongoDB connection using singleton pattern.
    Ensures single connection instance across the application.
    """
    _instance = None
    _client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance

    def get_client(self):
        """
        Returns MongoDB client, creating it if necessary.
        Lazy initialization ensures connection only when needed.
        """
        if self._client is None:
            try:
                mongo_host = os.environ.get('MONGO_HOST', 'localhost')
                mongo_port = os.environ.get('MONGO_PORT', '27017')
                mongo_uri = f'mongodb://{mongo_host}:{mongo_port}'
                
                self._client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
                # Verify connection
                self._client.admin.command('ping')
                logger.info(f"Connected to MongoDB at {mongo_uri}")
                
            except ConnectionFailure as e:
                logger.error(f"Failed to connect to MongoDB: {e}")
                raise
            except KeyError as e:
                logger.error(f"Missing environment variable: {e}")
                raise
                
        return self._client

    def get_database(self, db_name='test_db'):
        """Returns the specified database."""
        return self.get_client()[db_name]


# Singleton instance
db_connection = DatabaseConnection()
