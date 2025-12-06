/**
 * TodoForm Component
 * Handles todo creation form.
 * Presentational component that delegates business logic to parent.
 */

import React, { useState } from "react";
import "./TodoForm.css";

const TodoForm = ({ onSubmit, disabled }) => {
  const [inputValue, setInputValue] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Call parent's submit handler
    const success = await onSubmit(inputValue);

    // Clear input only on success
    if (success) {
      setInputValue("");
    }
  };

  return (
    <div className="todo-form">
      <h1>Create a ToDo</h1>
      <form onSubmit={handleSubmit}>
        <label htmlFor="todo">ToDo: </label>
        <input
          id="todo"
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Enter todo description..."
          disabled={disabled}
          maxLength={500}
        />
        <button
          type="submit"
          disabled={disabled || !inputValue.trim()}
          className="submit-button"
        >
          {disabled ? "Adding..." : "Add ToDo!"}
        </button>
      </form>
    </div>
  );
};

export default TodoForm;
