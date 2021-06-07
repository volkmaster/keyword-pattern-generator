from os.path import exists
from os import makedirs
from api import google_api, twitter_api, wikipedia_api
import util


__author__ = 'Ziga Vucko'


def run(query):
    """
    Create missing cache directories, call APIs, download and save content.
    """
    dir_name = query.lower().replace(' ', '')

    storage_dir = '/tmp'
    root_dir = storage_dir + '/cache/' + dir_name
    images_dir = root_dir + '/images'
    text_dir = root_dir + '/text'
    twitter_file = text_dir + '/twitter.txt'
    wikipedia_file = text_dir + '/wikipedia.txt'

    if exists(images_dir) and exists(twitter_file) and exists(wikipedia_file):
        print(util.timestamp() + ' Content already exists in the directories "' + text_dir + '" and "' + images_dir + '" in cache')
    else:
        if not exists(images_dir):
            print(util.timestamp() + ' Creating the directory "' + images_dir + '" and downloading the content')
            makedirs(images_dir)
            google_api.run(query, images_dir)

        if not exists(text_dir):
            print(util.timestamp() + ' Creating the directory "' + text_dir + '" and downloading the content')
            makedirs(text_dir)

        if not exists(twitter_file):
            twitter_api.run(query, text_dir)

        if not exists(wikipedia_file):
            wikipedia_api.run(query, text_dir)
