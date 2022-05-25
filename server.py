from googletrans import Translator
translator = Translator()
result = translator.translate('Hello', dest='bg', src='en')
print(result)
