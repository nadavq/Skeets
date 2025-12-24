import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from openai import OpenAI
from PIL import Image

load_dotenv()


class AiService:

    def __init__(self, db):
        api_key = os.environ.get("GEMINI_API_KEY")
        self.client = genai.Client(api_key=api_key)

    def create_set_from_image(self, image_url) -> str:
        instructions = """Extract the russian words from this image, and translate them to English. 
                            This is for users learning Russian, so try to isolate the words that can help
                            him to understand the language better. Convert required words to the infinitive form, for instance,
                            улыбнулась -> улыбаться, so it would appear in the infinitive form of the word.
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

    def translate_words(self, words_comma_separated: str):
        instructions = """
                Translate these words into English. 
                This is for users learning Russian, so try to isolate the words that can help
                him to understand the language better. 
                Convert required words to the infinitive form, for instance,
                улыбнулась -> улыбаться, so it would appear in the infinitive form of the word.
                Translate each word individually, and return the response in the structure of -
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
                        {"type": "input_text", "text": words_comma_separated},
                    ],
                }
            ],
        )

        return response.output_text

    def create_asset_from_word(self, word_for_img) -> bytes | None:
        prompt = (
            f"Create an image that best represents the following word or phrase: "
            f"{word_for_img}. The image must have a transparent background."
        )

        # 1. Get the directory where THIS script is located
        base_dir = Path(__file__).resolve().parent

        # 2. Join it with the relative path to your asset
        # This moves up one level (..), then into assets
        image_path = base_dir / ".." / "assets" / "icon_reference.jpeg"

        # 3. Open the image
        image = Image.open(image_path)
        # image = Image.open("/Users/nadavholtzman/PycharmProjects/Skeets/assets/icon_reference.jpeg")

        response = self.client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=[prompt, image],
        )

        for part in response.parts:
            if part.text is not None:
                print(part.text)
            elif part.inline_data is not None:
                image = part.as_image()
                return image.image_bytes

        return None
