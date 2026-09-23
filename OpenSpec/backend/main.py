from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from decimal import Decimal
from evaluator import evaluate_expression

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Web Calculator API",
    description="API for high-precision mathematical expression parsing and evaluation.",
    version="1.0.0"
)

# Configure CORS Middleware to allow requests from the React frontend development server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for seamless local multi-port development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ExpressionPayload(BaseModel):
    expression: str

class EvaluationResponse(BaseModel):
    result: float

@app.post("/api/v1/evaluate", response_model=EvaluationResponse)
def evaluate(payload: ExpressionPayload):
    try:
        res = evaluate_expression(payload.expression)
        return EvaluationResponse(result=res)
    except ZeroDivisionError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during evaluation: {str(e)}"
        )
