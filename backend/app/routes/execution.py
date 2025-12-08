"""Code execution routes."""

from fastapi import APIRouter, HTTPException, status
from app.models import ExecuteCodeRequest, ExecutionResult
from app.services import CodeExecutionService

router = APIRouter(prefix="/api/v1", tags=["Code Execution"])


@router.post("/execute", response_model=ExecutionResult)
async def execute_code(request: ExecuteCodeRequest):
    """Execute code in the specified language.

    Args:
        request: Code execution request with code, language, and optional timeout

    Returns:
        ExecutionResult with output, error, and execution time

    Raises:
        HTTPException: If execution fails or times out
    """
    try:
        result = await CodeExecutionService.execute(
            code=request.code, language=request.language, timeout=request.timeout
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "EXECUTION_ERROR",
                "message": f"Failed to execute code: {str(e)}",
                "statusCode": 500,
            },
        )
