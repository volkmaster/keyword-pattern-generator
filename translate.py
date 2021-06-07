import html
from google.cloud import translate_v2
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from collections import Counter
from num2words import num2words
import numpy as np

from api import api_caller
import pattern_generator
import util

nltk.data.path.append("./tmp")
nltk.download("stopwords", download_dir="./tmp")
nltk.download("punkt", download_dir="./tmp")

# Explicitly use service account credentials by specifying the private key file.
translate_client = translate_v2.Client.from_service_account_json('google_service_account.json')


def translate_text(target, text):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    import six
    from google.cloud import translate_v2 as translate

    # translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)
    result["translatedText"] = html.unescape(result["translatedText"])

    print(u"Text: {}".format(result["input"]))
    print(u"Translation: {}".format(result["translatedText"]))
    print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))

    return result["translatedText"]


def convert_lower_case(data):
    return np.char.lower(data)


def remove_stop_words(data):
    stop_words = stopwords.words('english')
    words = word_tokenize(str(data))
    new_text = ""
    for w in words:
        if w not in stop_words and len(w) > 1:
            new_text = new_text + " " + w
    return new_text


def remove_punctuation(data):
    symbols = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n"
    for i in range(len(symbols)):
        data = np.char.replace(data, symbols[i], ' ')
        data = np.char.replace(data, "  ", " ")
    data = np.char.replace(data, ',', '')
    return data


def remove_apostrophe(data):
    return np.char.replace(data, "'", "")


def stemming(data):
    stemmer = PorterStemmer()
    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        new_text = new_text + " " + stemmer.stem(w)
    return new_text


def convert_numbers(data):
    tokens = word_tokenize(str(data))
    new_text = ""
    for word in tokens:
        try:
            word = num2words(int(word))
        except:
            pass
        new_text = new_text + " " + word
    new_text = np.char.replace(new_text, "-", " ")
    return new_text


def preprocess(data):
    data = convert_lower_case(data)
    data = remove_punctuation(data)  # remove comma seperately
    data = remove_apostrophe(data)
    data = remove_stop_words(data)
    data = convert_numbers(data)
    # data = stemming(data)
    data = remove_punctuation(data)
    data = convert_numbers(data)
    # data = stemming(data)  # needed again as we need to stem the words
    data = remove_punctuation(data)  # needed again as num2word is giving few hypens and commas fourty-one
    data = remove_stop_words(data)  # needed again as num2word is giving stop words 101 - one hundred and one
    return data


