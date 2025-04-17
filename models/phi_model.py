from llama_cpp import Llama
from config import MODEL_PATH

class PhiModel:
    """Thin wrapper around a local Phi‑3 model."""

    def __init__(self, model_path: str = MODEL_PATH, max_tokens: int = 150):  # lowered to reduce rambling
        self.llm = Llama(model_path=model_path, n_ctx=4096)
        self.max_tokens = max_tokens

    def generate(self, prompt: str) -> str:
        out = self.llm(
            prompt,
            max_tokens=self.max_tokens,
            stop=["\nYou:", "\nChild:", "\nSpark:", "<|end|>", "<|endoftext|>"]
        )

        if isinstance(out, dict):
            text = out["choices"][0]["text"].strip()
        else:
            text = out.strip()

        # 🧠 Optional Bonus: Trim rambling or looping endings
        if "Now, let's explore" in text:
            text = text.split("Now,")[0].strip() + " Now, let's try something fun!"

        if text.endswith("Let's"):
            text += " try something fun!"

        return text
