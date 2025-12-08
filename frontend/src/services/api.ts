/**
 * API Service for CodeInterview Backend
 * Follows OpenAPI specification at /openapi.yaml
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

// Types for API responses
interface ApiErrorResponse {
  error: string;
  message: string;
  statusCode: number;
}

class ApiError extends Error {
  constructor(
    public statusCode: number,
    public errorCode: string,
    message: string
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

// Helper function to handle API responses
async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let errorData: ApiErrorResponse;
    try {
      errorData = await response.json();
    } catch {
      throw new ApiError(
        response.status,
        'UNKNOWN_ERROR',
        `HTTP ${response.status}: ${response.statusText}`
      );
    }
    throw new ApiError(
      errorData.statusCode || response.status,
      errorData.error,
      errorData.message
    );
  }

  // Handle 204 No Content
  if (response.status === 204) {
    return undefined as T;
  }

  return response.json();
}

/**
 * Sessions API
 */
export const sessionsApi = {
  /**
   * Create a new interview session
   * POST /api/v1/sessions
   */
  async create(language?: string, code?: string) {
    const response = await fetch(`${API_BASE_URL}/sessions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        language: language || 'javascript',
        code: code || '// Start coding here\nconsole.log("Hello, World!");',
      }),
    });
    return handleResponse(response);
  },

  /**
   * Get session details
   * GET /api/v1/sessions/{sessionId}
   */
  async get(sessionId: string) {
    const response = await fetch(`${API_BASE_URL}/sessions/${sessionId}`);
    return handleResponse(response);
  },

  /**
   * Update session
   * PATCH /api/v1/sessions/{sessionId}
   */
  async update(
    sessionId: string,
    data: { code?: string; language?: string; status?: string }
  ) {
    const response = await fetch(`${API_BASE_URL}/sessions/${sessionId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return handleResponse(response);
  },

  /**
   * Delete session
   * DELETE /api/v1/sessions/{sessionId}
   */
  async delete(sessionId: string) {
    const response = await fetch(`${API_BASE_URL}/sessions/${sessionId}`, {
      method: 'DELETE',
    });
    return handleResponse(response);
  },
};

/**
 * Users API
 */
export const usersApi = {
  /**
   * Join a session
   * POST /api/v1/sessions/{sessionId}/users
   */
  async join(sessionId: string, name?: string) {
    const response = await fetch(
      `${API_BASE_URL}/sessions/${sessionId}/users`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(name ? { name } : {}),
      }
    );
    return handleResponse(response);
  },

  /**
   * Get all users in a session
   * GET /api/v1/sessions/{sessionId}/users
   */
  async list(sessionId: string) {
    const response = await fetch(
      `${API_BASE_URL}/sessions/${sessionId}/users`
    );
    return handleResponse(response);
  },

  /**
   * Leave a session
   * DELETE /api/v1/sessions/{sessionId}/users/{userId}
   */
  async leave(sessionId: string, userId: string) {
    const response = await fetch(
      `${API_BASE_URL}/sessions/${sessionId}/users/${userId}`,
      {
        method: 'DELETE',
      }
    );
    return handleResponse(response);
  },
};

/**
 * Code Execution API
 */
export const executionApi = {
  /**
   * Execute code
   * POST /api/v1/execute
   */
  async execute(code: string, language: string, timeout?: number) {
    const response = await fetch(`${API_BASE_URL}/execute`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        code,
        language,
        timeout: timeout || 30000,
      }),
    });
    return handleResponse(response);
  },
};

/**
 * Health Check API
 */
export const healthApi = {
  /**
   * Health check
   * GET /api/v1/health
   */
  async check() {
    const response = await fetch(`${API_BASE_URL}/health`);
    return handleResponse(response);
  },
};

export { ApiError };
