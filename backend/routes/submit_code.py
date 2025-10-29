from fastapi import APIRouter, Query, HTTPException
from backend.models.code_submission import CodeSubmission
from backend.services.code_evaluator import evaluate_code
from backend.db.database import Submission, SessionLocal
import json

router = APIRouter()

# --- Save a submission record ---
def save_submission(data):
    session = SessionLocal()
    try:
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
    except Exception as e:
        session.rollback()
        print(f"⚠️ Error saving submission: {e}")
    finally:
        session.close()


# --- Main endpoint: submit code for evaluation ---
@router.post("/submit-code")
def submit_code(submission: CodeSubmission):
    try:
        # Run rule-based + GPT-2 evaluation
        result = evaluate_code(submission.language, submission.code)

        # Save results
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating code: {e}")


# --- Fetch all submissions for a user ---
@router.get("/history")
def get_history(user_id: str = Query("anonymous")):
    session = SessionLocal()
    try:
        submissions = (
            session.query(Submission)
            .filter(Submission.user_id == user_id)
            .order_by(Submission.timestamp.desc())
            .all()
        )

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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching history: {e}")
    finally:
        session.close()
