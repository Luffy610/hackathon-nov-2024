import json
import logging
from json import JSONDecodeError
from utils.utils import clean_code_snippet
from utils.datamodels import Goal, Persona

SYSTEM_INSTRUCTIONS = """
You are a an experienced data analyst who can generate a given number of insightful GOALS about data, 
when given a summary of the data, and a specified persona. 
The VISUALIZATIONS YOU RECOMMEND MUST FOLLOW VISUALIZATION BEST PRACTICES 
(e.g., must use bar charts instead of pie charts for comparing quantities) AND BE 
MEANINGFUL (e.g., plot longitude and latitude on maps where appropriate). 
They must also be relevant to the specified persona. 
Each goal must include a question, a visualization 
(THE VISUALIZATION MUST REFERENCE THE EXACT COLUMN FIELDS FROM THE SUMMARY), 
and a rationale (JUSTIFICATION FOR WHICH dataset FIELDS ARE USED and what we will learn from the visualization). 
Each goal MUST mention the exact fields from the dataset summary above
"""

FORMAT_INSTRUCTIONS = """
THE OUTPUT MUST BE A CODE SNIPPET OF A VALID LIST OF JSON OBJECTS. IT MUST USE THE FOLLOWING FORMAT:

```[
    { "index": 0,  
    "question": "What is the distribution of X", 
    "visualization": "histogram of X", 
    "rationale": "This tells about "} ..
    ]
```
THE OUTPUT SHOULD ONLY USE THE JSON FORMAT ABOVE.
"""

logger = logging.getLogger("goal_generator")

class GoalGenerator:

    def generate(self, summary, text_config, text_gen, no_of_goals, persona):

        user_prompt = f"""The number of GOALS to generate is {no_of_goals}. 
        The goals should be based on the data summary below, \n\n.
        {summary} \n\n"""

        if not persona:
            persona = Persona(
                persona="A highly skilled data analyst who can come up with complex, insightful goals about data",
                rationale=""
            )

        user_prompt += f"""\n The generated goals SHOULD BE FOCUSED ON THE INTERESTS AND PERSPECTIVE of a '{persona.persona} persona, who is interested in complex, insightful goals about the data. \n"""

        messages = [
            {"role": "system", "content": SYSTEM_INSTRUCTIONS},
            {"role": "assistant",
             "content":
                 f"{user_prompt}\n\n {FORMAT_INSTRUCTIONS} \n\n. The generated {no_of_goals} goals are: \n "}]

        result = text_gen.generate(messages=messages, config=text_config)

        try:
            json_string = clean_code_snippet(result.text[0]["content"])
            result = json.loads(json_string)
            if isinstance(result,dict):
                result = [result]
            result = [Goal(**x) for x in result]

        except JSONDecodeError:
            logger.error(f"Error decoding JSON: {result.text[0]['content']}")
            raise ValueError(
                "The model did not return a valid JSON object while attempting generate goals. "
                "Consider using a larger model or a model with higher max token length.")

        return result