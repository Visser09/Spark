import json, os, random

_HOOK_FILE = os.path.join(os.path.dirname(__file__), "..", "hooks", "curiosity_hooks.json")

with open(_HOOK_FILE) as f:
    _HOOKS = json.load(f)

def pick_hook() -> str:
    """Return a random fun fact."""
    return random.choice(_HOOKS)
