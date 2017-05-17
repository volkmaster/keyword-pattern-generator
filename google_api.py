from googleapiclient.discovery import build
import urllib.request
import urllib.error
import ssl
import util
import settings


__author__ = 'Ziga Vucko'


def search_images(service, query, size='xlarge', start=1):
    return service.cse().list(
        cx=settings.GOOGLE_SEARCH_ENGINE_ID,
        q=query,
        searchType='image',
        imgSize=size,
        start=start
    ).execute()


def run(query, images_dir):
    # Run the query to the Google Custom Search API.
    print(util.timestamp() + ' Calling the Google Custom Search API, downloading images and saving the content to cache')

    # Build a urllib opener to bypass website's blockade of the user-agent used by urllib.
    opener = urllib.request.build_opener()
    opener.addheaders = [
        ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/36.0.1941.0 '
                       'Safari/537.36')
    ]
    urllib.request.install_opener(opener)

    # Build a service object for interacting with the API.
    service = build('customsearch', 'v1', developerKey=settings.GOOGLE_API_KEY)

    # Call the API, parse the JSON response, download the images and cache them.
    for i in range(3):
        res = search_images(service, query, start=i*10+1)

        for item in res['items']:
            url = item['link']
            filename = item['link'].split('/')[-1]
            if filename.lower().endswith(('png', 'jpg', 'jpeg', 'tiff', 'gif', 'bmp')):
                try:
                    print(url)
                    urllib.request.urlretrieve(url, images_dir + '/' + filename)
                except (urllib.error.URLError, ssl.CertificateError):
                    pass

