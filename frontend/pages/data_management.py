import pandas as pd
from utils.excel_handler import dataframe_to_excel, validate_columns
def inspect_import(uploaded_file, required_columns):
    dataframe = pd.read_excel(uploaded_file); return dataframe, validate_columns(dataframe, required_columns)
