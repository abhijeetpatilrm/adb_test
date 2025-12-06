"""
Business logic layer for Todo operations.
Implements Single Responsibility Principle by separating business rules
from data access and HTTP concerns.
"""
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class TodoService:
    """
    Encapsulates business logic for Todo operations.
    This layer validates input and orchestrates repository calls.
    """
    
    def __init__(self, repository):
        """
        Initialize service with repository dependency.
        Dependency injection makes this testable and flexible.
        
        Args:
            repository: TodoRepository instance
        """
        self.repository = repository

    def get_all_todos(self) -> List[Dict]:
        """
        Retrieve all todos.
        
        Returns:
            List of todo dictionaries
            
        Raises:
            Exception: If repository operation fails
        """
        try:
            return self.repository.find_all()
        except Exception as e:
            logger.error(f"Service error fetching todos: {e}")
            raise

    def create_todo(self, text: str) -> Dict:
        """
        Create a new todo with validation.
        
        Args:
            text: Todo text content
            
        Returns:
            Created todo dictionary
            
        Raises:
            ValidationError: If input validation fails
            Exception: If repository operation fails
        """
        # Business rule: text must be non-empty
        if not text or not isinstance(text, str):
            raise ValidationError("Todo text is required and must be a string")
        
        cleaned_text = text.strip()
        if not cleaned_text:
            raise ValidationError("Todo text cannot be empty or whitespace only")
        
        # Business rule: reasonable length limit
        if len(cleaned_text) > 500:
            raise ValidationError("Todo text cannot exceed 500 characters")
        
        try:
            todo_data = {"text": cleaned_text}
            return self.repository.create(todo_data)
        except Exception as e:
            logger.error(f"Service error creating todo: {e}")
            raise

    def get_todo_by_id(self, todo_id: str) -> Dict:
        """
        Retrieve a specific todo.
        
        Args:
            todo_id: Todo identifier
            
        Returns:
            Todo dictionary or None
        """
        if not todo_id:
            raise ValidationError("Todo ID is required")
        
        try:
            return self.repository.find_by_id(todo_id)
        except Exception as e:
            logger.error(f"Service error fetching todo by ID: {e}")
            raise

    def delete_todo(self, todo_id: str) -> bool:
        """
        Delete a todo.
        
        Args:
            todo_id: Todo identifier
            
        Returns:
            True if deleted successfully
        """
        if not todo_id:
            raise ValidationError("Todo ID is required")
        
        try:
            return self.repository.delete(todo_id)
        except Exception as e:
            logger.error(f"Service error deleting todo: {e}")
            raise
