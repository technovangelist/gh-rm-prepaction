import os
import requests
import json

parentdocs = list()
srcignorelist = os.environ["INPUT_IGNORELIST"]
ignorelist = [x.strip() for x in srcignorelist.split(',')
              if not srcignorelist == '']
docsdirectory = os.environ["INPUT_DOCSDIRECTORY"]
categoriesresponse = requests.get(
    'https://dash.readme.com/api/v1/categories?perPage=10&page=1', headers={'Authorization': 'Basic ' + os.environ["readmeapikey"]})
if categoriesresponse.status_code == 200:
    categories = categoriesresponse.json()

    for (dirpath, dirnames, filenames) in os.walk(docsdirectory):
        if not any(dirpath.startswith(docsdirectory + "/" + ignore) for ignore in ignorelist):
            for file in filenames:
                fullpath = os.path.join(dirpath, file).split('/')[1:]
                filename = fullpath[-1]
                category = fullpath[0]
                categoryid = [x for x in categories if x["title"]
                              == category][0]["id"]
                categoryinfo = categories
                with open(os.path.join(dirpath, file)) as f:
                    filetitle = f.readline().rstrip()
                print('title = ' + filetitle)
                print('filename = ' + filename)
                print('category = ' + category + ' (' + str(categoryid) + ')')
                if len(fullpath) > 2:
                    parent = fullpath[-2]
                    if parent == filename.replace('.md', ''):
                        parent = fullpath[-3]
                    if parent == category:
                        parent = ""
                    else:
                        existingparentdocid = [
                            doc for doc in parentdocs if doc[0] == parent]
                        if len(existingparentdocid) == 0:
                            print("searching for parent id")
                            parentresponse = requests.get(
                                'https://dash.readme.com/api/v1/docs/'+parent, headers={'Authorization': 'Basic ' + os.environ["readmeapikey"], 'Accept': 'application/json'})
                            parentid = parentresponse.json()['id']
                        else:
                            parentid = existingparentdocid[0][1]
                        parentdocs.append((parent, parentid))
                        print('parent = ' + parent +
                              ' (' + str(parentid) + ')')
                print('---')
