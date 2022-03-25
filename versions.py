from webbrowser import get
import requests
from distutils.version import StrictVersion


def ensureVersionExists(readmeapikey, versionnumber):
    versionurl = "https://dash.readme.com/api/v1/version"

    getVersionsHeader = {
        'Authorization': 'Basic ' + readmeapikey,
        'Accept': 'application/json'
    }

    allVersions = requests.get(versionurl, headers=getVersionsHeader).json()
    allVersions.sort(
        key=lambda x: StrictVersion(x['version']), reverse=True)

    if not [x for x in allVersions if x["version"]
            == versionnumber]:
        print("Creating a new version number.")

        createVersionHeader = {
            'Authorization': 'Basic ' + readmeapikey,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        createVersionPayload = {
            "is_beta": True,
            "version": versionnumber,
            "from": allVersions[0]["version"],
            "is_stable": False,
            "is_hidden": False
        }

        requests.post(versionurl,
                      headers=createVersionHeader,
                      json=createVersionPayload).json()
