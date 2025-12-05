import { AlertTriangle } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface CapacityErrorProps {
  onGoHome: () => void;
}

export const CapacityError = ({ onGoHome }: CapacityErrorProps) => {
  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-6">
      <div className="max-w-md w-full text-center space-y-6">
        <div className="h-16 w-16 rounded-full bg-destructive/10 flex items-center justify-center mx-auto">
          <AlertTriangle className="h-8 w-8 text-destructive" />
        </div>
        <div className="space-y-2">
          <h2 className="text-xl font-semibold text-foreground">
            Session at Capacity
          </h2>
          <p className="text-muted-foreground">
            This interview session has reached the maximum of 10 participants.
            Please try again later or create a new session.
          </p>
        </div>
        <Button onClick={onGoHome}>
          Create New Session
        </Button>
      </div>
    </div>
  );
};
