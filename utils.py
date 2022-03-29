import os
import base64
import requests
import re


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


def thisDocumentAlreadyExists(readmeapikey, versionnumber, slug):
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


def getParentID(fullPathArray, filename, category, docsurl, versionnumber, readmeapikey, parentdocs):
    parent = ""
    parentid = ""

    if len(fullPathArray) > 3:
        parent = fullPathArray[-2]
        if parent == filename.replace('.md', ''):
            parent = fullPathArray[-3]
        if parent == category:

            parent = ""
        else:
            existingparentdocid = [
                doc for doc in parentdocs if doc[0] == parent]
            if len(existingparentdocid) == 0:
                parentresponse = requests.get(
                    docsurl + '/' + parent,
                    headers={'Authorization': 'Basic ' + readmeapikey, 'Accept': 'application/json',  'x-readme-version': versionnumber})

                try:
                    parentid = parentresponse.json()['id']
                except:
                    print("parent problem. parent=" + parent)
            else:
                parentid = existingparentdocid[0][1]
            # parentdocs.append((parent, parentid))

    return parent, parentid


def imageStringSwap(imagestring):
    filename = imagestring.split('/')[-1]
    # print("filename: " + filename)
    return "https://infrahq.sirv.com/docs/" + filename


def replaceURL(srcItem):
    fullurl = srcItem[0]
    alttext = srcItem[1]
    url = srcItem[2]
    optionalpart = srcItem[3]

    newurl = '[block:html]\n{"html": "<img class=\'Sirv\' data-src=\'' + \
        imageStringSwap(url) + '\' alt=\'' + alttext + '\'/>"}\n[/block]'
    # newurl = "!["+alttext+"]("+imageStringSwap(url) + optionalpart+")"
    print("newurl: " + newurl)
    return newurl


def replaceBlockQuote(srcitem):
    emoji = srcitem[2]
    callouttype = "info"
    if emoji == 'exclamation':
        callouttype = "danger"
    elif emoji == 'warning':
        callouttype = "warning"
    elif emoji == 'ok':
        callouttype = "success"
    message = srcitem[3]

    newBlock = '[block:callout]\n{"type": '+callouttype+', "body": ' + \
        message+'}\n[/block]'

    return newBlock


def ghToRmMDImages(inputtext):
    foundmatches = re.findall(
        r'(?P<fullimg>!\[(?P<alttext>.*?)\]\((?P<filename>.*?)(?=\"|\))(?P<optionalpart>\".*\")?\)?)', inputtext)

    outputtext = inputtext

    for item in foundmatches:
        fullurl = item[0]
        # print("fullurl: " + fullurl)
        # print("fullimg: " + item[0])

        newURL = replaceURL(item)
        outputtext = outputtext.replace(fullurl, newURL)
    return outputtext


def ghToRmBlockQuotes(inputtext):
    foundquotes = re.findall(
        r'^(?P<fullquote>>\s?(:(?P<emoji>\w+)?:)?\s?(?P<message>.*))', inputtext)
    outputtext = inputtext

    for item in foundquotes:
        oldblock = item[0]
        print(oldblock)
        newblock = replaceBlockQuote(item)
        print(newblock)
        outputtext = outputtext.replace(oldblock, newblock)
    return outputtext


def generateDocumentPayload(fullPathArray, categories, readmeapikey, versionnumber, parentdocs):
    # print("categories: " + str(categories))
    parentdocs = list()
    docsurl = "https://dash.readme.com/api/v1/docs"
    path = '/'.join(fullPathArray)
    filename = fullPathArray[-1]
    category = fullPathArray[1]
    # print("category: " + str(category))
    categoryid = [x for x in categories if x["title"] == category][0]["id"]

    with open(path) as f:
        filetitle = f.readline().rstrip().replace('# ', '')

    # titlestring = "title: " + filetitle + "\n"
    # print('title = ' + filetitle)
    # print('filename = ' + filename)
    # print('category = ' + category + ' (' + str(categoryid) + ')')
    # categorystring = "category: " + categoryid + "\n"
    # hiddenstring = "hidden: false\n"
    # parentdocstring = ""
    parent, parentid = getParentID(
        fullPathArray, filename, category, docsurl, versionnumber, readmeapikey, parentdocs)

    # print("FullpathLength: " + str(len(fullPathArray)))

    fulltext = getFileFullText(path)
    fulltext = ghToRmMDImages(fulltext)
    fulltext = ghToRmBlockQuotes(fulltext)

    payload = {
        "hidden": False,
        "type": "basic",
        "title": filetitle,
        "body": fulltext,
        "category": categoryid
    }
    if parentid is not "":
        payload["parentDoc"] = parentid

    return payload, parent, parentid
