"""
Repository layer for Todo data access.
Implements the Repository pattern to abstract database operations.
This separation allows easy testing and potential database swapping.
"""
from typing import List, Dict, Optional
from bson.objectid import ObjectId
from pymongo.errors import PyMongoError
import logging

logger = logging.getLogger(__name__)


class TodoRepository:
    """
    Handles all database operations for Todo entities.
    Follows the Repository pattern for clean separation of concerns.
    """
    
    def __init__(self, database):
        """
        Initialize repository with database instance.
        
        Args:
            database: MongoDB database instance
        """
        self.collection = database['todos']

    def find_all(self) -> List[Dict]:
        """
        Retrieve all todos from database.
        
        Returns:
            List of todo dictionaries with string IDs
            
        Raises:
            PyMongoError: If database query fails
        """
        try:
            # Convert ObjectId to string for JSON serialization
            todos = list(self.collection.find({}))
            for todo in todos:
                if '_id' in todo:
                    todo['_id'] = str(todo['_id'])
            return todos
        except PyMongoError as e:
            logger.error(f"Error fetching todos from database: {e}")
            raise

    def create(self, todo_data: Dict) -> Dict:
        """
        Insert a new todo into database.
        
        Args:
            todo_data: Dictionary containing todo fields
            
        Returns:
            Created todo with generated ID
            
        Raises:
            PyMongoError: If database insert fails
        """
        try:
            result = self.collection.insert_one(todo_data)
            todo_data['_id'] = str(result.inserted_id)
            return todo_data
        except PyMongoError as e:
            logger.error(f"Error creating todo in database: {e}")
            raise

    def find_by_id(self, todo_id: str) -> Optional[Dict]:
        """
        Find a specific todo by ID.
        
        Args:
            todo_id: String representation of ObjectId
            
        Returns:
            Todo dictionary or None if not found
        """
        try:
            todo = self.collection.find_one({'_id': ObjectId(todo_id)})
            if todo:
                todo['_id'] = str(todo['_id'])
            return todo
        except PyMongoError as e:
            logger.error(f"Error finding todo by ID: {e}")
            raise

    def delete(self, todo_id: str) -> bool:
        """
        Delete a todo by ID.
        
        Args:
            todo_id: String representation of ObjectId
            
        Returns:
            True if deleted, False if not found
        """
        try:
            result = self.collection.delete_one({'_id': ObjectId(todo_id)})
            return result.deleted_count > 0
        except PyMongoError as e:
            logger.error(f"Error deleting todo: {e}")
            raise
