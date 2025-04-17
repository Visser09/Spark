from models.phi_model import PhiModel
from core.memory import Memory
from core.prompt_builder import build_prompt

class SparkBrain:
    

    def build_prompt(self, user_input: str) -> str:
        return build_prompt(user_input, self.memory)


    def __init__(self):
        self.model = PhiModel()
        self.memory = Memory("memory_bank")

    def chat_loop(self):
        print("✨ Spark: Hi there! What’s sparking your curiosity today?")
        while True:
            user_input = input("You: ").strip()
            if user_input.lower() in {"exit", "quit"}:
                print("✨ Spark: Bye for now! Keep that curiosity glowing!")
                break

            prompt = build_prompt(user_input, self.memory)
            response = self.model.generate(prompt)
            print(f"✨ Spark: {response}")
            self.memory.update(user_input, response)
