import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from openai import OpenAI
from PIL import Image

# local_path = "models/SmolLM3-3B"
#
# tokenizer = AutoTokenizer.from_pretrained(local_path, local_files_only=True)
# model = AutoModelForCausalLM.from_pretrained(local_path, local_files_only=True)

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
        return self.make_request_to_gpt(instructions, words_comma_separated)

    def make_request_to_gpt(self, instructions: str, request_content: str, model: str = "gpt-5-nano") -> str:
        api_key = os.environ.get('OPENAI_API_KEY')
        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model=model,
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": instructions},
                        {"type": "input_text", "text": request_content},
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

    def generate_sentences(self, words: list[str]) -> list[str]:
        instructions = """
            Generate 8 sentences with the given words below. Each word should appear at least on time across the sentences.
            Make them simple, short (a few words) and return the output in this format - 
            sentence - translation to English{new_line}
            sentence - translation to English{new_line}
            ...
            
            The sentences must make sense, each one individually. 
            You may change the form of the words, use them in a different tense, and remove special characters, in order for the sentence to make sense.
            Return only the output and nothing else.
            The given words are - 
        """

        sentences = self.make_request_to_gpt(instructions, str(words), model="gpt-5-mini")
        sentences_split = sentences.split("\n")
        return sentences_split

    # def generate_sentence(self, words: list[str]) -> str:
    #     prompt = (
    #         "Write one complete, short, natural-sounding English sentence as written by a native speaker.\n"
    #         "You may add extra words if needed.\n"
    #         "Use each of the following words exactly once.\n"
    #         f"Words: {', '.join(words)}\n\n"
    #         "Sentence:*"
    #     )
    #
    #     inputs = tokenizer(prompt, return_tensors="pt")
    #
    #     outputs = model.generate(
    #         **inputs,
    #         max_new_tokens=40,
    #         temperature=0.7,
    #         do_sample=True,
    #         pad_token_id=tokenizer.eos_token_id
    #     )
    #
    #     decoded: str = tokenizer.decode(outputs[0], skip_special_tokens=True)
    #     output = decoded.split("*")[1]
    #     return outputs

    def generate_word_description(self, word_name: str):
        instructions = """
        Explain the following Russian word, it's usages and context in summary.
        Explain it in English.
        Return the response as markdown text that is UI friendly:
        """

        return self.make_request_to_gpt(instructions, word_name)

