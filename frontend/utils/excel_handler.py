from io import BytesIO
import pandas as pd
def dataframe_to_excel(dataframe):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer: dataframe.to_excel(writer, index=False, sheet_name='export')
    return output.getvalue()
def validate_columns(dataframe, required):
    return [column for column in required if column not in dataframe.columns]
