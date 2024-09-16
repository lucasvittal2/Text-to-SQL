from openai import OpenAI
from services.config.config import Config
import logging

class TextGenerator:
    
        

    def generateText(prompt: str) -> str:
        raise NotImplemented("Method 'generateText' were not implemented !")
    
class OpenAITextGenerator(TextGenerator):

    def __init__(self) -> None:
        self.__getParams()
        self.client = OpenAI(api_key=self.OPENAI_KEY)
        

    def generateText(self, prompt: str) -> str:
        try:
            self.__getParams()
            response = self.client.chat.completions.create(
                model=self.LLM_MODEL,
                messages=[
                    {"role": "user", "content": prompt},
                ],
                temperature=self.LLM_TEMPERATURE,
            )
            generated_text = response.choices[0].message.content
            return generated_text
        except Exception as err:
            logging.error(f"Error in generating text with OpenAI {self.llm_model} model due to the following error: \n\n{err}\n\n")
            raise err
        
    def __getParams(self) -> None:
        config = Config()
        params = config.getConfig()
        self.OPENAI_KEY = params["OPENAI_KEY"]
        self.LLM_TEMPERATURE = params["LLM_TEMPERATURE"]
        self.LLM_MODEL = params["OPENAI_LLM_MODEL"]