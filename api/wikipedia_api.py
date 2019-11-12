import wikipediaapi
import util


__author__ = 'Ziga Vucko'


def run(query, text_dir):
    # Run the query to the Wikipedia API.
    print(util.timestamp() + ' Calling the Wikipedia API, downloading the content for the keyword "' + query +
          '" and saving it to cache')

    wikipedia = wikipediaapi.Wikipedia('en')

    page = wikipedia.page(query.title())
    text = ''
    if not page.exists():
        print('Wikipedia page for keyword "' + query + '" does not exist. Creating an empty file')
    else:
        text = page.text

    with open(text_dir + '/wikipedia.txt', 'w', encoding="utf-8") as file:
        file.write(text)
