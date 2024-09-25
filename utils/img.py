def get_content_from_images_with_gpt(wrapper, images):
        messages = ({'role':'system', 'content':"Return the content of the image."},
                    {'role':'user', 'content': [{"type": "text", "text":"Return the content of these images: "}]})

        for _, image in enumerate(images):
            base64_image = wrapper.encode_image_from_files(image)
            messages[-1]["content"].append({"type":"image_url", "image_url":{"url":f"data:image/jpeg;base64,{base64_image}"}})
        return wrapper.getCompletion(messages)