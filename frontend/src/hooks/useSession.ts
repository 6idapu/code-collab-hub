import { useState, useEffect, useCallback } from 'react';
import { nanoid } from 'nanoid';
import type { Session, User, Language, SessionStatus } from '@/types/interview';

const MAX_USERS = 10;
const STORAGE_PREFIX = 'interview_session_';
const USER_COLORS = [
  '#22d3ee', '#a78bfa', '#f472b6', '#fbbf24', 
  '#34d399', '#fb7185', '#60a5fa', '#c084fc',
  '#4ade80', '#f97316'
];

const getRandomColor = (existingColors: string[]): string => {
  const available = USER_COLORS.filter(c => !existingColors.includes(c));
  return available[Math.floor(Math.random() * available.length)] || USER_COLORS[0];
};

const generateUserName = (): string => {
  const adjectives = ['Swift', 'Clever', 'Bold', 'Calm', 'Eager'];
  const nouns = ['Coder', 'Dev', 'Hacker', 'Builder', 'Creator'];
  return `${adjectives[Math.floor(Math.random() * adjectives.length)]}${nouns[Math.floor(Math.random() * nouns.length)]}`;
};

export const useSession = (sessionId: string | null) => {
  const [session, setSession] = useState<Session | null>(null);
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [isAtCapacity, setIsAtCapacity] = useState(false);

  const createSession = useCallback((): string => {
    const id = nanoid(10);
    const newSession: Session = {
      id,
      code: '// Start coding here\nconsole.log("Hello, World!");',
      language: 'javascript',
      users: [],
      createdAt: Date.now(),
      status: 'active',
    };
    localStorage.setItem(`${STORAGE_PREFIX}${id}`, JSON.stringify(newSession));
    return id;
  }, []);

  const joinSession = useCallback((session: Session): User | null => {
    if (session.users.length >= MAX_USERS) {
      setIsAtCapacity(true);
      return null;
    }

    const existingColors = session.users.map(u => u.color);
    const user: User = {
      id: nanoid(8),
      name: generateUserName(),
      color: getRandomColor(existingColors),
      joinedAt: Date.now(),
    };

    const updatedSession = {
      ...session,
      users: [...session.users, user],
    };
    
    localStorage.setItem(`${STORAGE_PREFIX}${session.id}`, JSON.stringify(updatedSession));
    setSession(updatedSession);
    setCurrentUser(user);
    
    return user;
  }, []);

  const updateCode = useCallback((code: string) => {
    if (!session) return;
    
    const updatedSession = { ...session, code };
    localStorage.setItem(`${STORAGE_PREFIX}${session.id}`, JSON.stringify(updatedSession));
    setSession(updatedSession);
  }, [session]);

  const updateLanguage = useCallback((language: Language) => {
    if (!session) return;
    
    const updatedSession = { ...session, language };
    localStorage.setItem(`${STORAGE_PREFIX}${session.id}`, JSON.stringify(updatedSession));
    setSession(updatedSession);
  }, [session]);

  const leaveSession = useCallback(() => {
    if (!session || !currentUser) return;
    
    const updatedSession = {
      ...session,
      users: session.users.filter(u => u.id !== currentUser.id),
    };
    
    localStorage.setItem(`${STORAGE_PREFIX}${session.id}`, JSON.stringify(updatedSession));
    setSession(null);
    setCurrentUser(null);
  }, [session, currentUser]);

  const markAsDone = useCallback(() => {
    if (!session) return;
    
    const updatedSession = {
      ...session,
      status: 'completed' as SessionStatus,
    };
    
    localStorage.setItem(`${STORAGE_PREFIX}${session.id}`, JSON.stringify(updatedSession));
    setSession(updatedSession);
  }, [session]);

  useEffect(() => {
    if (!sessionId) return;

    const stored = localStorage.getItem(`${STORAGE_PREFIX}${sessionId}`);
    if (stored) {
      const parsed = JSON.parse(stored) as Session;
      setSession(parsed);
      
      if (!currentUser) {
        joinSession(parsed);
      }
    }
  }, [sessionId, currentUser, joinSession]);

  // Sync with localStorage changes (for multi-tab support)
  useEffect(() => {
    if (!sessionId) return;

    const handleStorage = (e: StorageEvent) => {
      if (e.key === `${STORAGE_PREFIX}${sessionId}` && e.newValue) {
        const updated = JSON.parse(e.newValue) as Session;
        setSession(updated);
      }
    };

    window.addEventListener('storage', handleStorage);
    return () => window.removeEventListener('storage', handleStorage);
  }, [sessionId]);

  return {
    session,
    currentUser,
    isAtCapacity,
    createSession,
    updateCode,
    updateLanguage,
    leaveSession,
    markAsDone,
    maxUsers: MAX_USERS,
  };
};
