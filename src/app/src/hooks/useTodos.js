// Custom hook for managing todo state
import { useState, useEffect, useCallback } from "react";
import todoApi, { ApiError } from "../services/todoApi";

const useTodos = () => {
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch all todos
  const fetchTodos = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const data = await todoApi.getAll();
      setTodos(data);
    } catch (err) {
      const errorMessage =
        err instanceof ApiError
          ? err.message
          : "Failed to load todos. Please try again.";
      setError(errorMessage);
      console.error("Error fetching todos:", err);
    } finally {
      setLoading(false);
    }
  }, []);

  // Add a new todo
  const addTodo = useCallback(
    async (text) => {
      if (!text || !text.trim()) {
        setError("Todo text cannot be empty");
        return false;
      }

      setLoading(true);
      setError(null);

      try {
        await todoApi.create(text);
        await fetchTodos();
        return true;
      } catch (err) {
        const errorMessage =
          err instanceof ApiError
            ? err.message
            : "Failed to create todo. Please try again.";
        setError(errorMessage);
        console.error("Error creating todo:", err);
        return false;
      } finally {
        setLoading(false);
      }
    },
    [fetchTodos]
  );

  // Delete a todo
  const deleteTodo = useCallback(
    async (todoId) => {
      setLoading(true);
      setError(null);

      try {
        await todoApi.delete(todoId);
        await fetchTodos();
        return true;
      } catch (err) {
        const errorMessage =
          err instanceof ApiError
            ? err.message
            : "Failed to delete todo. Please try again.";
        setError(errorMessage);
        console.error("Error deleting todo:", err);
        return false;
      } finally {
        setLoading(false);
      }
    },
    [fetchTodos]
  );

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  useEffect(() => {
    fetchTodos();
  }, [fetchTodos]);

  return {
    todos,
    loading,
    error,
    addTodo,
    deleteTodo,
    refreshTodos: fetchTodos,
    clearError,
  };
};

export default useTodos;
