
from utils.datamodels import Goal
from chart_code_template import ChartTemplate


SYSTEM_PROMPT = """You are a helpful assistant highly skilled in writing PERFECT code for visualizations. 
Given some code template, you complete the template to generate a visualization given the dataset and the goal described. 
The code you write MUST FOLLOW VISUALIZATION BEST PRACTICES ie. meet the specified goal, 
apply the right transformation, use the right visualization type, 
use the right data encoding, and use the right aesthetics (e.g., ensure axis are legible). 
The transformations you apply MUST be correct and the fields you use MUST be correct. 
The visualization CODE MUST BE CORRECT and MUST NOT CONTAIN ANY SYNTAX OR LOGIC ERRORS 
(e.g., it must consider the field types and use them correctly). 
You MUST first generate a brief plan for how you would solve the task 
e.g. what transformations you would apply 
e.g. if you need to construct a new column, what fields you would use, what visualization type you would use, 
what aesthetics you would use, etc. .
"""

class ChartGenerator:

    def __init__(self):
        self.template = ChartTemplate()


    def generate(self, summary, goal, text_gen_config, text_gen, library="altair"):

        library_template, library_instructions = self.template.get_template(goal=goal, library=library)
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "system", "content": f"The dataset summary is : {summary} \n\n"},
            library_instructions,
            {"role": "user",
             "content":
                 f"Always add a legend with various colors where appropriate. "
                 f"The visualization code MUST only use data fields that exist in the dataset "
                 f"(field_names) or fields that are transformations based on existing field_names). "
                 f"Only use variables that have been defined in the code or are in the dataset summary. "
                 f"You MUST return a FULL PYTHON PROGRAM ENCLOSED IN BACKTICKS ``` "
                 f"that starts with an import statement. "
                 f"DO NOT add any explanation. \n\n "
                 f"THE GENERATED CODE SOLUTION SHOULD BE CREATED BY MODIFYING THE SPECIFIED PARTS OF THE "
                 f"TEMPLATE BELOW \n\n {library_template} \n\n."
                 f"The FINAL COMPLETED CODE BASED ON THE TEMPLATE above is ... \n\n"}]

        result = text_gen.generate(messages=messages, config = text_gen_config)

        response = [x['content'] for x in result.text]

        return response