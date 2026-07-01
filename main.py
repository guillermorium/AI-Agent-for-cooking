from openai import OpenAI
import os
import json

class CookingAgent:
    def __init__(self):
        # AI agent creation. It will use Claude as LLM
        self.client = OpenAI(
            base_url="https://models.github.ai/inference",
            api_key=os.environ["GITHUB_TOKEN"]
        )
        self.model_name = "openai/gpt-4.1"

        # Ensure needed structure is OK
        if not os.path.exists('recipes_history.json'):
            with open("recipes_history.json", "w") as history:
                history.write("{}")


        pass

    def setup_tools(self):
        pass

    def check_history(self):
        pass

    def search_recipe(self):
        pass

    def filter_ingredients(self):
        pass

    def macros_calculation(self):
        pass

    def recipe_output(self, recipe):
        # Builds the response
        response = self.client.chat.completions.create(
            model = self.model_name,
            messages = [
                {
                "role": "user",
                "content": "Dime 3 personajes de Juego de tronos"
                }
            ]
        )

        return response.choices[0].message.content


if __name__ == "__main__":
    agent = CookingAgent()

    response = agent.recipe_output("Cooking")
    print(response)