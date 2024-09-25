def extract_text_from_txt(txt_path):
        with open(txt_path, 'r') as file:
            return file.read()