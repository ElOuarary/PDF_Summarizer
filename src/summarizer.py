from transformers import pipeline

class Summarizer:
    def __init__(self, model=None):
        self.model = model
        self.summarizer = pipeline('summarization',  model='facebook/bart-large-cnn')
        
    def summarize(self, text):
        return self.summarizer(text)
    
