import wikipediaapi
import util


__author__ = 'Ziga Vucko'


def run(query, text_dir):
    # Run the query to the Wikipedia API.
    print(util.timestamp() + ' Calling the Wikipedia API, downloading the content of the given term and saving it to cache')

    wikipedia = wikipediaapi.Wikipedia('en')

    page = wikipedia.page(query)
    if not page.exists():
        raise util.Error('Wikipedia page for keyword "' + query + '" does not exist.')

    with open(text_dir + '/wikipedia.txt', 'w') as file:
        file.write(page.text)
