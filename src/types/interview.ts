export type Language = 'javascript' | 'typescript' | 'python';

export interface User {
  id: string;
  name: string;
  color: string;
  joinedAt: number;
}

export interface Session {
  id: string;
  code: string;
  language: Language;
  users: User[];
  createdAt: number;
}

export interface ExecutionResult {
  output: string;
  error: string | null;
  executionTime: number;
}
