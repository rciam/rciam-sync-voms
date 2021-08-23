import config
import requests
import logging
import sys
import os
from datetime import datetime
from lib.vomsApi import vomsApi
from lib.comanageDbClient import comanageDbClient

def syncVoms(dry_run):
    pathname = str(os.path.dirname(os.path.realpath(__file__)))
    loglevel = logging.getLevelName(config.logging['level'])
    logging.basicConfig(filename=pathname + '/log/main.log',
                        level=loglevel, filemode='a',
                        format='%(asctime)s - %(message)s')

    values_list = []
    row_id = 1
    now = datetime.utcnow()
    if 'ca_path' in config.voms['vomses_file']:
        vomses_verify = config.voms['vomses_file']['ca_path']
    else:
        vomses_verify = True
    vomses_res = requests.get(config.voms['vomses_file']['url'],
                              verify=vomses_verify)
    vos = vomses_res.json()
    for vo in vos:
        for voms in vo['VOMSServers']:
            voUsers = dict()
            vomsapi = vomsApi()
            voUsers = vomsapi.getUsers(voms['HostName'], voms['Port'],
                                       vo['VOName'])
            if voUsers == None:
                continue
            for user in voUsers:
                for role in voUsers[user]['Roles']:
                    values = (row_id, user, voUsers[user]['issuer'],
                              reformatRoles(role), now)
                    row_id += 1
                    values_list.append(values)
            break

    if values_list != []:
        logging.debug(values_list)
        comanage = comanageDbClient()
        comanage.update_local_members(values_list)


def reformatRoles(role):
    newRole = role.replace('/', ':')
    newRole = newRole.replace(':Role=', ':role=')
    return newRole[1:]


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "-n":
        dry_run_flag = True
    else:
        dry_run_flag = False
    syncVoms(dry_run_flag)
