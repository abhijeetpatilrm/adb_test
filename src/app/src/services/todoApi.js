// API service for handling all backend communication
import config from "../config";

// Custom error for API failures
export class ApiError extends Error {
  constructor(message, status, data = null) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.data = data;
  }
}

// Handles fetch requests with timeout and error handling
const makeRequest = async (endpoint, options = {}) => {
  const url = `${config.apiBaseUrl}${endpoint}`;

  const headers = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(
      () => controller.abort(),
      config.requestTimeout
    );

    const response = await fetch(url, {
      ...options,
      headers,
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new ApiError(
        errorData.error || `HTTP ${response.status}: ${response.statusText}`,
        response.status,
        errorData
      );
    }

    return await response.json();
  } catch (error) {
    if (error.name === "AbortError") {
      throw new ApiError("Request timeout. Please check your connection.", 408);
    }

    if (error instanceof ApiError) {
      throw error;
    }

    throw new ApiError(
      "Network error. Please check your connection and try again.",
      0,
      { originalError: error.message }
    );
  }
};

// Todo API methods
const todoApi = {
  getAll: async () => {
    return makeRequest(config.endpoints.todos, {
      method: "GET",
    });
  },

  create: async (text) => {
    return makeRequest(config.endpoints.todos, {
      method: "POST",
      body: JSON.stringify({ text }),
    });
  },

  delete: async (todoId) => {
    return makeRequest(`${config.endpoints.todos}${todoId}/`, {
      method: "DELETE",
    });
  },
};

export default todoApi;
