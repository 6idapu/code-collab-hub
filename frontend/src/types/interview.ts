export type Language = 'javascript' | 'typescript' | 'python';

export interface User {
  id: string;
  name: string;
  color: string;
  joinedAt: number;
}

export type SessionStatus = 'active' | 'completed';

export interface Session {
  id: string;
  code: string;
  language: Language;
  users: User[];
  createdAt: number;
  status: SessionStatus;
}

export interface ExecutionResult {
  output: string;
  error: string | null;
  executionTime: number;
}
