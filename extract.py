import json
from pathlib import Path
import re

class ModelExtract:
    
    def __init__(self, ai_personality = "base"):
        self.custom_text = None
        self.ai_personality = ai_personality    
    
    def get_initial_prompt(self, load_mcg = True, load_calc_modeling = True, load_consumption_spec = False):
        # Loads the personality
        ai_personality = self.get_ai_personality()
        custom_text = ' '
        if (self.custom_text != None):
            custom_text = self.custom_text
            return ai_personality + '\n\n' + custom_text
        else:
            return ai_personality
    
    # Set ai_personality manually
    def set_ai_personality(self, personality):
        self.ai_personality = personality

    # Load the document containing the personalities
    def get_ai_personality(self):
        return self.load_ai_personality("initial_prompts.json")
        
    # Deletes the custom text from the system prompt
    def clear_custom_text(self):
        self.custom_text = None       
        
    # Sets the custom text
    def set_custom_text(self, text):
        self.custom_text = text

    # Returns the custom text's content
    def get_custom_text(self):
        return self.custom_text         

    # Loads the system prompt from the ingested file and finds the prompt according to the selected profile
    def load_ai_personality(self, file_name="initial_prompts.json"):
        try:
            with open(file_name) as f:
                file_content_dict = json.load(f)
            file_content=file_content_dict[self.ai_personality]
            f.close()
            return file_content
        except:
            print("Couldn't read file.")