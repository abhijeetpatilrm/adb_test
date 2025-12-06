# API views for todo endpoints
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging

from .database import db_connection
from .repositories import TodoRepository
from .services import TodoService, ValidationError

logger = logging.getLogger(__name__)


class TodoListView(APIView):
    """Handles GET and POST for /todos/"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db = db_connection.get_database()
        repository = TodoRepository(db)
        self.service = TodoService(repository)

    def get(self, request):
        """List all todos"""
        try:
            todos = self.service.get_all_todos()
            return Response(todos, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Unexpected error in GET /todos/: {e}")
            return Response(
                {"error": "Failed to fetch todos. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        """Create a new todo"""
        try:
            text = request.data.get("text", "")
            todo = self.service.create_todo(text)
            return Response(todo, status=status.HTTP_201_CREATED)
            
        except ValidationError as e:
            logger.warning(f"Validation error in POST /todos/: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        except Exception as e:
            logger.error(f"Unexpected error in POST /todos/: {e}")
            return Response(
                {"error": "Failed to create todo. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TodoDetailView(APIView):
    """Handles DELETE for /todos/<id>/"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db = db_connection.get_database()
        repository = TodoRepository(db)
        self.service = TodoService(repository)
    
    def delete(self, request, todo_id):
        """Delete a todo by ID"""
        try:
            self.service.delete_todo(todo_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
            
        except ValidationError as e:
            logger.warning(f"Validation error in DELETE /todos/{todo_id}/: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        except Exception as e:
            logger.error(f"Unexpected error in DELETE /todos/{todo_id}/: {e}")
            return Response(
                {"error": "Failed to delete todo. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

