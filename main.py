import requests  # pip3 install requests
import config
import logging
import sys
import os
from datetime import datetime
from lib.vomsApi import vomsApi
from lib.comanageDbClient import comanageDbClient

def provision(dry_run):
    pathname = str(os.path.dirname(os.path.realpath(__file__)))
    logging.basicConfig(filename=pathname + '/log/voms-provision.log', level=logging.DEBUG,
                        filemode='a', format='%(asctime)s - %(message)s')

    values_list = []
    row_id = 1
    now = datetime.utcnow()
    dirac_res = requests.get('https://dirac.egi.eu/files/diracVOs.json')
    vos = dirac_res.json()
    for vo in vos:
        for voms in vo['VOMSServers']:
            voUsers = dict()
            vomsapi = vomsApi()
            voUsers = vomsapi.getUsers(voms['HostName'], '8443', vo['VOName'])
            if voUsers == None:
                continue
            for user in voUsers:
                for role in voUsers[user]['Roles']:
                    values = (row_id, user,
                            voUsers[user]['issuer'], reformateRoles(role), now)
                    row_id += 1
                    values_list.append(values)
            break

    if values_list != []:
        logging.debug(values_list)
        comanage = comanageDbClient()
        comanage.update_local_members(values_list)


def reformateRoles(role):
    newRole = role.replace('/', ':')
    newRole = newRole.replace(':Role=', ':role=')
    return newRole[1:]


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "-n":
        dry_run_flag = True
    else:
        dry_run_flag = False
    provision(dry_run_flag)
