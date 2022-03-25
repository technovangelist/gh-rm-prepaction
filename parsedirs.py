from versions import ensureVersionExists
import os
from pydoc import doc
import requests
import json
import base64
from distutils.version import StrictVersion
from utils import getReadmeAPIKey, getIgnoreList, getCategories, getAllDocumentPaths, thisDocumentAlreadyExists, generateDocumentPayload

parentdocs = list()
allpaths = list()

versionnumber = os.environ["INPUT_VERSIONNUMBER"].replace("v", "")
docsdirectory = os.environ["INPUT_DOCSDIRECTORY"]

docsurl = "https://dash.readme.com/api/v1/docs"

readmeapikey = getReadmeAPIKey()
ignorelist = getIgnoreList()

ensureVersionExists(readmeapikey, versionnumber)
categories = getCategories(readmeapikey, versionnumber)

allpaths = getAllDocumentPaths(docsdirectory, ignorelist)

# print('\n'.join(map(str, allpaths)))
for path in allpaths:
    fullpath = path.split('/')
    filename = fullpath[-1]
    slug = filename.replace('.md', '')

  # start genearte doc payload

    payload, parent, parentid = generateDocumentPayload(
        fullpath, categories, readmeapikey, versionnumber, parentdocs)
    parentdocs.append((parent, parentid))

    headers = {
        "Accept": "application/json",
        "x-readme-version": versionnumber,
        "Content-Type": "application/json",
        "Authorization": "Basic " + readmeapikey
    }

    if not thisDocumentAlreadyExists(readmeapikey, versionnumber, slug):
        payload["slug"] = slug
        response = requests.request(
            "POST", docsurl, json=payload, headers=headers)

        print(response)
        # update the document if it does exist
    else:
        print("Updating document: " + slug +
              ", versionnumber: " + versionnumber)

        response = requests.request(
            "PUT", docsurl + '/' + slug, json=payload, headers=headers)
        print(response)
