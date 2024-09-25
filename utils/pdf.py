import fitz
from PIL import Image
import io
from utils import img as img_extractor

def extract_text_from_pdf(wrapper, pdf_path):
        text = ""
        images = []
        #doc = fitz.open(pdf_path)

        with fitz.open(pdf_path) as doc:
        
            for page_number in range(doc.page_count): 
                page=doc.load_page(page_number)
                text += page.get_text()
                image_list = page.get_images()
                #print(image_list)
    
            for _, img in enumerate(image_list,start=1):
                #print(image_index)
                xref = img[0] 
                # extract image bytes 
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]

                # Create a PIL Image object from the image bytes
                image = Image.open(io.BytesIO(image_bytes))
                images.append(image)

        # Apply OCR on images
        
        images_text = img_extractor.get_content_from_images_with_gpt(wrapper, images)
        
        return text+"\nText from images: "+images_text