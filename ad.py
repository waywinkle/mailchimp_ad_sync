from ldap3 import Server, Connection, NTLM, Tls
from ssl import PROTOCOL_TLSv1, CERT_REQUIRED
import json
from properties import get_all_properties

PROPERTIES = get_all_properties('properties.json')


def get_ou_members(global_prop, list_prop):
    ad_query_string = '''(&
                        (objectCategory=user)
                        {ou}
                        )
    '''.format(ou=list_prop['group_ou'])

    tls_configuration = Tls(validate=CERT_REQUIRED, version=PROTOCOL_TLSv1)
    server = Server(global_prop['ad_server'], use_ssl=True, tls=tls_configuration)
    conn = Connection(server,
                      user=global_prop['ad_user'],
                      password=global_prop['ad_password'],
                      authentication=NTLM,
                      auto_bind=True)
    conn.search(global_prop['base_ou'], ad_query_string, attributes=['mail', 'givenname', 'sn'])
    ad_users = get_users(conn.entries)

    return ad_users


def get_users(entries):
    json_entries = {}
    log = []
    for entry in entries:
        convert = json.loads(entry.entry_to_json())
        mail = convert['attributes'].get('mail', None)
        first_name = convert['attributes'].get('givenName', None)
        last_name = convert['attributes'].get('sn', None)

        if mail and first_name and last_name:
            json_entries.update({
                mail[0]: {
                    'first_name': first_name[0],
                    'last_name': last_name[0]
                }
            })
        elif mail:
            log.append(mail[0])
        elif first_name and last_name:
            log.append(first_name[0] + ' ' + last_name[0])
        elif first_name:
            log.append(first_name[0])
        else:
            log.append(entry)

    return json_entries


if __name__ == '__main__':
    result = get_ou_members(PROPERTIES['global'], PROPERTIES['groups']['synlait_milk'])

    for i, j in result.items():
        print(i, j)

