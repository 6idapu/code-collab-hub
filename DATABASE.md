# SQLAlchemy SQLite Database Implementation

## Overview

The backend has been migrated from an in-memory mock database to a real **SQLite database** powered by **SQLAlchemy ORM**. This provides persistent storage of all sessions and user data.

## Database Setup

### File Location
- **Database File**: `backend/code_interview.db`
- **Auto-created** on first run - no manual setup needed

### Database URL Configuration

By default, the app uses SQLite. To use a custom database:

```bash
# Use PostgreSQL
export DATABASE_URL="postgresql://user:password@localhost/code_interview"
npm run dev

# Use MySQL
export DATABASE_URL="mysql+pymysql://user:password@localhost/code_interview"
npm run dev

# Use SQLite with different location
export DATABASE_URL="sqlite:////tmp/code_interview.db"
npm run dev
```

## Database Schema

### Tables

#### `sessions`
```
id (String, Primary Key)          - Session ID (10 chars)
code (Text)                       - Current code in session
language (String)                 - Programming language
status (String)                   - "active" or "completed"
created_at (Integer)              - Unix timestamp (milliseconds)
updated_at (Integer)              - Last update timestamp (milliseconds)
```

#### `users`
```
id (String, Primary Key)          - User ID (8 chars)
name (String)                     - User display name
color (String)                    - Hex color code
joined_at (Integer)               - Unix timestamp (milliseconds)
```

#### `session_users` (Junction Table)
```
session_id (String, FK)           - Foreign key to sessions
user_id (String, FK)              - Foreign key to users
```

### Relationships
- **Sessions → Users**: Many-to-Many (through `session_users`)
- Each session can have multiple users (max 10)
- Each user can be in one session at a time (in practice)

## Data Persistence

### Before (Mock Database)
- ❌ All data lost when server restarts
- ❌ No persistence between deployments
- ✅ Fast for testing and development

### After (SQLite)
- ✅ All sessions persist to disk
- ✅ Survives server restarts
- ✅ Data available after redeployment
- ✅ Can be backed up like any database file

## File Structure

```
backend/
├── app/
│   ├── models/
│   │   ├── orm.py          # NEW: SQLAlchemy ORM models
│   │   └── schema.py       # Pydantic schemas (unchanged)
│   ├── services/
│   │   └── database.py     # Database service (refactored)
│   └── routes/             # Routes (minimal changes)
├── code_interview.db       # NEW: SQLite database file
├── pyproject.toml          # Updated: sqlalchemy dependency
└── ...
```

## Implementation Details

### ORM Models (`app/models/orm.py`)

```python
# SessionModel represents a session row
class SessionModel:
    id: str
    code: str
    language: str
    status: str
    created_at: int
    updated_at: int
    users: List[UserModel]  # Relationship

# UserModel represents a user row
class UserModel:
    id: str
    name: str
    color: str
    joined_at: int
    sessions: List[SessionModel]  # Relationship
```

### Database Service (`app/services/database.py`)

The `Database` class manages all database operations:

```python
db = Database()  # SQLite by default

# Session operations
db.create_session(session_id, language, code, created_at)
db.get_session_by_id(session_id)
db.update_session(session_id, code=None, language=None, status=None)
db.delete_session(session_id)

# User operations
db.add_user(session_id, user)
db.get_session_users(session_id)
db.remove_user(session_id, user_id)
db.get_user_in_session(session_id, user_id)
```

### Connection Pooling

SQLAlchemy handles:
- Connection reuse
- Thread safety
- Automatic connection cleanup
- Connection timeouts

## Testing

All 43 tests pass with the new SQLite backend:

```bash
npm run test:backend
# Output: 43 passed in 2.81s
```

Tests use temporary SQLite databases (in-memory or temp files) and are properly isolated.

## Migration Path

If you want to migrate from SQLite to PostgreSQL in production:

1. Install PostgreSQL driver:
   ```bash
   cd backend
   uv add psycopg2-binary
   ```

2. Create PostgreSQL database:
   ```bash
   createdb code_interview
   ```

3. Export data from SQLite (optional):
   ```sql
   -- SQLite dump and restore to PostgreSQL
   ```

4. Set environment variable:
   ```bash
   export DATABASE_URL="postgresql://user:password@localhost/code_interview"
   npm run dev
   ```

## Performance Considerations

### SQLite (Current)
- ✅ Zero setup needed
- ✅ Perfect for development
- ✅ Single-file database
- ⚠️ Limited concurrent writes (WAL mode helps)
- ⚠️ Not ideal for high-traffic production

### PostgreSQL (Recommended for Production)
- ✅ High concurrency
- ✅ Advanced features (full-text search, JSON, etc.)
- ✅ Better for distributed deployments
- ⚠️ Requires server setup

### MySQL
- ✅ Wide hosting support
- ✅ Good performance
- ⚠️ Some features limited

## Backup & Recovery

### SQLite
```bash
# Backup
cp backend/code_interview.db backend/code_interview.db.backup

# Restore
cp backend/code_interview.db.backup backend/code_interview.db
```

### With PostgreSQL
```bash
# Backup
pg_dump code_interview > backup.sql

# Restore
psql code_interview < backup.sql
```

## Troubleshooting

### Database File Locked
SQLite can lock if multiple processes access it. Solutions:
1. Ensure only one server instance
2. Use WAL mode (already enabled)
3. Migrate to PostgreSQL for high concurrency

### Database Corruption
SQLite can corrupt if:
- Process crashes during write
- File system issues
- Multiple writers simultaneously

Recovery:
```bash
# Check integrity
sqlite3 code_interview.db "PRAGMA integrity_check;"

# Restore from backup
cp code_interview.db.backup code_interview.db
```

## API Changes

The API responses are **completely unchanged** - no frontend modifications needed. The database migration is transparent to API consumers.

Example session response (identical before and after):
```json
{
  "id": "abc123def456",
  "code": "console.log('Hello');",
  "language": "javascript",
  "users": [...],
  "createdAt": 1702000000000,
  "status": "active"
}
```
