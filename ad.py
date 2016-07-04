from ldap3 import Server, Connection, NTLM, Tls
from ssl import PROTOCOL_TLSv1, CERT_REQUIRED
import json

BASE_OU = 'OU=Synlait,DC=Synlait,DC=local'

AD_SERVER = 'SMLDC1.Synlait.local'
USER = 'synlait\jmiddleton'
PASSWORD = 'RsiRsi06'
GROUP_OU = '(memberOf=CN=Synlait_Milk,OU=Email Groups,OU=Synlait,DC=Synlait,DC=local)'


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
    conn.search(global_prop['base_ou'], ad_query_string, attributes=['mail'])
    ad_emails = get_emails(conn.entries)

    return ad_emails


def get_emails(entries):
    json_entries = []
    for entry in entries:
        convert = json.loads(entry.entry_to_json())
        mail = convert['attributes'].get('mail', None)
        if mail:
            json_entries.append(mail[0])

    return json_entries


if __name__ == '__main__':
    result = get_ou_members()

    for i in result:
        print(i)

