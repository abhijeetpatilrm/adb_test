# Architecture Overview

This TODO application uses a **layered architecture** with clear separation of concerns between frontend and backend components.

## Backend Architecture (Django + MongoDB)

The backend follows a three-layer pattern:

```
HTTP Request → Views → Service → Repository → MongoDB
```

**Views (`views.py`):** Handle HTTP requests and responses
**Service (`services.py`):** Business logic and validation
**Repository (`repositories.py`):** Database operations

This separation ensures each component has a single responsibility, making the code easier to test and maintain.

## Frontend Architecture (React)

The frontend uses React Hooks with a clean component structure:

```
User Action → Component → Custom Hook → API Service → Backend
```

**Components:** UI presentation (TodoList, TodoForm)
**Custom Hook (`useTodos.js`):** State management and business logic
**API Service (`todoApi.js`):** HTTP communication with backend

All components are functional with hooks (no class components), following React best practices.

## How It Works

When a user adds a todo:

1. User submits form → `TodoForm` component
2. Calls `addTodo()` from `useTodos` hook
3. Hook calls `todoApi.create()` to send POST request
4. Django `views.py` receives request
5. `TodoService` validates the input
6. `TodoRepository` saves to MongoDB
7. Response flows back to frontend
8. Hook refreshes the list with `fetchTodos()`
9. UI updates with new todo

## Design Principles

- **Single Responsibility:** Each component/class has one clear job
- **Dependency Inversion:** High-level code doesn't depend on low-level details
- **Error Handling:** Proper validation, logging, and user-friendly messages
- **Separation of Concerns:** Business logic, data access, and presentation are separated

## Docker Setup

Three containers work together:

- **app** (port 3000): React development server
- **api** (port 8000): Django backend server
- **mongo** (port 27017): MongoDB database

Volume mounts enable live code reloading during development.
