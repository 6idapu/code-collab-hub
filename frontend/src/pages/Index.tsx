import { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { LandingPage } from '@/components/LandingPage';
import { InterviewRoom } from '@/components/InterviewRoom';
import { CapacityError } from '@/components/CapacityError';
import { useSession } from '@/hooks/useSession';

const Index = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const sessionIdFromUrl = searchParams.get('session');
  const [activeSessionId, setActiveSessionId] = useState<string | null>(sessionIdFromUrl);
  
  const { createSession, isAtCapacity } = useSession(activeSessionId);

  useEffect(() => {
    if (sessionIdFromUrl) {
      setActiveSessionId(sessionIdFromUrl);
    }
  }, [sessionIdFromUrl]);

  const handleCreateSession = () => {
    const newSessionId = createSession();
    setSearchParams({ session: newSessionId });
    setActiveSessionId(newSessionId);
  };

  const handleGoHome = () => {
    setSearchParams({});
    setActiveSessionId(null);
  };

  if (isAtCapacity) {
    return <CapacityError onGoHome={handleGoHome} />;
  }

  if (activeSessionId) {
    return <InterviewRoom sessionId={activeSessionId} onExit={handleGoHome} />;
  }

  return <LandingPage onCreateSession={handleCreateSession} />;
};

export default Index;
