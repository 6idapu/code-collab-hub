"""Code execution service."""

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
        """Execute JavaScript code.

        Note: This is a simplified implementation that returns a message
        suggesting that JavaScript execution should be done in the frontend.
        For production, consider using Node.js or a WebAssembly runtime.
        """
        return ExecutionResult(
            output="JavaScript/TypeScript execution requires a Node.js runtime. "
            "For now, this should be executed in the browser.",
            error=None,
            executionTime=1.0,
        )
