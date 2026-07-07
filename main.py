from openai import OpenAI
import os
import json

class CookingAgent:
    def __init__(self):
        """
        AI agent creation using ChatGPT 4.1. Loads the history of recommended ingredients and recipes (and creates the
        json file if it doesn't exist).
        """
        # Agent config
        self.client = OpenAI(
            base_url="https://models.github.ai/inference",
            api_key=os.environ["GITHUB_TOKEN"]
        )
        self.model_name = "openai/gpt-4.1"

        # Set agent's tools
        self.setup_tools()

        # Ensure needed structure is OK
        if not os.path.exists('recipes_history.json'):
            with open("recipes_history.json", "w") as history:
                history.write("{}")

        # Reads history file (long-term memory)
        with open('recipes_history.json', 'r') as f:
            self.history = json.load(f)

        # Short-term memory
        self.current_session = [
            {
                "role": "system",
                "content": "You're a profesional chef focused on balanced nutrition and a cooking influencer who "
                           "likes innovation and modern recipes."
                           ""
                           "When you decide to write down the final recipe, you have to ask the user to confirm if "
                           "he wants that recipe (ask him to write 'ok' or 'no')."
            }
        ]

        pass

    def setup_tools(self):
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "recipe_response",
                    "description": "Propose a final recipe idea following the desired structure",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            }
        ]

        pass

    def normal_response(self, prompt):

        recipe_idea = False
        # Saves user's prompt
        self.current_session.append(
            {
                "role": "user",
                "content": prompt
            }
        )
        # Builds a response for the user conversation
        response = self.client.chat.completions.create(
            model = self.model_name,
            messages = self.current_session,
            tools = self.tools
        )
        # Saves agent's response
        self.current_session.append(response.choices[0].message)

        if response.choices[0].message.tool_calls is not None:
            for tc in response.choices[0].message.tool_calls:
                if tc.function.name == "recipe_response":
                    # Flag have control on the final recipe
                    recipe_idea = True

                    elaboration = self.recipe_response()
                    self.current_session.append(
                        {
                            "role": "tool",
                            "tool_call_id": tc.id,
                            "content": elaboration
                        }
                    )
                    return elaboration, recipe_idea

        return response.choices[0].message.content, recipe_idea

    def recipe_response(self, language="spanish"):
        # Builds the response
        response = self.client.chat.completions.create(
            model = self.model_name,
            messages = [
                {
                "role": "user",
                "content": f"Explain me the recipe you are thinking about. You must structure the response into 4"
                           f"parts:"
                           f"- Introduction: Before listing all ingredients, you have to indicate how many people is the "
                           f"recipe for, how long would you be cooking and the difficulty of the recipe in a 5 stars scale."
                           f"- Ingredients:  Then, you have to list ingredients and the amount it is used."
                           f"- Elaboration: You have to indicate different steps to follow correctly the cooking process. "
                           f"It must be easy to understand, and you can include advises and variations (not necessary)."
                           f"- Macros: At the end, you have to estimate, looking at the ingredients, the calories of "
                           f"the recipe and its macros."
                           f"- Advises: This is an optional part in which you can resume all the advises or variations "
                           f"that the recipe could have."
                           f"(You answer must be in {language})"
                }
            ]
        )

        return response.choices[0].message.content

    def final_response(self):
        # Add the recipe to the json file

        # Export the response to PDF
        pass

    def check_history(self):
        pass

    def search_recipe(self):
        pass

    def filter_ingredients(self):
        pass

    def macros_calculation(self):
        pass


if __name__ == "__main__":
    agent = CookingAgent()
    recipe_idea = False
    while True:
        prompt_message = str(input("Tú: "))

        if recipe_idea and prompt_message.lower() in ["hecho", "ok", "perfecto", "exportar"]:
            agent.final_response()
            break

        response, recipe_idea = agent.normal_response(prompt_message)

        print("Agente: ", response, recipe_idea)