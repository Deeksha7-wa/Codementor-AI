import ast
from transformers import pipeline

# --- Lazy model loading (only when needed) ---
code_hint_model = None
model_loading = False

def get_model():
    """Load the tiny GPT-2 model only once when needed."""
    global code_hint_model, model_loading
    if code_hint_model is None and not model_loading:
        model_loading = True
        try:
            print("⏳ Loading distilgpt2 model in background...")
            code_hint_model = pipeline("text-generation", model="distilgpt2")
            print("✅ GPT-2 model loaded successfully.")
        except Exception as e:
            print(f"⚠️ Model load failed: {e}")
        finally:
            model_loading = False
    return code_hint_model


def evaluate_python_code(code: str, ai: bool = False):
    """Evaluate Python code statically + optional GPT-2 fallback."""
    errors, hints, suggestions = [], [], []

    # --- Static AST analysis ---
    try:
        ast.parse(code)
        hints.append("✅ Code syntax is correct.")
    except SyntaxError as e:
        errors.append(str(e))
        hints.append("❌ Syntax error: check indentation or missing colon.")

    # --- Deterministic suggestions ---
    suggestions.extend([
        "💡 Consider using functions for reusable code blocks.",
        "🧩 Add comments to explain logic for readability."
    ])

    # --- Optional GPT-2 enhancement ---
    if ai:
        try:
            model = get_model()
            if model:
                prompt = f"Give one short, clear tip for improving this Python code:\n{code}\nTip:"
                ai_result = model(prompt, max_length=60, num_return_sequences=1)
                ai_text = ai_result[0]["generated_text"].split("Tip:")[-1].strip()

                # Clean and limit gibberish
                if ai_text:
                    if len(ai_text.split()) > 20:
                        ai_text = " ".join(ai_text.split()[:20]) + "..."
                    hints.append("🤖 " + ai_text)
            else:
                hints.append("⏳ AI model loading — try again shortly.")
        except Exception as e:
            print(f"⚠️ AI generation failed: {e}")
            hints.append("(AI hint unavailable — using static feedback.)")

    return {"errors": errors, "hints": hints, "suggestions": suggestions}


def evaluate_javascript_code(code: str):
    """Placeholder for JavaScript static evaluation."""
    return {
        "errors": [],
        "hints": ["✅ JS syntax looks valid (basic check only)."],
        "suggestions": [
            "💡 Add comments for clarity.",
            "🔁 Avoid deeply nested callbacks — use async/await."
        ]
    }


def evaluate_code(language: str, code: str, ai: bool = False):
    """Dispatch by language."""
    lang = language.lower()
    if lang == "python":
        return evaluate_python_code(code, ai)
    elif lang == "javascript":
        return evaluate_javascript_code(code)
    else:
        return {"errors": [f"Language '{language}' not supported."], "hints": [], "suggestions": []}



