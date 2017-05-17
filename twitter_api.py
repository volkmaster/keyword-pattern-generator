import twitter


__author__ = 'Ziga Vucko'


CONSUMER_KEY = 'xQjVGBByo6T7fFsLnxUPOTbWK'
CONSUMER_SECRET = '8OavKLFUtj5oUi0EHjo7atWXGWw1KVxiv9SQY0C0yxuPbfbuq4'
ACCESS_TOKEN_KEY = '1278654702-clvIrmYFcYEUMuOxBxgIVrhE9fkGHMJjzCxJUW5'
ACCESS_TOKEN_SECRET = 'AJigqXaFeXkHueHF92lrKreVU61rMmJ8dGoUyoYVxV6SQ'


def run(query, text_dir):
    # Run the query to the Twitter Search API.
    print('Calling the Twitter Search API, downloading statuses and saving them to cache')
    api = twitter.Api(consumer_key=CONSUMER_KEY,
                      consumer_secret=CONSUMER_SECRET,
                      access_token_key=ACCESS_TOKEN_KEY,
                      access_token_secret=ACCESS_TOKEN_SECRET)

    statuses = api.GetSearch(term=query, count=50, lang='en')
    text = '\n'.join([s.text for s in statuses])
    with open(text_dir + '/twitter.txt', 'w') as file:
        file.write(text)
