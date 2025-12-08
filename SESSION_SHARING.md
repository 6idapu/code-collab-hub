# Real-Time Session Sharing & Collaboration

## How It Works

The application now supports real-time collaborative coding sessions:

### ✅ What's Working

1. **Session URL Persistence**
   - Sessions are identified by URL parameter: `?session=SESSION_ID`
   - Refreshing the page maintains your connection to the same session
   - No new session is created on page reload

2. **Session Sharing**
   - Copy and paste the URL to share with others
   - Others joining via the link connect to the **same session**
   - All participants see the same code and output

3. **Real-Time Updates**
   - Frontend polls the backend every 1 second for updates
   - When one user types code, others see it within 1 second
   - All users see live language changes and execution results

4. **Multi-User Support**
   - Up to 10 users can connect to the same session
   - Each user is tracked with a unique ID and color
   - Session capacity prevents overcrowding

## Technical Implementation

### Frontend Changes

**`frontend/src/hooks/useSession.ts`**
- Added polling effect that runs every 1 second when a user is connected
- Polls: `GET /api/v1/sessions/{sessionId}`
- Fetches and updates session state, including code changes from other users
- Stops polling when user leaves or session ends

**`frontend/src/pages/Index.tsx`**
- Fixed URL parameter handling
- Session ID now persists when page refreshes
- Properly joins the same session instead of creating a new one

### Backend Requirements

The backend API must support:
- `GET /api/v1/sessions/{sessionId}` - Fetch current session state
- `PATCH /api/v1/sessions/{sessionId}` - Update code/language/status
- `POST /api/v1/sessions/{sessionId}/users` - Join session
- `DELETE /api/v1/sessions/{sessionId}/users/{userId}` - Leave session

## Testing

### Manual Testing Steps

1. **Start services:**
   ```bash
   npm run dev
   ```

2. **Open in first browser/window:**
   - Go to `http://localhost:8080`
   - Click "Create Interview Session"
   - Copy the generated URL

3. **Open in second browser/window:**
   - Paste the URL from step 2
   - You should join the **same session**
   - Initial code should match

4. **Test real-time sync:**
   - In first window: type some code
   - In second window: within 1 second you should see the changes
   - Verify output syncs when running code

### Test with curl

```bash
# Create session
curl -X POST http://localhost:8000/api/v1/sessions \
  -H "Content-Type: application/json" \
  -d '{"language":"javascript","code":"const x = 1;"}'

# Get session
curl http://localhost:8000/api/v1/sessions/{SESSION_ID}

# Update code (simulating user 1 typing)
curl -X PATCH http://localhost:8000/api/v1/sessions/{SESSION_ID} \
  -H "Content-Type: application/json" \
  -d '{"code":"const y = 2;"}'

# Poll for updates (simulating user 2)
curl http://localhost:8000/api/v1/sessions/{SESSION_ID}
```

## Performance Notes

- **Polling Interval**: 1 second
  - Balances real-time updates with server load
  - Could be reduced to 500ms for faster sync (higher load)
  - Could be increased to 2-3s for slower networks

- **Next Step**: Replace polling with WebSocket for true real-time sync without network overhead

## Limitations (Current)

1. **Polling-based** (not WebSocket)
   - Up to 1 second delay between updates
   - More network requests than ideal
   - But works across all browsers and proxies

2. **No Conflict Resolution**
   - If two users edit simultaneously, last write wins
   - No operational transformation (OT) or conflict-free replicated data type (CRDT)

3. **Memory-only Storage**
   - Sessions lost when backend restarts
   - No persistence to database

## Future Improvements

- [ ] WebSocket for true real-time sync
- [ ] Operational Transformation (OT) for collaborative editing
- [ ] Database persistence for session recovery
- [ ] User presence indicators (who's typing)
- [ ] Cursor position sharing
- [ ] Chat/comments in session
- [ ] Session history/replay
