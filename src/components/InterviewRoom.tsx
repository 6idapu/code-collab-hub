import { Play } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Header } from './Header';
import { CodeEditor } from './CodeEditor';
import { LanguageSelector } from './LanguageSelector';
import { OutputPanel } from './OutputPanel';
import { useSession } from '@/hooks/useSession';
import { useCodeExecution } from '@/hooks/useCodeExecution';

interface InterviewRoomProps {
  sessionId: string;
}

export const InterviewRoom = ({ sessionId }: InterviewRoomProps) => {
  const { session, currentUser, updateCode, updateLanguage, maxUsers } = useSession(sessionId);
  const { executeCode, result, isExecuting } = useCodeExecution();

  if (!session) {
    return (
      <div className="h-screen flex items-center justify-center bg-background">
        <div className="text-muted-foreground">Loading session...</div>
      </div>
    );
  }

  const handleRun = () => {
    executeCode(session.code, session.language);
  };

  return (
    <div className="h-screen flex flex-col bg-background">
      <Header
        sessionId={sessionId}
        users={session.users}
        maxUsers={maxUsers}
        currentUser={currentUser}
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
