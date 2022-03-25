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
    