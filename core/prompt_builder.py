from core.curiosity import pick_hook

def build_prompt(user_input: str, memory) -> str:
    """
    Build a conversational prompt that:
      • Responds playfully to the child's topic
      • Weaves real learning into that topic
      • Occasionally drops a curiosity hook
    """
    # simple heuristic: drop a hook every 2nd turn
    use_hook = len(memory.data["history"]) % 2 == 1
    hook_txt = f"\nAdd this fun fact if it fits naturally: “{pick_hook()}”" if use_hook else ""

    return (
        "You are Spark, a playful mentor who teaches through curiosity loops.\n"
        "Guidelines:\n"
        "  - Always start with enthusiasm for the child’s topic.\n"
        "  - Teach by analogy: link their interest to at least one new skill (math, science, art, etc.).\n"
        "  - End with either a question or a creative mini‑project they can try.\n"
        f"Child said: {user_input}\n"
        f"{hook_txt}\n"
        "Spark, reply now:"
    )
