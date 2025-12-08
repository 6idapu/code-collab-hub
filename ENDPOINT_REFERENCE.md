# API Endpoint Reference Guide

## Quick Reference

### Base URL
```
Development: http://localhost:8000
Production: https://api.codeinterview.app
API Version: v1
```

---

## Endpoints Overview

### 🏢 Sessions Management

| Method | Endpoint | Purpose | Status Codes |
|--------|----------|---------|--------------|
| POST | `/api/v1/sessions` | Create new session | 201, 400, 500 |
| GET | `/api/v1/sessions/{sessionId}` | Get session details | 200, 404, 500 |
| PATCH | `/api/v1/sessions/{sessionId}` | Update session | 200, 400, 404, 500 |
| DELETE | `/api/v1/sessions/{sessionId}` | Delete session | 204, 404, 500 |

### 👥 User Management

| Method | Endpoint | Purpose | Status Codes |
|--------|----------|---------|--------------|
| POST | `/api/v1/sessions/{sessionId}/users` | Join session | 201, 400, 404, 409, 500 |
| GET | `/api/v1/sessions/{sessionId}/users` | Get session users | 200, 404, 500 |
| DELETE | `/api/v1/sessions/{sessionId}/users/{userId}` | Leave session | 204, 404, 500 |

### ⚙️ Code Execution

| Method | Endpoint | Purpose | Status Codes |
|--------|----------|---------|--------------|
| POST | `/api/v1/execute` | Execute code | 200, 400, 408, 500 |

### 🏥 Health

| Method | Endpoint | Purpose | Status Codes |
|--------|----------|---------|--------------|
| GET | `/api/v1/health` | Health check | 200 |

---

## Detailed Endpoint Documentation

### CREATE SESSION
```
POST /api/v1/sessions
```

**Request Body** (optional):
```json
{
  "language": "javascript",
  "code": "// Start coding here\nconsole.log(\"Hello, World!\");"
}
```

**Success Response** (201):
```json
{
  "id": "abcdef1234",
  "code": "// Start coding here\nconsole.log(\"Hello, World!\");",
  "language": "javascript",
  "users": [],
  "createdAt": 1702000000000,
  "status": "active"
}
```

**Error Response** (400):
```json
{
  "error": "INVALID_LANGUAGE",
  "message": "Language must be one of: javascript, typescript, python",
  "statusCode": 400
}
```

---

### GET SESSION
```
GET /api/v1/sessions/{sessionId}
```

**Path Parameters**:
- `sessionId` (string, 10 chars): Session identifier

**Success Response** (200):
```json
{
  "id": "abcdef1234",
  "code": "console.log(\"Hello\");",
  "language": "javascript",
  "users": [
    {
      "id": "user1234",
      "name": "SwiftCoder",
      "color": "#22d3ee",
      "joinedAt": 1702000000000
    }
  ],
  "createdAt": 1702000000000,
  "status": "active"
}
```

**Error Response** (404):
```json
{
  "error": "SESSION_NOT_FOUND",
  "message": "Session with ID 'abcdef1234' not found",
  "statusCode": 404
}
```

---

### UPDATE SESSION
```
PATCH /api/v1/sessions/{sessionId}
```

**Path Parameters**:
- `sessionId` (string, 10 chars): Session identifier

**Request Body** (at least one required):
```json
{
  "code": "console.log(\"Updated\");",
  "language": "typescript",
  "status": "completed"
}
```

**Success Response** (200):
```json
{
  "id": "abcdef1234",
  "code": "console.log(\"Updated\");",
  "language": "typescript",
  "users": [...],
  "createdAt": 1702000000000,
  "status": "completed"
}
```

---

### DELETE SESSION
```
DELETE /api/v1/sessions/{sessionId}
```

**Success Response** (204):
```
No content
```

---

### JOIN SESSION
```
POST /api/v1/sessions/{sessionId}/users
```

**Path Parameters**:
- `sessionId` (string, 10 chars): Session identifier

**Request Body** (optional):
```json
{
  "name": "SwiftCoder"
}
```

**Success Response** (201):
```json
{
  "id": "user1234",
  "name": "SwiftCoder",
  "color": "#22d3ee",
  "joinedAt": 1702000000000
}
```

**Error Response - At Capacity** (409):
```json
{
  "error": "SESSION_AT_CAPACITY",
  "message": "Session has reached maximum of 10 users",
  "statusCode": 409
}
```

---

