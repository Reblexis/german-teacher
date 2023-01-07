import googletrans


text1 = "Hoffnung"
text2 = "world"

translator = googletrans.Translator()
print(translator.detect(text1))
# get meaning of text1
translation = translator.translate(text1, src='de', dest="en")
print(translation.text)
extra_data = translation.extra_data
print(extra_data)

print(extra_data['all-translations'][0][1])

