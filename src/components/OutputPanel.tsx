import { Terminal, Clock, AlertCircle, CheckCircle } from 'lucide-react';
import type { ExecutionResult } from '@/types/interview';

interface OutputPanelProps {
  result: ExecutionResult | null;
  isExecuting: boolean;
}

export const OutputPanel = ({ result, isExecuting }: OutputPanelProps) => {
  return (
    <div className="h-full flex flex-col bg-card">
      <div className="h-10 border-b border-border px-4 flex items-center gap-2">
        <Terminal className="h-4 w-4 text-muted-foreground" />
        <span className="text-sm font-medium text-foreground">Output</span>
        {result && (
          <span className="text-xs text-muted-foreground flex items-center gap-1 ml-auto">
            <Clock className="h-3 w-3" />
            {result.executionTime.toFixed(2)}ms
          </span>
        )}
      </div>
      
      <div className="flex-1 overflow-auto p-4 font-mono text-sm">
        {isExecuting ? (
          <div className="flex items-center gap-2 text-muted-foreground">
            <div className="h-4 w-4 border-2 border-primary border-t-transparent rounded-full animate-spin" />
            Executing...
          </div>
        ) : result ? (
          <div className="space-y-2">
            {result.error ? (
              <div className="flex items-start gap-2 text-destructive">
                <AlertCircle className="h-4 w-4 mt-0.5 shrink-0" />
                <pre className="whitespace-pre-wrap">{result.error}</pre>
              </div>
            ) : (
              <div className="flex items-start gap-2 text-foreground">
                <CheckCircle className="h-4 w-4 mt-0.5 shrink-0 text-success" />
                <pre className="whitespace-pre-wrap">{result.output}</pre>
              </div>
            )}
          </div>
        ) : (
          <span className="text-muted-foreground">
            Click "Run" to execute code
          </span>
        )}
      </div>
    </div>
  );
};
