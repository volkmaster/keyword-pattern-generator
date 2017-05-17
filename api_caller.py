from os.path import exists
from os import makedirs
import google_api
import twitter_api
import wikipedia_api


__author__ = 'Ziga Vucko'


def run(query):
    dirname = query.lower().replace(' ', '')

    root_dir = 'cache/' + dirname
    text_dir = root_dir + '/text'
    images_dir = root_dir + '/images'

    if not exists(root_dir):
        print('\t\tCreating the directories "' + text_dir + '" and "' + images_dir + '" and downloading the content')

        # Create the text and images directories for the given query.
        makedirs(text_dir)
        makedirs(images_dir)

        # Call APIs, download and save content to cache.
        google_api.run(query, images_dir)
        twitter_api.run(query, text_dir)
        wikipedia_api.run(query, text_dir)

    else:
        print('\t\tContent already exists in the directories "' + text_dir + '" and "' + images_dir + '" in cache')
