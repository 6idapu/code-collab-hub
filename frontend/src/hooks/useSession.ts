import { useState, useCallback, useEffect, useRef } from 'react';
import type { Session, User, Language, SessionStatus } from '@/types/interview';
import { sessionsApi, usersApi, ApiError } from '@/services/api';

const MAX_USERS = 10;
const POLL_INTERVAL = 1000; // Poll every 1 second for real-time updates

export const useSession = (sessionId: string | null) => {
  const [session, setSession] = useState<Session | null>(null);
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [isAtCapacity, setIsAtCapacity] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const pollIntervalRef = useRef<NodeJS.Timeout | null>(null);

  const createSession = useCallback(async (): Promise<string> => {
    try {
      setIsLoading(true);
      setError(null);
      const newSession = await sessionsApi.create(
        'javascript',
        '// Start coding here\nconsole.log("Hello, World!");'
      );
      setSession(newSession);
      return newSession.id;
    } catch (err) {
      const message = err instanceof ApiError ? err.message : 'Failed to create session';
      setError(message);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const joinSession = useCallback(async (sessionId: string): Promise<User | null> => {
    try {
      setIsLoading(true);
      setError(null);
      
      // Fetch the session first
      const sessionData = await sessionsApi.get(sessionId);
      setSession(sessionData);

      // Then join the session
      const user = await usersApi.join(sessionId);
      setCurrentUser(user);
      setIsAtCapacity(false);
      
      return user;
    } catch (err) {
      if (err instanceof ApiError) {
        if (err.statusCode === 409) {
          setIsAtCapacity(true);
          setError('Session is at capacity');
          return null;
        }
        setError(err.message);
      } else {
        setError('Failed to join session');
      }
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const updateCode = useCallback(async (code: string) => {
    if (!session) return;
    
    try {
      setError(null);
      const updated = await sessionsApi.update(session.id, { code });
      setSession(updated);
    } catch (err) {
      const message = err instanceof ApiError ? err.message : 'Failed to update code';
      setError(message);
    }
  }, [session]);

  const updateLanguage = useCallback(async (language: Language) => {
    if (!session) return;
    
    try {
      setError(null);
      const updated = await sessionsApi.update(session.id, { language });
      setSession(updated);
    } catch (err) {
      const message = err instanceof ApiError ? err.message : 'Failed to update language';
      setError(message);
    }
  }, [session]);

  const leaveSession = useCallback(async () => {
    if (!session || !currentUser) return;
    
    try {
      setError(null);
      await usersApi.leave(session.id, currentUser.id);
      setSession(null);
      setCurrentUser(null);
    } catch (err) {
      const message = err instanceof ApiError ? err.message : 'Failed to leave session';
      setError(message);
    }
  }, [session, currentUser]);

  const markAsDone = useCallback(async () => {
    if (!session) return;
    
    try {
      setError(null);
      const updated = await sessionsApi.update(session.id, { status: 'completed' });
      setSession(updated);
    } catch (err) {
      const message = err instanceof ApiError ? err.message : 'Failed to mark session as done';
      setError(message);
    }
  }, [session]);

  const loadSession = useCallback(async (id: string) => {
    try {
      setIsLoading(true);
      setError(null);
      const sessionData = await sessionsApi.get(id);
      setSession(sessionData);
    } catch (err) {
      const message = err instanceof ApiError ? err.message : 'Failed to load session';
      setError(message);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const loadAndJoinSession = useCallback(async (id: string) => {
    try {
      setIsLoading(true);
      setError(null);
      
      // Load session
      const sessionData = await sessionsApi.get(id);
      setSession(sessionData);
      
      // Join session
      const user = await usersApi.join(id);
      setCurrentUser(user);
      setIsAtCapacity(false);
      
      return user;
    } catch (err) {
      if (err instanceof ApiError) {
        if (err.statusCode === 409) {
          setIsAtCapacity(true);
          setError('Session is at capacity');
          return null;
        }
        setError(err.message);
      } else {
        setError('Failed to join session');
      }
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Start polling for session updates when sessionId is active and user has joined
  useEffect(() => {
    if (!sessionId || !currentUser) {
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current);
        pollIntervalRef.current = null;
      }
      return;
    }

    // Poll immediately and then at interval
    const pollSession = async () => {
      try {
        const updatedSession = await sessionsApi.get(sessionId);
        setSession(updatedSession);
      } catch (err) {
        // Silent fail on poll errors to avoid disrupting user experience
        console.debug('Failed to poll session:', err);
      }
    };

    // Initial poll
    pollSession();

    // Set up interval
    pollIntervalRef.current = setInterval(pollSession, POLL_INTERVAL);

    return () => {
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current);
        pollIntervalRef.current = null;
      }
    };
  }, [sessionId, currentUser]);

  return {
    session,
    currentUser,
    isAtCapacity,
    isLoading,
    error,
    createSession,
    joinSession,
    updateCode,
    updateLanguage,
    leaveSession,
    markAsDone,
    loadSession,
    loadAndJoinSession,
    maxUsers: MAX_USERS,
  };
};
