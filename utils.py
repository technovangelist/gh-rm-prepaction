import os
import base64
import requests


def getReadmeAPIKey():
    rawreadmeapikey = os.environ["INPUT_READMEAPIKEY"]

    readmeapikey = base64.b64encode(
        rawreadmeapikey.encode('utf-8')).decode('utf-8')

    return readmeapikey


def getIgnoreList():
    srcignorelist = os.environ["INPUT_IGNORELIST"]

    ignorelist = [x.strip() for x in srcignorelist.split(',')
                  if not srcignorelist == '']

    return ignorelist


def getCategories(readmeapikey, versionnumber):
    categoriesUrl = 'https://dash.readme.com/api/v1/categories?perPage=100&page=1'

    categoriesresponse = requests.get(
        categoriesUrl,
        headers={'Authorization': 'Basic ' + readmeapikey,
                 'x-readme-version': versionnumber})

    categories = categoriesresponse.json()

    return categories


def getAllDocumentPaths(source_directory, ignorelist):
    allpaths = list()

    for (dirpath, dirnames, filenames) in os.walk(source_directory):
        if not any(dirpath.startswith(source_directory + "/" + ignore) for ignore in ignorelist):
            dirnames.sort()
            filenames.sort()
            for filename in filenames:
                path = os.path.join(dirpath, filename)
                allpaths.append(path)

    allpaths.sort(reverse=True)

    return allpaths


def getFileFullText(path):
    with open(path) as f:
        fulltext = f.read()
    fulltext = fulltext.split("\n")[1:]
    fulltext = '\n'.join(fulltext).strip()

    return fulltext


def thisDocumentExists(readmeapikey, versionnumber, slug):
    docUrl = 'https://dash.readme.com/api/v1/docs/' + slug
    docresponse = requests.get(
        docUrl,
        headers={'Authorization': 'Basic ' + readmeapikey,
                 'Accept': 'application/json',
                 'x-readme-version': versionnumber})
    if docresponse.status_code == 200:
        return True
    else:
        return False
