import twitter
import util
import settings


__author__ = 'Ziga Vucko'


def run(query, text_dir):
    # Run the query to the Twitter Search API.
    print(util.timestamp() + ' Calling the Twitter Search API, downloading statuses for the keyword "' + query +
          '" and saving them to cache')

    api = twitter.Api(consumer_key=settings.TWITTER_CONSUMER_KEY,
                      consumer_secret=settings.TWITTER_CONSUMER_SECRET,
                      access_token_key=settings.TWITTER_ACCESS_TOKEN_KEY,
                      access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET)

    statuses = api.GetSearch(term=query, count=50, lang='en')
    text = '\n'.join([s.text for s in statuses])
    with open(text_dir + '/twitter.txt', 'w', encoding="utf-8") as file:
        file.write(text)
