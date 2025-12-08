import { useState, useCallback } from 'react';
import type { ExecutionResult, Language } from '@/types/interview';
import { executionApi, ApiError } from '@/services/api';

export const useCodeExecution = () => {
  const [isExecuting, setIsExecuting] = useState(false);
  const [result, setResult] = useState<ExecutionResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const executeCode = useCallback(
    async (code: string, language: Language): Promise<ExecutionResult> => {
      setIsExecuting(true);
      setError(null);

      try {
        const executionResult = await executionApi.execute(code, language, 30000);
        setResult(executionResult);
        return executionResult;
      } catch (err) {
        const errorMessage =
          err instanceof ApiError ? err.message : 'Code execution failed';
        setError(errorMessage);
        
        const executionResult: ExecutionResult = {
          output: '',
          error: errorMessage,
          executionTime: 0,
        };
        setResult(executionResult);
        return executionResult;
      } finally {
        setIsExecuting(false);
      }
    },
    []
  );

  const clearResult = useCallback(() => {
    setResult(null);
    setError(null);
  }, []);

  return {
    executeCode,
    clearResult,
    isExecuting,
    result,
    error,
  };
};
