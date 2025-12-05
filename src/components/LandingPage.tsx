import { Plus, Code2, Users, Zap } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface LandingPageProps {
  onCreateSession: () => void;
}

export const LandingPage = ({ onCreateSession }: LandingPageProps) => {
  return (
    <div className="min-h-screen bg-background flex flex-col">
      <header className="h-14 border-b border-border px-6 flex items-center">
        <h1 className="text-lg font-semibold text-foreground font-mono">
          <span className="text-primary">&lt;</span>
          CodeInterview
          <span className="text-primary">/&gt;</span>
        </h1>
      </header>

      <main className="flex-1 flex items-center justify-center p-6">
        <div className="max-w-md w-full space-y-8 text-center">
          <div className="space-y-4">
            <h2 className="text-3xl font-bold text-foreground">
              Real-time Collaborative
              <br />
              <span className="text-primary">Code Interviews</span>
            </h2>
            <p className="text-muted-foreground">
              Create a session, share the link, and code together in real-time with syntax highlighting and instant execution.
            </p>
          </div>

          <Button
            size="lg"
            onClick={onCreateSession}
            className="gap-2 w-full max-w-xs"
          >
            <Plus className="h-5 w-5" />
            Create Interview Session
          </Button>

          <div className="grid grid-cols-3 gap-4 pt-8">
            <div className="space-y-2">
              <div className="h-10 w-10 rounded-lg bg-secondary flex items-center justify-center mx-auto">
                <Code2 className="h-5 w-5 text-primary" />
              </div>
              <p className="text-xs text-muted-foreground">
                Syntax Highlighting
              </p>
            </div>
            <div className="space-y-2">
              <div className="h-10 w-10 rounded-lg bg-secondary flex items-center justify-center mx-auto">
                <Users className="h-5 w-5 text-primary" />
              </div>
              <p className="text-xs text-muted-foreground">
                Up to 10 Users
              </p>
            </div>
            <div className="space-y-2">
              <div className="h-10 w-10 rounded-lg bg-secondary flex items-center justify-center mx-auto">
                <Zap className="h-5 w-5 text-primary" />
              </div>
              <p className="text-xs text-muted-foreground">
                Instant Execution
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};
