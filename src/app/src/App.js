import React from "react";
import "./App.css";
import useTodos from "./hooks/useTodos";
import TodoList from "./components/TodoList";
import TodoForm from "./components/TodoForm";
import ErrorMessage from "./components/ErrorMessage";

function App() {
  // Custom hook manages all todo state and logic
  const { todos, loading, error, addTodo, deleteTodo, clearError } = useTodos();

  return (
    <div className="App">
      {/* Error notification banner */}
      <ErrorMessage message={error} onDismiss={clearError} />

      {/* Display todos */}
      <TodoList todos={todos} loading={loading} onDelete={deleteTodo} />

      {/* Create new todo */}
      <TodoForm onSubmit={addTodo} disabled={loading} />
    </div>
  );
}

export default App;
