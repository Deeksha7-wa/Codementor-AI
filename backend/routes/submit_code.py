from fastapi import APIRouter, Query
from backend.models.code_submission import CodeSubmission
from backend.services.code_evaluator import evaluate_code
from backend.db.database import Submission, SessionLocal
import json

router = APIRouter()

# Save submission
def save_submission(data):
    session = SessionLocal()
    submission = Submission(
        user_id=data["user_id"],
        language=data["language"],
        code=data["code"],
        errors=json.dumps(data["errors"]),
        hints=json.dumps(data["hints"]),
        suggestions=json.dumps(data["suggestions"]),
    )
    session.add(submission)
    session.commit()
    session.close()

@router.post("/submit-code")
def submit_code(submission: CodeSubmission):
    result = evaluate_code(submission.language, submission.code)

    # Save synchronously
    data_to_save = {
        "user_id": submission.user_id,
        "language": submission.language,
        "code": submission.code,
        "errors": result["errors"],
        "hints": result["hints"],
        "suggestions": result["suggestions"],
    }
    save_submission(data_to_save)

    return {
        "status": "success",
        "user_id": submission.user_id,
        "language": submission.language,
        **result
    }

@router.get("/history")
def get_history(user_id: str = Query("anonymous")):
    session = SessionLocal()
    submissions = session.query(Submission).filter(Submission.user_id == user_id).all()
    session.close()
    return [
        {
            "id": s.id,
            "language": s.language,
            "code": s.code,
            "errors": json.loads(s.errors),
            "hints": json.loads(s.hints),
            "suggestions": json.loads(s.suggestions),
            "timestamp": s.timestamp,
        }
        for s in submissions
    ]


