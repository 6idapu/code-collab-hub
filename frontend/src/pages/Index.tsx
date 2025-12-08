import { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { LandingPage } from '@/components/LandingPage';
import { InterviewRoom } from '@/components/InterviewRoom';
import { CapacityError } from '@/components/CapacityError';
import { useSession } from '@/hooks/useSession';
import { Alert, AlertDescription } from '@/components/ui/alert';

const Index = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const sessionIdFromUrl = searchParams.get('session');
  const [activeSessionId, setActiveSessionId] = useState<string | null>(
    sessionIdFromUrl
  );
  const [isCreating, setIsCreating] = useState(false);
  const [creationError, setCreationError] = useState<string | null>(null);

  const { createSession, isAtCapacity } = useSession(activeSessionId);

  // When URL changes (including on refresh or when link is shared), update active session
  useEffect(() => {
    if (sessionIdFromUrl && sessionIdFromUrl !== activeSessionId) {
      setActiveSessionId(sessionIdFromUrl);
      setCreationError(null);
    } else if (!sessionIdFromUrl && activeSessionId) {
      // User navigated back home
      setActiveSessionId(null);
    }
  }, [sessionIdFromUrl]);

  const handleCreateSession = async () => {
    try {
      setIsCreating(true);
      setCreationError(null);
      const newSessionId = await createSession();
      setSearchParams({ session: newSessionId });
      setActiveSessionId(newSessionId);
    } catch (err) {
      setCreationError(
        err instanceof Error ? err.message : 'Failed to create session'
      );
    } finally {
      setIsCreating(false);
    }
  };

  const handleGoHome = () => {
    setSearchParams({});
    setActiveSessionId(null);
    setCreationError(null);
  };

  if (isAtCapacity) {
    return <CapacityError onGoHome={handleGoHome} />;
  }

  if (creationError) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background p-4">
        <Alert variant="destructive" className="max-w-md">
          <AlertDescription>{creationError}</AlertDescription>
          <button
            onClick={handleGoHome}
            className="mt-4 text-sm underline hover:no-underline"
          >
            Go Back Home
          </button>
        </Alert>
      </div>
    );
  }

  if (activeSessionId) {
    return <InterviewRoom sessionId={activeSessionId} onExit={handleGoHome} />;
  }

  return (
    <LandingPage
      onCreateSession={handleCreateSession}
      isCreating={isCreating}
    />
  );
};

export default Index;
