import { Play } from 'lucide-react';
import { useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Header } from './Header';
import { CodeEditor } from './CodeEditor';
import { LanguageSelector } from './LanguageSelector';
import { OutputPanel } from './OutputPanel';
import { useSession } from '@/hooks/useSession';
import { useCodeExecution } from '@/hooks/useCodeExecution';

interface InterviewRoomProps {
  sessionId: string;
  onExit: () => void;
}

export const InterviewRoom = ({ sessionId, onExit }: InterviewRoomProps) => {
  const {
    session,
    currentUser,
    updateCode,
    updateLanguage,
    leaveSession,
    markAsDone,
    loadSession,
    maxUsers,
    isLoading,
    error,
  } = useSession(sessionId);
  const { executeCode, result, isExecuting } = useCodeExecution();

  // Load session on mount
  useEffect(() => {
    if (sessionId) {
      loadSession(sessionId);
    }
  }, [sessionId, loadSession]);

  const handleExit = async () => {
    await leaveSession();
    onExit();
  };

  const handleRun = async () => {
    await executeCode(session!.code, session!.language);
  };

  if (isLoading) {
    return (
      <div className="h-screen flex items-center justify-center bg-background">
        <div className="text-muted-foreground">Loading session...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="h-screen flex items-center justify-center bg-background p-4">
        <Alert variant="destructive" className="max-w-md">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      </div>
    );
  }

  if (!session || !currentUser) {
    return (
      <div className="h-screen flex items-center justify-center bg-background">
        <div className="text-muted-foreground">Initializing session...</div>
      </div>
    );
  }

  return (
    <div className="h-screen flex flex-col bg-background">
      <Header
        sessionId={sessionId}
        users={session.users}
        maxUsers={maxUsers}
        currentUser={currentUser}
        status={session.status || 'active'}
        onExit={handleExit}
        onMarkDone={markAsDone}
      />

      <div className="flex-1 flex flex-col overflow-hidden">
        <div className="h-12 border-b border-border px-4 flex items-center justify-between bg-card">
          <LanguageSelector
            language={session.language}
            onChange={updateLanguage}
          />
          <Button
            size="sm"
            onClick={handleRun}
            disabled={isExecuting}
            className="gap-2"
          >
            <Play className="h-4 w-4" />
            Run
          </Button>
        </div>

        <div className="flex-1 flex flex-col lg:flex-row overflow-hidden">
          <div className="flex-1 min-h-0">
            <CodeEditor
              code={session.code}
              language={session.language}
              onChange={updateCode}
            />
          </div>
          <div className="h-64 lg:h-auto lg:w-96 border-t lg:border-t-0 lg:border-l border-border">
            <OutputPanel result={result} isExecuting={isExecuting} />
          </div>
        </div>
      </div>
    </div>
  );
};
