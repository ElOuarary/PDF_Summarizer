from pdf_processor import PDFprocessor
from summarizer import Summarizer

processor = PDFprocessor()
summarizer = Summarizer()

text = processor.extract_text('.pdf')
summary = summarizer.summarize(text)
print(summary)