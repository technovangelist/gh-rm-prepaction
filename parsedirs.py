import os
import requests
import json

srcignorelist = os.environ["INPUT_IGNORELIST"]
ignorelist = [x.strip() for x in srcignorelist.split(',')
              if not srcignorelist == '']
docsdirectory = os.environ["INPUT_DOCSDIRECTORY"]
categoriesresponse = requests.get(
    'https://dash.readme.com/api/v1/categories?perPage=10&page=1', headers={'Authorization': 'Basic ' + os.environ["readmeapikey"]})
if categoriesresponse.status_code == 200:
    categories = categoriesresponse.json()

    # curl - -request GET \
    #      - -url 'https://dash.readme.com/api/v1/categories?perPage=10&page=1' \
    #      - -header 'Authorization: Basic R1ZUalN3bEp3RVRkbllWOEdtQ3F1YW00bGROV2FibUE6'
    for (dirpath, dirnames, filenames) in os.walk(docsdirectory):
        if not any(dirpath.startswith(docsdirectory + "/" + ignore) for ignore in ignorelist):
            for file in filenames:
                fullpath = os.path.join(dirpath, file).split('/')[1:]
                title = fullpath[-1]
                category = fullpath[0]
                categoryid = [x for x in categories if x["title"]
                              == category][0]["id"]
                categoryinfo = categories
                print('title = ' + title)
                print('category = ' + category)
                if len(fullpath) > 2:
                    parent = fullpath[-2]
                    if parent == title.replace('.md', ''):
                        parent = fullpath[-3]
                    if parent == category:
                        parent = ""
                    else:
                        print('parent = ' + parent)
                print('---')
