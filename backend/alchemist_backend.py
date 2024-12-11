import json
from fastapi import FastAPI, UploadFile, File
from fastapi import Path
import os
import io, sys
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn

sys.path.append("../")
from llm_components.manager import Manager, llm
from utils.datamodels import Goal
from utils.utils import read_dataframe


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
root_file_path = os.path.dirname(os.path.abspath(__file__))
files_static_root = os.path.join(root_file_path, "files/")
data_folder = os.path.join(root_file_path, "files","data")
global df, summary

text_gen = llm(
    provider="openai",
    api_type="azure",
    azure_endpoint="https://genai-openai-iamtechtitans.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview",
    api_key="your-api-key",
    api_version="2023-07-01-preview"
)

bot = Manager(text_gen=text_gen)

app.mount("/ui", StaticFiles(directory=os.path.join(os.getcwd(), "..", "ui")), name="static")

@app.get("/", response_class = HTMLResponse )
def read_root():
    with open(os.path.join(os.getcwd(), "..","ui","index.html"), "r") as f:
        return HTMLResponse(content=f.read())

@app.post("/items/{item_id}")
def read_item(item_id:int, q: str = None):
    return {"item_id":item_id, "q":q}

@app.post("/uploadfile/")
def upload_file(file: UploadFile = File(...), title="The file path", description="Path to the file to process"):
    # Example of processing the file path and returning a dictionary
    #file_path = os.path.join(data_folder, file.filename)
    global df
    df=read_dataframe(file)

    return "File Uploaded Successfully"

@app.get("/defaultchart/")
def process_file():
    # Example of processing the file path and returning a dictionary
    #file_path = os.path.join(data_folder, file.filename)
    global df, summary

    summary = bot.summarize(data=df,summary_method='llm')

    goals = bot.goals(summary)

    chart_code = bot.chart_generator(goal=goals[0],summary=summary, library='matplotlib')
    chart_resp_in_list_of_bytearrays = bot.execute(code_specs=chart_code,data=df,summary=summary,library='matplotlib')

    # Return a dictionary with the two items
    return {
        "summary": summary,
        "goals": goals,
        "chart_response": f"data:image/png;base64,{chart_resp_in_list_of_bytearrays[0].raster}",
        "chart_code" : chart_code[0]
    }


@app.get("/generatechart/")
def generate_chart(goal):
    if isinstance(goal,dict):
        g = Goal(
            question = goal["question"],
            visualization = goal["visualization"],
            rationale = goal["rationale"]
        )
    else: #expecting string
        g = Goal(
            question = goal,
            visualization = "",
            rationale = ""
        )

    chart_code = bot.chart_generator(goal=g,summary=summary, library='matplotlib')
    chart_resp_in_list_of_bytearrays = bot.execute(code_specs=chart_code,data=df,summary=summary,library='matplotlib')
    return {
        "chart_response": f"data:image/png;base64,{chart_resp_in_list_of_bytearrays[0].raster}",
        "chart_code" : chart_code[0]
    }

@app.get("/explain/")
def chart_explainer(code):
    code=code.replace(" ", "%20")
    code=code.replace("\n", "%0A")
    code = code.strip()
    print(code)
    print(bot.explain(code=code))
    return bot.explain(code=code)[0]

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8080)