### GET SESSION USERS
```
GET /api/v1/sessions/{sessionId}/users
```

**Path Parameters**:
- `sessionId` (string, 10 chars): Session identifier

**Success Response** (200):
```json
{
  "users": [
    {
      "id": "user1234",
      "name": "SwiftCoder",
      "color": "#22d3ee",
      "joinedAt": 1702000000000
    },
    {
      "id": "user5678",
      "name": "BoldDev",
      "color": "#a78bfa",
      "joinedAt": 1702000000100
    }
  ]
}
```

---

### LEAVE SESSION
```
DELETE /api/v1/sessions/{sessionId}/users/{userId}
```

**Path Parameters**:
- `sessionId` (string, 10 chars): Session identifier
- `userId` (string, 8 chars): User identifier

**Success Response** (204):
```
No content
```

---

### EXECUTE CODE
```
POST /api/v1/execute
```

**Request Body** (required):
```json
{
  "code": "console.log('Hello, World!');",
  "language": "javascript",
  "timeout": 30000
}
```

**Success Response** (200):
```json
{
  "output": "Hello, World!",
  "error": null,
  "executionTime": 2.5
}
```

**Error Response - Syntax Error** (200 with error):
```json
{
  "output": "",
  "error": "SyntaxError: Unexpected token",
  "executionTime": 1.2
}
```

**Error Response - Timeout** (408):
```json
{
  "error": "EXECUTION_TIMEOUT",
  "message": "Code execution exceeded 30000ms timeout",
  "statusCode": 408
}
```

---

### HEALTH CHECK
```
GET /api/v1/health
```

**Success Response** (200):
```json
{
  "status": "ok",
  "timestamp": "2025-12-08T10:30:00Z"
}
```

---

## Error Codes Reference

| HTTP Code | Error Type | Meaning |
|-----------|-----------|---------|
| 400 | INVALID_REQUEST | Request parameters are invalid |
| 400 | INVALID_LANGUAGE | Language not supported |
| 404 | SESSION_NOT_FOUND | Session doesn't exist |
| 404 | USER_NOT_FOUND | User not in session |
| 409 | SESSION_AT_CAPACITY | Maximum users reached (10) |
| 408 | EXECUTION_TIMEOUT | Code execution timed out |
| 500 | INTERNAL_ERROR | Server error |

---

## Authentication & Security

Currently no authentication is required. Future versions should implement:
- Session token validation
- Rate limiting
- CORS configuration
- Input validation and sanitization

---

## Rate Limiting (Recommended)

- Code execution: 10 requests per minute per IP
- Session operations: 100 requests per minute per IP
- User operations: 50 requests per minute per IP

---

## Example Client Usage (JavaScript/TypeScript)

```typescript
// Create session
const createSession = async () => {
  const response = await fetch('http://localhost:8000/api/v1/sessions', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      language: 'javascript',
      code: 'console.log("Hello");'
    })
  });
  return response.json();
};

// Join session
const joinSession = async (sessionId: string) => {
  const response = await fetch(
    `http://localhost:8000/api/v1/sessions/${sessionId}/users`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    }
  );
  return response.json();
};

// Execute code
const executeCode = async (code: string, language: string) => {
  const response = await fetch('http://localhost:8000/api/v1/execute', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ code, language })
  });
  return response.json();
};
```

---

## Data Validation Rules

### Session ID
- Format: 10 alphanumeric characters (a-z, A-Z, 0-9, underscore, hyphen)
- Example: `abcdef1234`, `Ab_Cd-Ef12`

### User ID
- Format: 8 alphanumeric characters
- Example: `user1234`, `Ab_Cd-Ef`

### Language
- Valid values: `javascript`, `typescript`, `python`
- Case-sensitive, lowercase required

### Color
- Format: Hex color code (#RRGGBB)
- Example: `#22d3ee`, `#a78bfa`

### Code
- Plain text string
- No length limit specified
- Can contain newlines and special characters

---

## Implementation Checklist for Backend

- [ ] Session CRUD endpoints
- [ ] User management endpoints
- [ ] Code execution endpoint with sandbox
- [ ] Health check endpoint
- [ ] Input validation
- [ ] Error handling and responses
- [ ] Session persistence (database)
- [ ] User session cleanup
- [ ] Execution timeout handling
- [ ] CORS configuration
- [ ] Logging and monitoring
- [ ] API documentation/Swagger UI
- [ ] Unit tests
- [ ] Integration tests
- [ ] Load testing

---

Generated: December 8, 2025
