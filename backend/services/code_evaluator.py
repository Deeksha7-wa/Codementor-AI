import ast
import threading
from transformers import pipeline

# --- Global model (lazy loaded) ---
code_hint_model = None
model_loading = False

def get_model():
    """Load the GPT-2 model only once, when first used."""
    global code_hint_model, model_loading
    if code_hint_model is None and not model_loading:
        model_loading = True
        try:
            print("⏳ Loading GPT-2 model...")
            # Tiny model → much faster cold starts on Render
            code_hint_model = pipeline("text-generation", model="sshleifer/tiny-gpt2")
            print("✅ GPT-2 model loaded successfully.")
        except Exception as e:
            print(f"⚠️ Model load failed: {e}")
        finally:
            model_loading = False
    return code_hint_model


def evaluate_python_code(code: str):
    """Analyze Python code using AST + optional AI hints."""
    errors, hints, suggestions = [], [], []

    # --- Static rule-based checks ---
    try:
        ast.parse(code)
        hints.append("Code syntax is correct.")
    except SyntaxError as e:
        errors.append(str(e))
        hints.append("Check syntax: possible indentation or missing colon.")

    # Basic static suggestion
    suggestions.append("Consider using functions for reusable code blocks.")

    # --- AI-generated hints (non-blocking safe mode) ---
    try:
        model = get_model()
        if model:
            prompt = f"Suggest simple, understandable improvements for this Python code:\n{code}\nHints:"
            ai_result = model(prompt, max_length=80, num_return_sequences=1)
            ai_text = ai_result[0]["generated_text"].split("Hints:")[-1].strip()
            if ai_text:
                hints.append(ai_text)
        else:
            hints.append("AI hint model not ready yet — try again shortly.")
    except Exception as e:
        print(f"⚠️ AI generation failed: {e}")
        hints.append("AI hint temporarily unavailable — fallback to static analysis.")

    return {"errors": errors, "hints": hints, "suggestions": suggestions}


def evaluate_javascript_code(code: str):
    """Placeholder for JS support."""
    return {
        "errors": [],
        "hints": ["Basic JavaScript support coming soon."],
        "suggestions": []
    }


def evaluate_code(language: str, code: str):
    """Dispatch evaluation by language."""
    lang = language.lower()
    if lang == "python":
        return evaluate_python_code(code)
    elif lang == "javascript":
        return evaluate_javascript_code(code)
    else:
        return {"errors": [f"Language '{language}' not supported."], "hints": [], "suggestions": []}




