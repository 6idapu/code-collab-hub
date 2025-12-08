"""Code execution service."""

import asyncio
import subprocess
import tempfile
import time
import traceback
from typing import Optional
from app.models import Language, ExecutionResult


class CodeExecutionService:
    """Service for executing code safely."""

    @staticmethod
    async def execute(
        code: str, language: Language, timeout: int = 30000
    ) -> ExecutionResult:
        """Execute code and return the result.

        Args:
            code: The code to execute
            language: Programming language
            timeout: Timeout in milliseconds

        Returns:
            ExecutionResult with output, error, and execution time
        """
        start_time = time.time()

        try:
            if language == "python":
                return CodeExecutionService._execute_python(code)
            elif language in ["javascript", "typescript"]:
                return CodeExecutionService._execute_javascript(code)
            else:
                return ExecutionResult(
                    output="",
                    error=f"Unsupported language: {language}",
                    executionTime=0,
                )
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            return ExecutionResult(
                output="",
                error=f"{type(e).__name__}: {str(e)}",
                executionTime=execution_time,
            )

    @staticmethod
    def _execute_python(code: str) -> ExecutionResult:
        """Execute Python code in a sandboxed environment.

        Note: This is a simplified implementation. In production,
        use a proper sandbox like RestrictedPython or Docker.
        """
        start_time = time.time()
        output_buffer = []
        error_output: Optional[str] = None

        try:
            # Create a safe execution environment
            safe_globals = {
                "__builtins__": {
                    "print": lambda *args, **kwargs: output_buffer.append(
                        " ".join(str(arg) for arg in args)
                    ),
                    "len": len,
                    "range": range,
                    "str": str,
                    "int": int,
                    "float": float,
                    "list": list,
                    "dict": dict,
                    "tuple": tuple,
                    "set": set,
                    "sum": sum,
                    "max": max,
                    "min": min,
                },
                "__name__": "__main__",
            }
            safe_locals = {}

            # Execute the code
            exec(code, safe_globals, safe_locals)

            # Capture any returned values
            if "result" in safe_locals:
                output_buffer.append(f"Result: {safe_locals['result']}")

        except SyntaxError as e:
            error_output = f"SyntaxError: {e.msg} (line {e.lineno})"
        except Exception as e:
            error_output = f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"

        execution_time = (time.time() - start_time) * 1000
        output = "\n".join(output_buffer) if output_buffer else ""

        return ExecutionResult(
            output=output or (output or "Code executed successfully (no output)"),
            error=error_output,
            executionTime=execution_time,
        )

    @staticmethod
    def _execute_javascript(code: str) -> ExecutionResult:
        """Execute JavaScript code using Node.js.

        Args:
            code: JavaScript code to execute

        Returns:
            ExecutionResult with output, error, and execution time
        """
        start_time = time.time()

        try:
            # Create a temporary file for the code
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".js", delete=False
            ) as f:
                # Wrap code with console output capture
                wrapped_code = f"""
const originalLog = console.log;
const originalError = console.error;
const originalWarn = console.warn;
const outputs = [];

console.log = function(...args) {{
    outputs.push(args.map(arg => 
        typeof arg === 'object' ? JSON.stringify(arg, null, 2) : String(arg)
    ).join(' '));
}};

console.error = function(...args) {{
    outputs.push('Error: ' + args.map(arg => 
        typeof arg === 'object' ? JSON.stringify(arg, null, 2) : String(arg)
    ).join(' '));
}};

console.warn = function(...args) {{
    outputs.push('Warning: ' + args.map(arg => 
        typeof arg === 'object' ? JSON.stringify(arg, null, 2) : String(arg)
    ).join(' '));
}};

try {{
    {code}
}} catch (e) {{
    outputs.push('Error: ' + e.message);
}}

console.log = originalLog;
console.error = originalError;
console.warn = originalWarn;

if (outputs.length > 0) {{
    originalLog(outputs.join('\\n'));
}} else {{
    originalLog('Code executed successfully (no output)');
}}
"""
                f.write(wrapped_code)
                temp_file = f.name

            # Execute the Node.js code with timeout
            result = subprocess.run(
                ["node", temp_file],
                capture_output=True,
                text=True,
                timeout=30,
            )

            execution_time = (time.time() - start_time) * 1000
            output = result.stdout.strip() if result.stdout else ""
            error = result.stderr.strip() if result.stderr else None

            return ExecutionResult(
                output=output or "Code executed successfully (no output)",
                error=error,
                executionTime=execution_time,
            )

        except subprocess.TimeoutExpired:
            execution_time = (time.time() - start_time) * 1000
            return ExecutionResult(
                output="",
                error="Execution timed out (30 second limit)",
                executionTime=execution_time,
            )
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            return ExecutionResult(
                output="",
                error=f"{type(e).__name__}: {str(e)}",
                executionTime=execution_time,
            )
