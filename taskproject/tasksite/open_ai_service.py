from openai import OpenAI
from dotenv import load_dotenv
import os

from .schemas import TaskList

load_dotenv()

class OpenAIService():


    def generate_prompt(self, items):
        task_list = '\n'.join(str(item) for item in items)
        
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

    def generate_taks(self, items):

        client = OpenAI()

        completion = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": self.generate_prompt(items)
                }
            ],
            response_format = TaskList
        )

        return completion.choices[0].message.parsed



