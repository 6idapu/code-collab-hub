import { useState, useCallback } from 'react';
import type { ExecutionResult, Language } from '@/types/interview';

export const useCodeExecution = () => {
  const [isExecuting, setIsExecuting] = useState(false);
  const [result, setResult] = useState<ExecutionResult | null>(null);

  const executeCode = useCallback(async (code: string, language: Language): Promise<ExecutionResult> => {
    setIsExecuting(true);
    const startTime = performance.now();
    
    let output = '';
    let error: string | null = null;

    try {
      if (language === 'python') {
        output = 'Python execution requires a backend. Please use JavaScript or TypeScript.';
      } else {
        // Capture console output
        const logs: string[] = [];
        const originalLog = console.log;
        const originalError = console.error;
        const originalWarn = console.warn;

        console.log = (...args) => logs.push(args.map(String).join(' '));
        console.error = (...args) => logs.push(`Error: ${args.map(String).join(' ')}`);
        console.warn = (...args) => logs.push(`Warning: ${args.map(String).join(' ')}`);

        try {
          // Create sandboxed execution
          const sandboxedCode = `
            "use strict";
            ${code}
          `;
          
          // Execute in a try-catch
          const fn = new Function(sandboxedCode);
          const returnValue = fn();
          
          if (returnValue !== undefined) {
            logs.push(`Return: ${JSON.stringify(returnValue, null, 2)}`);
          }
        } finally {
          console.log = originalLog;
          console.error = originalError;
          console.warn = originalWarn;
        }

        output = logs.join('\n') || 'Code executed successfully (no output)';
      }
    } catch (e) {
      error = e instanceof Error ? e.message : String(e);
    }

    const executionTime = performance.now() - startTime;
    const executionResult = { output, error, executionTime };
    
    setResult(executionResult);
    setIsExecuting(false);
    
    return executionResult;
  }, []);

  const clearResult = useCallback(() => {
    setResult(null);
  }, []);

  return {
    executeCode,
    clearResult,
    isExecuting,
    result,
  };
};
