import requests  # pip3 install requests
import config
import logging
import sys
from datetime import datetime
from lib.vomsApi import vomsApi
from lib.comanageDbClient import comanageDbClient


def provision(dry_run):
    logging.basicConfig(filename='diracProvision.log', level=logging.DEBUG,
                        filemode='w+', format='%(asctime)s - %(message)s')

    values_list = []
    row_id = 1
    now = datetime.utcnow()
    for voms in config.voms_config['vomses']:
        voUsers = dict()
        vomsapi = vomsApi()
        voUsers = vomsapi.getUsers(
            voms['hostname'], voms['port'], voms['vo_name'])
        for user in voUsers:
            for role in voUsers[user]['Roles']:
                values = (row_id, user,
                          voUsers[user]['issuer'], reformateRoles(role), now)
                row_id += 1
                values_list.append(values)

    print(values_list)
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
