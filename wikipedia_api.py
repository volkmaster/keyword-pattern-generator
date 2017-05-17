import wikipedia


__author__ = 'Ziga Vucko'


def run(query, text_dir):
    # Run the query to the Wikipedia API.
    print('Calling the Wikipedia API, downloading the content of the given term and saving it to cache')
    page = wikipedia.page(query)
    with open(text_dir + '/wikipedia.txt', 'w') as file:
        file.write(page.content)
