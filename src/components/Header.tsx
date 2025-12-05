import { Copy, Check, Users, LogOut, CheckCircle } from 'lucide-react';
import { useState } from 'react';
import { Button } from '@/components/ui/button';
import type { User, SessionStatus } from '@/types/interview';

interface HeaderProps {
  sessionId: string;
  users: User[];
  maxUsers: number;
  currentUser: User | null;
  status: SessionStatus;
  onExit: () => void;
  onMarkDone: () => void;
}

export const Header = ({ sessionId, users, maxUsers, currentUser, status, onExit, onMarkDone }: HeaderProps) => {
  const [copied, setCopied] = useState(false);

  const shareUrl = `${window.location.origin}?session=${sessionId}`;

  const handleCopy = async () => {
    await navigator.clipboard.writeText(shareUrl);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <header className="h-14 border-b border-border bg-card px-4 flex items-center justify-between">
      <div className="flex items-center gap-3">
        <h1 className="text-lg font-semibold text-foreground font-mono">
          <span className="text-primary">&lt;</span>
          CodeInterview
          <span className="text-primary">/&gt;</span>
        </h1>
        <span className="text-xs text-muted-foreground font-mono">
          #{sessionId}
        </span>
      </div>

      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2">
          <Users className="h-4 w-4 text-muted-foreground" />
          <span className="text-sm text-muted-foreground">
            {users.length}/{maxUsers}
          </span>
          <div className="flex -space-x-2">
            {users.slice(0, 5).map((user) => (
              <div
                key={user.id}
                className="h-6 w-6 rounded-full border-2 border-card flex items-center justify-center text-xs font-medium"
                style={{ backgroundColor: user.color }}
                title={user.name}
              >
                {user.name[0]}
              </div>
            ))}
            {users.length > 5 && (
              <div className="h-6 w-6 rounded-full border-2 border-card bg-muted flex items-center justify-center text-xs text-muted-foreground">
                +{users.length - 5}
              </div>
            )}
          </div>
        </div>

        <Button
          variant="outline"
          size="sm"
          onClick={handleCopy}
          className="gap-2"
        >
          {copied ? (
            <>
              <Check className="h-4 w-4 text-success" />
              Copied
            </>
          ) : (
            <>
              <Copy className="h-4 w-4" />
              Share Link
            </>
          )}
        </Button>

        {status === 'active' ? (
          <Button
            variant="outline"
            size="sm"
            onClick={onMarkDone}
            className="gap-2 border-primary/50 text-primary hover:bg-primary/10"
          >
            <CheckCircle className="h-4 w-4" />
            Done
          </Button>
        ) : (
          <span className="text-sm text-primary font-medium flex items-center gap-1">
            <CheckCircle className="h-4 w-4" />
            Completed
          </span>
        )}

        <Button
          variant="outline"
          size="sm"
          onClick={onExit}
          className="gap-2 border-destructive/50 text-destructive hover:bg-destructive/10"
        >
          <LogOut className="h-4 w-4" />
          Exit
        </Button>
      </div>
    </header>
  );
};