text = "Dihurjevi so se borili rod za rodom z lakotno, rdečo zemljo, tešili njen glad z gnojem, parali ji nedrja, razbijali grude njenega čela, odpirali žile njenega osrčja in mašili žrela požiralnikov z odpadki, prhovino in kamenjem. Vse zastonj! -- Zemlja je ostala vedno enako nenasitna in požrešna, hlastno je goltala gnoj in ga brez sledu posrkavala kakor znoj njihovih rok in čel. Zdelo se je, da se njene lakotne ilovnate čeljusti požrešno stegajo po samem Dihurjevem rodu, srkajo za njegovim mozgom in za njegovo krvjo, zakaj rod za rodom je postajal bolj krmežljav. Polovico živeža, ki je obstajal iz ovsenega kruha in močnika, so dajali požiralniki, ostalo so morali Dihurji pridelati drugod ali pa pristradati. Zategadelj je bilo znano vsem gospodinjam po vsej soseski, da so Dihurji razvpiti rezači ogromnih kosov kruha in da ni priporočljivo, polagati pri malicah premalo načetih hlebov pred nje. In kakor nalašč je pri Dihurjevih neprestano tekla zibelka. Tudi zdaj je kričalo pri bajti pet malih Dihurjev, čeravno je bila mati Dihurka šele kakih deset let pri hiši. Neki Dihur je napravil zibanje na vodni pogon od studenca za plotom. Sosedje so trdili, da so bili vsi na ta način zibani Dihurji nekoliko zavaljani in da se jih ta lastnost še danes trdovratno drži. Ta čudežna naprava je še zdaj pod streho. Komaj so se mladi Dihurji dobro znebili plenic, so se že razpršili po svetu po raznih pastirskih službah. Po navadi so Dihurji napredovali do volarjev, Dihurke pa do kravaric, le redkokdaj se je pripetilo, da se je kak Dihur priženil na kako bajto ali Dihurka omožila na grunt. Vedelo se je le to, da so Dihurji v daljni žlahti z bogatim kmetom Košuto onstran gore, kjer je nekdaj gospodinjila Dihurjeva strina. Vendar se Košute niso brigali za to sorodstvo, narobe, celo sramovali so se ga. Dva Dihurjeva strica sta ostala pri rudarjih v Mežici. Nikoli nista prihajala domov, pri bajti pa je nastala legenda o njunem čarobnem, gosposkem življenju. Ko je imel sedanji Dihur deset let, ga je mati odvedla h kmetu Osojniku pod goro za pastirja. Vso pot mu je slikala izobilje, ki ga tam čaka, potice in pogače, da Dihurček pri slovesu niti solze ni potočil. Toda tam ga je čakalo trdo življenje. Sit je sicer bil, toda napori službe so presegali njegove moči. Čez dan je pasel petnajst glav govedi, zvečer po večerji in skoraj do polnoči pa vole, ki so čez dan delali pri ozimini in po deteljiščih. Zjutraj ob treh pa ga je veliki hlapec Matija že budil k mlačvi."
# translation = translate_text("en", text)
translation = "The ferrets fought generation after generation with the hungry, red earth, satisfying her hunger with manure, tearing her breasts, breaking the lumps of her forehead, opening the veins of her heart, and clogging the throats of her esophagus with debris, showers, and stones. Everything is free! - The earth has always remained equally insatiable and greedy, swallowing manure loudly and sucking it without a trace like the sweat of their hands and foreheads. Her hungry clayey jaws seemed to greedily stretch across the Ferret's genus itself, sucking for his brain and for his blood, for generation after generation was becoming more crunchy. Half of the food that existed from oat bread and potion was given by the esophagus, the rest the Ferrets had to grow elsewhere or starve. For this reason, it was known to all housewives throughout the neighborhood that the Ferrets were notorious cutters of huge chunks of bread, and that it was not advisable to lay under bread in front of her at snacks. And perfectly, the Cradle was constantly running at the Ferrets. Even now, five little Ferrets were screaming at the byte, even though Ferret's mother had only been at the house for about ten years. Some Ferret made a water-powered rocking from a well behind a fence. Neighbors claimed that all the Ferrets rocked in this way were a bit rolled up and that this trait still holds them stubbornly today. This miraculous device is still under the roof now. As soon as the young Ferrets got rid of their diapers well, they were already scattered around the world in various pastoral services. Usually, the Ferrets progressed to the oxen and the Ferrets to the cowherds, and it rarely happened that a Ferret married on a byte or a Ferret married on the ground. All that was known was that the Ferrets were in a distant nobility with the rich farmer Košuta on the other side of the mountain, where the Ferret's aunt used to be a housewife. However, Košute did not care about this kinship, wrongly, they were even ashamed of it. Dihur's two uncles stayed with the miners in Mežica. They never came home, and a legend about their magical, lordly life arose at the byte. When the present Ferret was ten years old, his mother took him to the farmer Osojnik under the mountain as a shepherd. All the way, she painted the abundance that awaits him there, potica and cakes, so that Dihurček did not shed a tear at the farewell. But there a hard life awaited him. He was fed up, but the efforts of the service exceeded his strength. During the day he grazed fifteen head of cattle, and in the evening after dinner and almost until midnight the oxen, who worked during the day in the winter and in the clover fields. At three in the morning, the big servant Matija had already woken him to the threshing floor."
print(translation)
data = preprocess(translation)
tokens = word_tokenize(data)
print(tokens)
most_frequent_words = list(dict(Counter(tokens)).keys())[:5]
print(most_frequent_words)

for keyword in most_frequent_words:
    api_caller.run(keyword)

pattern_generator.run(file='images/pattern.png', width=1000, height=1000, keywords=most_frequent_words, serial_number=3)

# api_caller
# load 10 images (from pixabay) for most frequent words
# load 10 tweets for most frequent words

# generate document
# apply filters (which ones?)
# save images to S3 (only final ones?)
# repeat 3 times

# return image urls in the response
