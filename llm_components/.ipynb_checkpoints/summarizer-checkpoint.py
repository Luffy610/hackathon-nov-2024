import json
import logging
import warnings
import pandas as pd
from utils.utils import clean_code_snippet

SYSTEM_PROMPT = """
You are an experienced data analyst that can annotate datasets. Your instructions are as follows:
i) ALWAYS generate the name of the dataset and the dataset_description
ii) ALWAYS generate a field description.
iii.) ALWAYS generate a semantic_type (a single word) for each field given its values e.g. company, city, number, supplier, location, gender, longitude, latitude, url, ip address, zip code, email, etc
You must return an updated JSON dictionary without any preamble or explanation.
"""

logger = logging.getLogger("summarizer")

class Summarizer:
    def __init__(self):
        self.summary = None

    def check_type(self, dtype, value):
        if "float" in str(dtype):
            return float(value)
        elif "int" in str(dtype):
            return int(value)
        else:
            return value

    def get_column_properties(self, df, n_samples):
        properties_list = []
        for column in df.columns:
            logger.info(f"Getting properties of column: {column}")
            dtype = df[column].dtype
            properties = {}
            if dtype in [int, float, complex]:
                properties["dtype"] = "number"
                properties["std"] = self.check_type(dtype, df[column].std())
                properties["min"] = self.check_type(dtype, df[column].min())
                properties["max"] = self.check_type(dtype, df[column].max())
            elif dtype == bool:
                properties["dtype"] = "boolean"
            elif dtype == object:
                try:
                    with warnings.catch_warnings():
                        warnings.simplefilter('ignore')
                        pd.to_datetime(df[column], errors='raise')
                        properties['dtype'] = "date"
                except ValueError:
                    if df[column].nunique() / len(df[column]) < 0.5:
                        properties["dtype"] = "category"
                    else:
                        properties["dtype"] = "string"

            elif pd.api.types.is_categorical_dtype(df[column]):
                properties["dtype"] = "category"
            elif pd.api.types.is_datetime64_any_dtype(df[column]):
                properties["dtype"] = "date"
            else:
                properties["dtype"] = str(dtype)

            if properties["dtype"] == "date":
                try:
                    properties["min"] = df[column].min()
                    properties["max"] = df[column].max()
                except TypeError:
                    caste_date_col = pd.to_datetime(df[column], errors='coerce')
                    properties["min"] = caste_date_col.min()
                    properties["max"] = caste_date_col.max()

            n_unique = df[column].nunique()
            if "samples" not in properties:
                non_null_values = df[column][df[column].notnull()].unique()
                n_samples = min(n_samples, len(non_null_values))
                samples = pd.Series(non_null_values).sample(n_samples, random_state=42).tolist()
                properties["samples"] = samples

            properties["num_unique_values"] = n_unique
            properties["semantic_type"] = ""
            properties["description"] = ""
            properties_list.append({"column":column, "properties":properties})
        logger.info("Properties of all column successfully generated")
        return properties_list

    def enrich_summary(self, base_summary, text_gen, text_gen_config):
        logger.info(f"Enriching data summary")
        messages = [
            {
                "role" : "system",
                "content" : SYSTEM_PROMPT
            },
            {
                "role" : "assistant",
                "content" : f""" Annotate the dictionary below. Only return a JSON object {base_summary}"""
            }
        ]

        response = text_gen.generate(messages=messages, config=text_gen_config)
        enriched_summary = base_summary
        try:
            json_string = clean_code_snippet(response.text[0]["content"])
            enriched_summary = json.loads(json_string)
        except json.decoder.JSONDecodeError:
            error_msg = f"The model did not return a valid JSON object while attempting to generate an enriched data summary. Consider using a default summary or  a larger model with higher max token length. | {response.text[0]['content']}"
            logger.info(error_msg)
            logger.info(response.text[0]["content"])
            raise ValueError(error_msg + "" + response.usage)
        return enriched_summary

    def summarize(self, data, text_gen, file_name, n_samples, text_gen_config, summary_method):
        data_properties = self.get_column_properties(data, n_samples)
        base_summary = {
            "name" : file_name,
            "file_name" : file_name,
            "dataset_description" : "",
            "fields" : data_properties
        }
        data_summary = base_summary
        if summary_method == "llm":
            data_summary = self.enrich_summary(
                base_summary=base_summary,
                text_gen=text_gen,
                text_gen_config=text_gen_config
            )
        elif summary_method == "columns":
            del data_summary["fields"]

        data_summary["fields"] = data.columns.to_list()
        data_summary["file_name"] = file_name
        return data_summary