import json

from xlwings.base_classes import Chart

from utils.utils import clean_code_snippet
from llmx import TextGenerator, TextGenerationConfig, TextGenerationResponse
from llm_components.chart_code_template import ChartTemplate

system_prompt = """
You are a helpful assistant highly skilled in providing helpful, structured explanations of visualization of the plot(data: pd.DataFrame) method in the provided code. You divide the code into sections and provide a description of each section and an explanation. The first section should be named "accessibility" and describe the physical appearance of the chart (colors, chart type etc), the goal of the chart, as well the main insights from the chart.
You must explain the code from non technical person point of view describing in brief what are the insights we get from the chart
"""

format_instructions = """
Your output MUST be perfect string explaining the insights of chart in detail with atleast 6 to 7 lines, no LINES MUST BE REPEATED in context perspective too.
"""

class ChartExplainer:
    def __init__(self):
        self.template = ChartTemplate()

    def explain(self,
                code: str,
                textgen_config: TextGenerationConfig,
                text_gen: TextGenerator,
                library: str ="matplotlib"
                ):

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "assistant", "content": f"The code to be explained is {code}. \n=============\n"},
            {"role": "user", "content": f"{format_instructions}. \n\n The structured explanation for the above code is \n\n"}
        ]

        completions: TextGenerationResponse = text_gen.generate(messages=messages, config=textgen_config)

        completions = [clean_code_snippet(str(x['content'])) for x in completions.text]


        return completions