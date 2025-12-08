# API Analysis and OpenAPI Specification

## Executive Summary

Based on the analysis of the frontend codebase, I've identified all required backend endpoints and created a comprehensive OpenAPI specification (`openapi.yaml`). The frontend is a **real-time collaborative code interview platform** that requires endpoints for session management, user management, and code execution.

## Frontend Analysis

### Application Architecture

The frontend is a React TypeScript application using:
- **State Management**: React hooks with localStorage for persistence
- **UI Framework**: shadcn/ui with Tailwind CSS
- **Editor**: Monaco Editor with syntax highlighting
- **Routing**: React Router for page navigation
- **Data Fetching**: TanStack React Query (configured but not yet used)

### Core Features

1. **Session Management**
   - Create new interview sessions with unique IDs
   - Join existing sessions (up to 10 users max)
   - Leave sessions
   - Mark sessions as completed
   - Share session links

2. **Code Editor**
   - Monaco Editor with full syntax highlighting
   - Support for JavaScript, TypeScript, and Python
   - Real-time code updates
   - Code execution capabilities

3. **Collaboration**
   - Multiple users in one session (up to 10)
   - User identification with unique colors
   - Display of active participants
   - Real-time presence awareness

4. **Code Execution**
   - Execute JavaScript and TypeScript in-browser
   - Python execution requires backend (currently shows message)
   - Display console output and errors
   - Track execution time

## API Endpoints Required

### 1. Sessions Management (`/api/v1/sessions`)

#### Create Session
- **Method**: POST
- **Path**: `/api/v1/sessions`
- **Purpose**: Create a new interview session
- **Request**: Optional language and initial code
- **Response**: Session object with unique ID

#### Get Session
- **Method**: GET
- **Path**: `/api/v1/sessions/{sessionId}`
- **Purpose**: Fetch current session state
- **Response**: Complete session with all users and code

#### Update Session
- **Method**: PATCH
- **Path**: `/api/v1/sessions/{sessionId}`
- **Purpose**: Update code, language, or status
- **Used By**: Real-time code sync, language switching, session completion

#### Delete Session
- **Method**: DELETE
- **Path**: `/api/v1/sessions/{sessionId}`
- **Purpose**: Remove a completed session

### 2. User Management (`/api/v1/sessions/{sessionId}/users`)

#### Join Session
- **Method**: POST
- **Path**: `/api/v1/sessions/{sessionId}/users`
- **Purpose**: Add user to session
- **Capacity**: Max 10 users per session (409 error when exceeded)
- **Response**: User object with assigned color

#### Get Session Users
- **Method**: GET
- **Path**: `/api/v1/sessions/{sessionId}/users`
- **Purpose**: Get all users in session
- **Response**: Array of user objects

#### Leave Session
- **Method**: DELETE
- **Path**: `/api/v1/sessions/{sessionId}/users/{userId}`
- **Purpose**: Remove user from session

### 3. Code Execution (`/api/v1/execute`)

#### Execute Code
- **Method**: POST
- **Path**: `/api/v1/execute`
- **Purpose**: Execute code and return output
- **Languages**: JavaScript, TypeScript, Python
- **Response**: 
  - `output`: Console output
  - `error`: Error message (if any)
  - `executionTime`: Execution duration in ms
- **Timeout**: 30 seconds (configurable)

### 4. Health Check (`/api/v1/health`)

- **Method**: GET
- **Path**: `/api/v1/health`
- **Purpose**: Check API availability

## Data Models

### Session
```typescript
{
  id: string (10 chars);           // Unique identifier
  code: string;                     // Current code
  language: 'javascript' | 'typescript' | 'python';
  users: User[];                    // Active participants
  createdAt: number;                // Unix timestamp
  status: 'active' | 'completed';   // Session state
}
```

### User
```typescript
{
  id: string (8 chars);             // Unique identifier
  name: string;                     // Display name
  color: string;                    // Hex color (#RRGGBB)
  joinedAt: number;                 // Unix timestamp
}
```

### ExecutionResult
```typescript
{
  output: string;                   // Console output
  error: string | null;             // Error message
  executionTime: number;            // Milliseconds
}
```

## Key Frontend Interactions

### Session Flow
1. User lands on landing page
2. Clicks "Create Interview Session" → POST `/api/v1/sessions`
3. Gets unique session ID (e.g., `abcdef1234`)
4. Joins session → POST `/api/v1/sessions/{id}/users`
5. Gets assigned user ID and color
6. Others can join via shared URL

### Code Execution Flow
1. User edits code in Monaco Editor
2. Code automatically updates in local state (future: sync to backend)
3. Clicks "Run" → POST `/api/v1/execute`
4. Backend executes code
5. Returns output/error with execution time
6. Displayed in output panel

### Real-time Collaboration (Future Enhancement)
- Currently uses localStorage for state persistence
- Plan: WebSocket connection for real-time updates
- Users see code changes as they happen
- Cursor/selection tracking (not yet implemented)

## Implementation Notes

### Current Limitations
- Frontend currently uses **localStorage** for persistence
- JavaScript/TypeScript execution runs **in-browser** (Function API)
- Python execution would require backend sandbox
- No real-time synchronization yet (uses storage events for multi-tab)

### Backend Requirements
1. **Session Storage**: Database to persist sessions
2. **User Management**: Track connected users per session
3. **Code Execution**: Secure sandbox for JavaScript, TypeScript, Python
4. **Timeout Handling**: 30-second execution limit with cleanup
5. **Error Handling**: Comprehensive error responses (400, 404, 409, 500)
6. **Scalability**: Support multiple concurrent sessions

## Future Enhancements (Not in Current Scope)

- WebSocket support for real-time updates
- Cursor position tracking
- Syntax error highlighting before execution
- Code persistence and history
- User authentication
- Session recordings/replays
- Collaborative debugging features

## OpenAPI Specification Details

The complete OpenAPI 3.0.0 specification includes:
- All 8 endpoints with detailed descriptions
- Request/response schemas with examples
- HTTP status codes and error handling
- Parameter validation patterns
- Required fields and data types
- Nullable fields for optional values

File: `openapi.yaml`

## Next Steps for Backend Implementation

1. **Choose Technology Stack**
   - Python (FastAPI, Flask) or Node.js (Express, Fastify)
   - Database for session persistence
   - Code execution sandbox (Docker, VM, or language-specific runners)

2. **Implement Endpoints** (in order of priority)
   - Sessions CRUD operations
   - User join/leave
   - Code execution with timeout
   - Health check

3. **Add Non-Functional Requirements**
   - Input validation
   - Error handling
   - Logging
   - Testing

4. **Consider**
   - Rate limiting
   - CORS configuration
   - Security headers
   - Code sandbox security

---

**Analysis Date**: December 8, 2025
**OpenAPI Version**: 3.0.0
**API Version**: 1.0.0
