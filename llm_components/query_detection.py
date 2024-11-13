import os
import openai


openai.api_key = os.environ.get("OPEN_AI_KEY")


def classify_query_intent(llm_engine, query):
    prompt = f"""
    You are an assistant that determines when to use either the "summarize" function or the "goal creator" function in a data analysis system.

    - Use the **summarize function** when the query is about providing a high-level overview, general summary, or quick recap of the data without specific goals or insights. These queries often contain phrases like "summarize," "overview," "quick summary," or "what’s in the data."

    - Use the **goal creator function** when the query asks for possible insights, analysis goals, or specific metrics that can be derived from the data. This function should also be used for requests about trends, distributions, averages, counts, and totals that require exploring specific relationships or extracting insights from the summary. Common phrases include "what insights can be derived," "analyze," "trends," "average," "goal," "metric," and "distribution."

    Here are some examples:

    - "Summarize the data for Q1 results." -> summarize function
    - "What insights can be derived from the sales data?" -> goal creator function
    - "Can you provide a quick summary of the customer demographics?" -> summarize function
    - "Show me the main metrics and goals we can extract from this dataset." -> goal creator function
    - "Give an overview of our revenue data." -> summarize function
    - "What are the main trends and insights in the data?" -> goal creator function

    Now classify the following query:
    "{query}"

    """

    response = openai.Completion.create(
        engine=llm_engine,
        prompt=prompt,
        max_tokens=10,
        temperature=0
    )

    intent = response.choices[0].text.strip()
    return intent