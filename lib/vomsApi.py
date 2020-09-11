import requests
import sys
import logging
import config


""" Get all the users of the VOMS VO with their detailed information

:return: user dictionary keyed by the user DN
"""

class vomsApi:

    def getUsers(self, hostname, port, vo_name):
        result = None
        url = "https://%s:%s/voms/%s/apiv2/users" % (hostname, port, vo_name)
        logging.debug("Processing '%s'" % (url))
        rawUserList = []
        startIndex = 0
        result = None
        error = None
        urlDone = False
        while not urlDone:
            try:
                result = requests.get(url,
                                    headers={"X-VOMS-CSRF-GUARD": "y"},
                                    cert=(config.voms['cert_path'], config.voms['key_path']),
                                    verify=config.voms['trusted_ca_path'],
                                    params={"startIndex": str(startIndex),
                                            "pageSize": "100"})
            except requests.ConnectionError as exc:
                error = "%s:%s" % (url, repr(exc))
                urlDone = True
                continue

            if result.status_code != 200:
                error = "Failed to contact the VOMS server: %s" % result.text
                urlDone = True
                continue

            userList = result.json()['result']
            rawUserList.extend(userList)
            if len(userList) < 100:
                urlDone = True
            startIndex += 100

        if error:
            logging.debug("Failed to contact the VOMS server: %s" % error)
            return None

        # We have got the user info, reformat it
        resultDict = {}
        for user in rawUserList:
            if user['suspended']:
                logging.debug("Ignoring suspended user: %s" % user)
                continue
            for cert in user['certificates']:
                dn = cert['subjectString']
                # resultDict[dn] = user
                resultDict[dn] = dict()
                resultDict[dn]['issuer'] = cert['issuerString']
                resultDict[dn]['Roles'] = user['fqans']
                attributes = user.get('attributes')
                if attributes:
                    for attribute in user.get('attributes', []):
                        if attribute.get('name') == 'nickname':
                            resultDict[dn]['nickname'] = attribute.get('value')

        return resultDict
