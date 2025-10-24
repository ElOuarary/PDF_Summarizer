import logging
from transformers import pipeline
import yaml

class Summarizer:
    def __init__(self, model):
        self.logger = logging.getLogger(__name__)
        try:
            with open('config/model_config.yaml', 'r') as f:
                config = yaml.safe_load(f)
        except:
            self.logger.error('Could not laod the configuration file of the model')
            self.model = model
        self.model_name = config[model].name
        self.context_window = config[model].context_window
        self.max_tokens = config[model].max_tokens
        self.summarization_min_length = config[model].summarization.min_length
        self.summarization_max_length = config[model].summarization.max_length
        try:
            self.summarizer = pipeline("summarization", model=self.model_name, device=-1)
        except Exception as e:
            self.logger.warning(f'Failed to load the model {model}')
            self.summarizer = None


def summarize(self, text):
    if not self.summarizer:
        self.logger.warning(f'{self.model} was not loaded')
        return None
    try:
        if len(text) <= 1024:
            result = self.summarizer(
                text    
            )
            return result
    except Exception as e:
        self.logger.error(f'Summarization failed: {e}')
        return None
    
if __name__ == '__main__':
    pass