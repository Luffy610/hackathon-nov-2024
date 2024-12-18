import re
import pandas as pd
import logging

logger = logging.getLogger("utils")

def clean_code_snippet(code_string):
    cleaned_snippet = re.search(r'```(?:\w+)?\s*([\s\S]*?)\s*```', code_string)
    if cleaned_snippet:
        cleaned_snippet = cleaned_snippet.group(1)
    else:
        cleaned_snippet = code_string
    return cleaned_snippet

def clean_column_name(col_name):
    return re.sub(r'[^0-9a-zA-Z_]', '_', col_name)

def clean_column_names(df):
    cleaned_df = df.copy()
    cleaned_df.columns = [clean_column_name(col) for col in cleaned_df.columns]
    return cleaned_df

def read_dataframe(file, encoding='utf-8'):
    file_extension = file.filename.split(".")[-1]
    read_funcs = {
        'json': lambda: pd.read_json(file.file, orient='records'),
        'csv': lambda: pd.read_csv(file.file),
        'xls': lambda: pd.read_excel(file.file),
        'xlsx': lambda: pd.read_excel(file.file),
        'parquet': pd.read_parquet,
        'feather': pd.read_feather,
        'tsv': lambda: pd.read_csv(file.file, sep="\t")
    }
    if file_extension not in read_funcs:
        raise ValueError('Unsupported File Type.')
    try:
        df = read_funcs[file_extension]()
    except Exception as e:
        logger.error(f"Failed to read file: {file.filename}, Error: {e}.")
        raise
    cleaned_df = clean_column_names(df)
    return cleaned_df