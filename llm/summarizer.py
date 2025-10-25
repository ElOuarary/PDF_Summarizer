from dotenv import load_dotenv
from google import genai
import logging
import os
from pathlib import Path
from transformers import pipeline
import yaml


load_dotenv()


class Summarizer:
    def __init__(self, model):
        self.logger = logging.getLogger(__name__)
        try:
            with open('config/model_config.yaml', 'r') as f:
                config = yaml.safe_load(f)
        except:
            self.logger.error('Could not laod the configuration file of the model')
        self.model = model
        self.model_name = config[self.model]['name']
        self.min_page = config[self.model]['min_page']
        self.max_page = config[self.model]['max_page']
        if self.model == 'gemini':
            try:
                self.client = genai.Client(api_key=os.environ.get('GOOGLE_GEMINI_API'))
            except Exception as e:
                self.logger.error(f'Failed to connect to the GEMINI API, {e}')
                
        else:
            self.context_window = config[model]['context_window']
            self.summarization_min_length = config[model]['summarization']['min_length']
            self.summarization_max_length = config[model]['summarization']['max_length']
            try:
                self.summarizer = pipeline("summarization", model='facebook/bart-large-cnn', device=-1)
            except Exception as e:
                self.logger.warning(f'Failed to load the model {model}')
                self.summarizer = None
    
    
    def summarize_with_gemini(self, file_in_bytes):
        prompt = 'Summarize this document'
        sample_doc = self.client.files.upload(
            file=file_in_bytes,
            config=dict(
                mime_type='application/pdf'
            )
        )
        result = self.client.models.generate_content(
            model=self.model_name,
            contents=[sample_doc, prompt]
        )
        return result.text


    def summarize_with_local_model(self, text):
        if not self.summarizer:
            self.logger.warning(f'{self.model} was not loaded')
            return None
        try:
            result = self.summarizer(
                text
            )
            return result
        except Exception as e:
            self.logger.error(f'Summarization failed: {e}')
        return None
    
if __name__ == '__main__':
    pass