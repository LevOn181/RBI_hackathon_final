import pandas as pd
import json

def extract_text_from_excel(file_path):
        try:
        # Read the entire Excel file into a dictionary of DataFrames
            excel_data = pd.read_excel(file_path, sheet_name=None)
            
            # Convert each DataFrame to a list of dictionaries,
            # ensuring that each value is converted to a serializable format
            data = {
                sheet_name: data.applymap(lambda x: x.isoformat() if isinstance(x, pd.Timestamp) else x).to_dict(orient='records')
                for sheet_name, data in excel_data.items()
            }
            
            data_json = json.dumps(data)
            print("Data:"+data_json)
            return data_json
        except Exception as e:
            print(f"An error occurred while reading the Excel file: {e}")
            return None