/**
 * Configuration management for the application.
 * Centralizes environment-specific settings.
 */

const config = {
  // API base URL - can be overridden via environment variable
  apiBaseUrl: process.env.REACT_APP_API_URL || "http://localhost:8000",

  // API endpoints
  endpoints: {
    todos: "/todos/",
  },

  // Request timeout in milliseconds
  requestTimeout: 10000,
};

export default config;
