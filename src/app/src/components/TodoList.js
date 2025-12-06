/**
 * TodoList Component
 * Displays a list of todos.
 * Pure presentational component - receives data via props.
 */

import React from "react";
import "./TodoList.css";

const TodoList = ({ todos, loading, onDelete }) => {
  if (loading && todos.length === 0) {
    return <div className="loading">Loading todos...</div>;
  }

  if (todos.length === 0) {
    return <div className="empty-state">No todos yet. Create one below!</div>;
  }

  return (
    <div className="todo-list">
      <h1>List of TODOs</h1>
      <ul>
        {todos.map((todo, idx) => (
          <li key={todo._id || idx} className="todo-item">
            <span className="todo-text">{todo.text}</span>
            <button
              onClick={() => onDelete(todo._id)}
              className="delete-btn"
              aria-label="Delete todo"
            >
              ×
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TodoList;
