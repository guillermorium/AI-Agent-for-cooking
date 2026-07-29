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

        # Set agent's tools and attributes
        self.setup_attributes()
        self.setup_tools()

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

    def setup_attributes(self):
        # Long-term memory check
        if not os.path.exists('recipes_history.json'):
            with open("recipes_history.json", "w") as history:
                history.write("{}")

        # Reads history file (long-term memory)
        with open('recipes_history.json', 'r') as f:
            self.history = json.load(f)

        # The recipe proposal
        self.current_recipe = None
        # Flag to check if the user likes the recipe proposal
        self.recipe_idea = False

        pass

    def setup_tools(self):
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "recipe_response",
                    "description": "Propose a recipe idea following a fixed structure",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "current_recipe": {
                                "type": "string",
                                "description": "A recipe proposal to the user"
                            }
                        },
                        "required": ["current_recipe"]
                    }
                }
            }
        ]

        pass

    def normal_response(self, prompt):
        """
        Main function to build a response for the user and to continue the conversation.

        param prompt: user's message
        return response: agent's response
            recipe_idea: flag to check the end of the conversation
        """
        self.recipe_idea = False
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
                    self.recipe_idea = True
                    # Get the proposal recipe
                    self.current_recipe = json.loads(tc.function.arguments)["current_recipe"]
                    # Build the response
                    elaboration = self.recipe_response(self.current_recipe)
                    self.current_session.append(
                        {
                            "role": "tool",
                            "tool_call_id": tc.id,
                            "content": elaboration
                        }
                    )
                    return elaboration, self.recipe_idea

        return response.choices[0].message.content, self.recipe_idea

    def recipe_response(self, current_recipe: str, language="spanish"):
        # Builds the response
        response = self.client.chat.completions.create(
            model = self.model_name,
            messages = [
                {
                "role": "user",
                "content": f"Explain the recipe {current_recipe}. You must structure the response into 4 parts:"
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

    def export_response(self):
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

    while True:
        prompt_message = str(input("Usuario: "))

        if agent.recipe_idea and prompt_message.lower() in ["hecho", "ok", "perfecto", "exportar"]:
            agent.export_response()
            break

        response, agent.recipe_idea = agent.normal_response(prompt_message)

        print("Agente: ", response)