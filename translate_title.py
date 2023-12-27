from translate import Translator


def translate(text):
    translator = Translator(from_lang="ru", to_lang="en")
    translation = translator.translate(text)
    return translation


# print(translate("Магическая битва 2 сезон"))
l = [i for i in range(1, 6)]
d = {}
