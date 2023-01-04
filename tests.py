import googletrans


text1 = "Gut"
text2 = "world"

translator = googletrans.Translator()
print(translator.detect(text1))
# get meaning of text1
translation = translator.translate(text1, src='de', dest="en")
print(translation.text)
meaning1 = translation.extra_data
print(meaning1)

