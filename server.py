#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import makedirs
from os.path import exists
import html
import numpy as np
from google.cloud import translate_v2
import six
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from collections import Counter
from num2words import num2words

from api import api_caller
from filtering import elastic_transform, pixelsort, segmentation
import pattern_generator
import util


__author__ = 'Ziga Vucko'


LAMBDA_DIR = "tmp"

nltk.data.path.append(LAMBDA_DIR)
nltk.download("stopwords", download_dir=LAMBDA_DIR)
nltk.download("punkt", download_dir=LAMBDA_DIR)

# Explicitly use service account credentials by specifying the private key file.
translate_client = translate_v2.Client.from_service_account_json("google_service_account.json")


def translate_text(target, text):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
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
    stop_words = stopwords.words("english")
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


def main():
    text = "Dihurjevi so se borili rod za rodom z lakotno, rdečo zemljo, tešili njen glad z gnojem, parali ji nedrja, razbijali grude njenega čela, odpirali žile njenega osrčja in mašili žrela požiralnikov z odpadki, prhovino in kamenjem. Vse zastonj! -- Zemlja je ostala vedno enako nenasitna in požrešna, hlastno je goltala gnoj in ga brez sledu posrkavala kakor znoj njihovih rok in čel. Zdelo se je, da se njene lakotne ilovnate čeljusti požrešno stegajo po samem Dihurjevem rodu, srkajo za njegovim mozgom in za njegovo krvjo, zakaj rod za rodom je postajal bolj krmežljav. Polovico živeža, ki je obstajal iz ovsenega kruha in močnika, so dajali požiralniki, ostalo so morali Dihurji pridelati drugod ali pa pristradati. Zategadelj je bilo znano vsem gospodinjam po vsej soseski, da so Dihurji razvpiti rezači ogromnih kosov kruha in da ni priporočljivo, polagati pri malicah premalo načetih hlebov pred nje. In kakor nalašč je pri Dihurjevih neprestano tekla zibelka. Tudi zdaj je kričalo pri bajti pet malih Dihurjev, čeravno je bila mati Dihurka šele kakih deset let pri hiši. Neki Dihur je napravil zibanje na vodni pogon od studenca za plotom. Sosedje so trdili, da so bili vsi na ta način zibani Dihurji nekoliko zavaljani in da se jih ta lastnost še danes trdovratno drži. Ta čudežna naprava je še zdaj pod streho. Komaj so se mladi Dihurji dobro znebili plenic, so se že razpršili po svetu po raznih pastirskih službah. Po navadi so Dihurji napredovali do volarjev, Dihurke pa do kravaric, le redkokdaj se je pripetilo, da se je kak Dihur priženil na kako bajto ali Dihurka omožila na grunt. Vedelo se je le to, da so Dihurji v daljni žlahti z bogatim kmetom Košuto onstran gore, kjer je nekdaj gospodinjila Dihurjeva strina. Vendar se Košute niso brigali za to sorodstvo, narobe, celo sramovali so se ga. Dva Dihurjeva strica sta ostala pri rudarjih v Mežici. Nikoli nista prihajala domov, pri bajti pa je nastala legenda o njunem čarobnem, gosposkem življenju. Ko je imel sedanji Dihur deset let, ga je mati odvedla h kmetu Osojniku pod goro za pastirja. Vso pot mu je slikala izobilje, ki ga tam čaka, potice in pogače, da Dihurček pri slovesu niti solze ni potočil. Toda tam ga je čakalo trdo življenje. Sit je sicer bil, toda napori službe so presegali njegove moči. Čez dan je pasel petnajst glav govedi, zvečer po večerji in skoraj do polnoči pa vole, ki so čez dan delali pri ozimini in po deteljiščih. Zjutraj ob treh pa ga je veliki hlapec Matija že budil k mlačvi."
    # translation = translate_text("en", text)
    # translation = "The ferrets fought generation after generation with the hungry, red earth, satisfying her hunger with manure, tearing her breasts, breaking the lumps of her forehead, opening the veins of her heart, and clogging the throats of her esophagus with debris, showers, and stones. Everything is free! - The earth has always remained equally insatiable and greedy, swallowing manure loudly and sucking it without a trace like the sweat of their hands and foreheads. Her hungry clayey jaws seemed to greedily stretch across the Ferret's genus itself, sucking for his brain and for his blood, for generation after generation was becoming more crunchy. Half of the food that existed from oat bread and potion was given by the esophagus, the rest the Ferrets had to grow elsewhere or starve. For this reason, it was known to all housewives throughout the neighborhood that the Ferrets were notorious cutters of huge chunks of bread, and that it was not advisable to lay under bread in front of her at snacks. And perfectly, the Cradle was constantly running at the Ferrets. Even now, five little Ferrets were screaming at the byte, even though Ferret's mother had only been at the house for about ten years. Some Ferret made a water-powered rocking from a well behind a fence. Neighbors claimed that all the Ferrets rocked in this way were a bit rolled up and that this trait still holds them stubbornly today. This miraculous device is still under the roof now. As soon as the young Ferrets got rid of their diapers well, they were already scattered around the world in various pastoral services. Usually, the Ferrets progressed to the oxen and the Ferrets to the cowherds, and it rarely happened that a Ferret married on a byte or a Ferret married on the ground. All that was known was that the Ferrets were in a distant nobility with the rich farmer Košuta on the other side of the mountain, where the Ferret's aunt used to be a housewife. However, Košute did not care about this kinship, wrongly, they were even ashamed of it. Dihur's two uncles stayed with the miners in Mežica. They never came home, and a legend about their magical, lordly life arose at the byte. When the present Ferret was ten years old, his mother took him to the farmer Osojnik under the mountain as a shepherd. All the way, she painted the abundance that awaits him there, potica and cakes, so that Dihurček did not shed a tear at the farewell. But there a hard life awaited him. He was fed up, but the efforts of the service exceeded his strength. During the day he grazed fifteen head of cattle, and in the evening after dinner and almost until midnight the oxen, who worked during the day in the winter and in the clover fields. At three in the morning, the big servant Matija had already woken him to the threshing floor."
    translation = """
She wanted rainbow hair. That's what she told the hairdresser. It should be deep rainbow colors, too. She wasn't interested in pastel rainbow hair. She wanted it deep and vibrant so there was no doubt that she had done this on purpose.
He walked down the steps from the train station in a bit of a hurry knowing the secrets in the briefcase must be secured as quickly as possible. Bounding down the steps, he heard something behind him and quickly turned in a panic. There was nobody there but a pair of old worn-out shoes were placed neatly on the steps he had just come down. Had he past them without seeing them? It didn't seem possible. He was about to turn and be on his way when a deep chill filled his body.
There are only three ways to make this work. The first is to let me take care of everything. The second is for you to take care of everything. The third is to split everything 50 / 50. I think the last option is the most preferable, but I'm certain it'll also mean the end of our marriage.
The headphones were on. They had been utilized on purpose. She could hear her mom yelling in the background, but couldn't make out exactly what the yelling was about. That was exactly why she had put them on. She knew her mom would enter her room at any minute, and she could pretend that she hadn't heard any of the previous yelling.
It seemed like it should have been so simple. There was nothing inherently difficult with getting the project done. It was simple and straightforward enough that even a child should have been able to complete it on time, but that wasn't the case. The deadline had arrived and the project remained unfinished.
"""
    print(translation)
    data = preprocess(translation)
    tokens = word_tokenize(data)
    most_frequent_words = list(dict(Counter(tokens)).keys())[:5]
    print(f"{util.timestamp()} Most frequent words in the text: {most_frequent_words}")

    # load 10 images (from pixabay) for most frequent words
    # load 10 tweets for most frequent words
    # load wikipedia text for most frequent words (?)
    for keyword in most_frequent_words:
        api_caller.run(keyword)

    generated_images_dir = f"{LAMBDA_DIR}/generated"
    file = f"{generated_images_dir}/pattern.png"
    if not exists(generated_images_dir):
        print(f"{util.timestamp()} Creating the directory '{generated_images_dir}'")
        makedirs(generated_images_dir)

    # load serial number from db (remove entirely?)
    with open("serial_number.txt", "r") as f_in:
        serial_number = int(f_in.read())

    # generate base document
    pattern_generator.run(file, width=1200, height=600, keywords=most_frequent_words, serial_number=serial_number)

    # apply filters
    file = elastic_transform.run(file, alpha=60000, sigma=8)
    file = pixelsort.run(file, sorting_path='vertical')
    file = segmentation.run(file, weight=10)  # weight=25 ... too strong?
    # add one more filter

    print(f"{util.timestamp()} Pattern with serial number #{str(serial_number)} successfully generated.")
    print("\t\tFilters applied: Elastic transform (liquify), Pixel sorting (vertical), Segmentation")

    # save images to S3 (only final carpet ones?)
    # repeat base document generation and filter application 3 times

    # save serial number to db (remove entirely?)
    with open("serial_number.txt", "w") as f_out:
        serial_number += 1
        f_out.write(str(serial_number))

    # return image S3 urls in the response


if __name__ == "__main__":
    main()
