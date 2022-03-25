import os
from pydoc import doc
import requests
import json
import base64
from distutils.version import StrictVersion
from versions import ensureVersionExists

parentdocs = list()
rawreadmeapikey = os.environ["INPUT_READMEAPIKEY"]
versionnumber = os.environ["INPUT_VERSIONNUMBER"].replace("v", "")
srcignorelist = os.environ["INPUT_IGNORELIST"]
docsdirectory = os.environ["INPUT_DOCSDIRECTORY"]

versionurl = "https://dash.readme.com/api/v1/version"
docsurl = "https://dash.readme.com/api/v1/docs"

readmeapikey = base64.b64encode(
    rawreadmeapikey.encode('utf-8')).decode('utf-8')
# existingversions = requests.get(versionurl, headers={
#                                 'Authorization': 'Basic ' + readmeapikey, 'Accept': 'application/json'}).json()
# existingversions.sort(key=lambda x: StrictVersion(x['version']), reverse=True)
# if not [x for x in existingversions if x["version"]
#         == versionnumber]:
#     print("Creating a new version number.")
#     requests.post(versionurl, headers={
#         'Authorization': 'Basic ' + readmeapikey, 'Accept': 'application/json', 'Content-Type': 'application/json'}, json={"is_beta": True, "version": versionnumber, "from": existingversions[0]["version"], "is_stable": False, "is_hidden": False}).json()

ensureVersionExists(readmeapikey, versionnumber)
ignorelist = [x.strip() for x in srcignorelist.split(',')
              if not srcignorelist == '']
categoriesresponse = requests.get(
    'https://dash.readme.com/api/v1/categories?perPage=100&page=1', headers={'Authorization': 'Basic ' + readmeapikey, 'x-readme-version': versionnumber})
if categoriesresponse.status_code == 200:
    categories = categoriesresponse.json()

    # print("Categories: " + '\n'.join(map(str, categories)))
    allpaths = list()
    for (dirpath, dirnames, filenames) in os.walk(docsdirectory):
        if not any(dirpath.startswith(docsdirectory + "/" + ignore) for ignore in ignorelist):
            dirnames.sort()
            filenames.sort()
            for filename in filenames:
                path = os.path.join(dirpath, filename)
                allpaths.append(path)

allpaths.sort(reverse=True)
# print('\n'.join(map(str, allpaths)))
for path in allpaths:

    # for (dirpath, dirnames, filenames) in os.walk(docsdirectory):
    # dirnames.sort()
    # if not any(dirpath.startswith(docsdirectory + "/" + ignore) for ignore in ignorelist):
    # for file in filenames:
    # fullpath = os.path.join(dirpath, file).split('/')[1:]
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

    with open(path) as f:
        fulltext = f.read()
    fulltext = fulltext.split("\n")[1:]
    fulltext = '\n'.join(fulltext).strip()

    # print(fulltext)
    # get the document to see if it exists
    # create the document if it doesn't exist
    print("**** " + slug + " ****")
    print("Fulltext: " + fulltext)
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
    docExistHeaders = {
        'Authorization': 'Basic ' + readmeapikey, 'Accept': 'application/json', 'x-readme-version': versionnumber}
    print("docExistHeaders: " + str(docExistHeaders))
    docExistUrl = docsurl + "/" + slug
    print("docExistUrl: " + docExistUrl)
    documentExists = requests.get(docExistUrl, headers=docExistHeaders)
    print("Document Status Code: " +
          str(documentExists.status_code))

    # print("Document JSON: " + str(documentExists.json()))
    if documentExists.status_code != 200:
        print("DocumentExists: " + str(documentExists.json()))
        print("Creating document: " + slug +
              ", version: " + versionnumber)

        print("headers: " + json.dumps(headers))
        payload["slug"] = slug
        print("payload: " + json.dumps(payload))
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
