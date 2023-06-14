
from googletrans import Translator

translator = Translator()

def translate(text, src='auto', dest='ja') -> str:
  response = translator.translate(text, src=src, dest=dest)
  return response.text
