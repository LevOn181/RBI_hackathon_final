import pandas as pd

def extract_text_from_csv(file_path):
        df = pd.read_csv(file_path, encoding="utf-8")
        json_string = df.to_json(orient='records')
        # Print or use the JSON string
        print(json_string)
        return json_string

