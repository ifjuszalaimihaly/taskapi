from openai import OpenAI
from dotenv import load_dotenv
import os

from .schemas import TaskList

# Load environment variables from .env file (e.g., OPENAI_API_KEY)
load_dotenv()

# Service class for interacting with the OpenAI API
class OpenAIService():

    # Generates a natural language prompt from a list of task items
    def generate_prompt(self, items):
        # Combine task string representations into a single list separated by newlines
        task_list = '\n'.join(str(item) for item in items)
        
        # Build the instruction prompt for the language model
        prompt_text = f'''Based on the task list below, generate 2 to 5 new tasks that are thematically related to the original items.
                    Each line in the task list represents one existing task.

                    Your job is to suggest what the task creator should do next, inspired by the existing to-do list.
                    The language of your response should match the language of the original tasks.

                    Return your answer in **JSON format**.
                    Each suggested task must include the following fields:
                    - title
                    - description
                    - due_date
                    - status (this must always be "pending")

                    This is the task list:
                    {task_list}
                    '''
        return prompt_text

    # Sends the prompt to OpenAI and parses the structured JSON response into a TaskList
    def generate_taks(self, items):
        # Create OpenAI client using the API key from environment
        client = OpenAI()

        # Send prompt and request a structured JSON response
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": self.generate_prompt(items)
                }
            ],
            response_format = TaskList  # Expected structured response format
        )

        # Return the parsed TaskList object from the LLM response
        return completion.choices[0].message.parsed
