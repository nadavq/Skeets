import os
from openai import OpenAI


class AiService:

    def create_set_from_image(self, image_url) -> str:
        instructions = """Extract the russian words from this image, and translate them to English. 
                            Return the response in a structure of -
                            word,translate{new_line}
                            word,translate{new_line}
                            ...
                            
                            Return only the response itself and no other words.
        """
        api_key = os.environ.get('OPENAI_API_KEY')
        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model="gpt-5-nano",
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": instructions},
                        {"type": "input_image", "image_url": image_url},
                    ],
                }
            ],
        )

        return response.output_text
