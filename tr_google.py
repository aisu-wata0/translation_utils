
from googletrans import Translator

translator = Translator()

def translate(text, src='en', dest='ja') -> str:
  response = translator.translate(text, src=src, dest=dest)
  return response.text
