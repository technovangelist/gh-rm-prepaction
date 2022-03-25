from versions import ensureVersionExists
import os
from pydoc import doc
import requests
import json
import base64
from distutils.version import StrictVersion
from utils import getReadmeAPIKey, getIgnoreList, getCategories, getAllDocumentPaths, getFileFullText, thisDocumentExists

parentdocs = list()
allpaths = list()

versionnumber = os.environ["INPUT_VERSIONNUMBER"].replace("v", "")
docsdirectory = os.environ["INPUT_DOCSDIRECTORY"]

docsurl = "https://dash.readme.com/api/v1/docs"

readmeapikey = getReadmeAPIKey()
ignorelist = getIgnoreList()
categories = getCategories(readmeapikey, versionnumber)

ensureVersionExists(readmeapikey, versionnumber)

allpaths = getAllDocumentPaths(docsdirectory, ignorelist)

# print('\n'.join(map(str, allpaths)))
for path in allpaths:
    print("Working on: " + path)
    fullpath = path.split('/')

    filename = fullpath[-1]
    slug = filename.replace('.md', '')
    category = fullpath[1]
    print("Category: " + category)
    categoryid = [x for x in categories if x["title"]
                  == category][0]["id"]
    categoryinfo = categories
    with open(path) as f:
        filetitle = f.readline().rstrip().replace('# ', '')

    titlestring = "title: " + filetitle + "\n"
    # print('title = ' + filetitle)
    # print('filename = ' + filename)
    # print('category = ' + category + ' (' + str(categoryid) + ')')
    categorystring = "category: " + categoryid + "\n"
    hiddenstring = "hidden: false\n"
    parentdocstring = ""
    parentid = ""
    print("FullpathLength: " + str(len(fullpath)))
    if len(fullpath) > 3:
        parent = fullpath[-2]
        if parent == filename.replace('.md', ''):
            parent = fullpath[-3]
        if parent == category:

            parent = ""
        else:
            existingparentdocid = [
                doc for doc in parentdocs if doc[0] == parent]
            if len(existingparentdocid) == 0:
                # print("searching for parent id")

                parentresponse = requests.get(
                    docsurl + '/' + parent,
                    headers={'Authorization': 'Basic ' + readmeapikey, 'Accept': 'application/json',  'x-readme-version': versionnumber})

                try:
                    parentid = parentresponse.json()['id']
                except:
                    print("parent problem. parent=" + parent)
            else:
                parentid = existingparentdocid[0][1]
            parentdocs.append((parent, parentid))
            # print('parent = ' + parent +
            #       ' (' + str(parentid) + ')')
            parentdocstring = "parentDoc: " + str(parentid) + "\n"

    fulltext = getFileFullText(path)

    payload = {
        "hidden": False,
        "type": "basic",
        "title": filetitle,
        "body": fulltext,
        # "body": "test text",
        "category": categoryid
    }
    if parentid is not "":
        payload["parentDoc"] = parentid

    headers = {
        "Accept": "application/json",
        "x-readme-version": versionnumber,
        "Content-Type": "application/json",
        "Authorization": "Basic " + readmeapikey
    }

    if not thisDocumentExists(readmeapikey, versionnumber, slug):
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
# this was updating the document but i won't need this if i am posting them myself
# with open(os.path.join(dirpath, file), "r+") as f:
#     lines = f.readlines()
#     f.seek(0)
#     f.truncate()
#     f.write(frontmatterstring)
#     f.writelines(lines[1:])
