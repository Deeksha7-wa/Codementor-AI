import ast
from transformers import pipeline

# Don't load the model yet — wait until it's first needed
code_hint_model = None

def get_model():
    """Load the tiny GPT-2 model only once, when first used."""
    global code_hint_model
    if code_hint_model is None:
        code_hint_model = pipeline("text-generation", model="hf-internal-testing/tiny-random-gpt2")
    return code_hint_model


def evaluate_python_code(code: str):
    errors = []
    hints = []
    suggestions = []

    # --- Static analysis ---
    try:
        ast.parse(code)
        hints.append("Code syntax is correct.")
    except SyntaxError as e:
        errors.append(str(e))
        hints.append("Check syntax: possible indentation or missing colon.")

    suggestions.append("Consider using functions for reusable code blocks.")

    # --- AI-generated hints ---
    model = get_model()  # Load only when first needed
    prompt = f"Suggest improvements or hints for this Python code:\n{code}\nHints:"
    ai_result = model(prompt, max_length=100, num_return_sequences=1)
    ai_text = ai_result[0]["generated_text"].split("Hints:")[-1].strip()
    if ai_text:
        hints.append(ai_text)

    return {
        "errors": errors,
        "hints": hints,
        "suggestions": suggestions
    }


def evaluate_javascript_code(code: str):
    # Placeholder for future JS analysis
    return {
        "errors": [],
        "hints": ["AI hint support coming soon for JavaScript."],
        "suggestions": []
    }


def evaluate_code(language: str, code: str):
    """Dispatch code evaluation based on language."""
    if language.lower() == "python":
        return evaluate_python_code(code)
    elif language.lower() == "javascript":
        return evaluate_javascript_code(code)
    else:
        return {
            "errors": [f"Language '{language}' not supported."],
            "hints": [],
            "suggestions": []
        }

