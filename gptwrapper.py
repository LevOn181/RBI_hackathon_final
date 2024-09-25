from openai import OpenAI, AsyncOpenAI
import base64
from PIL import Image
import io
import os


class GPTWrapper:

    def __init__(self, openai_model = 'gpt-4o'):
        self.client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.settings = {
            "model": openai_model,
            "temperature": 0.7,
            "max_tokens": 1000
        }
        return

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def encode_image_from_files(self, image):
        if not isinstance(image, Image.Image):
            image = Image.open(io.BytesIO(image))
        if image.mode and image.mode == 'RGBA':
            image = image.convert('RGB')

        with io.BytesIO() as buffer:
            image.save(buffer, format="JPEG")  # Ensure the image is converted to JPEG
            return base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    # Set the model paramters manually
    def set_model_params(self, settings):
            self.settings = settings
    # Returns the selected model
    def get_openai_model(self):
        return self.openai_model

    def getCompletion(self,message_history):
        print("Inside get completion")
        response = OpenAI().chat.completions.create(
            messages=message_history,
            **self.settings
        )
        return response.choices[0].message.content 
    
