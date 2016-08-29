import requests
from requests.auth import HTTPBasicAuth
import json
from hashlib import md5
import pprint
from properties import get_all_properties

HEADERS = {'Content-Type': 'application/json'}
MEMBERS_ENDPOINT = 'lists/{list_id}/members'
RETURN_FIELDS = 'members.email_address,members.merge_fields'
PARAMS = {'fields': RETURN_FIELDS,
          'count': 5000
}


def get_mailchimp_list_users(properties):
    auth = HTTPBasicAuth(properties['username'], properties['api_key'])
    url = properties['base_url'] + MEMBERS_ENDPOINT.format(list_id=properties['list_id'])
    resp = requests.get(url, auth=auth, headers=HEADERS, params=PARAMS)

    return get_users(resp.json())


def update_mailchimp_list(properties, members, opertation):
    auth = HTTPBasicAuth(properties['username'], properties['api_key'])
    url = properties['base_url'] + MEMBERS_ENDPOINT.format(list_id=properties['list_id'])
    results = []
    for member in members:
        resp = None
        if opertation == 'ADD':
            body = json.dumps({'status': 'subscribed', 'email_address': member})
            resp = requests.post(url, auth=auth, headers=HEADERS, data=body)
        elif opertation == 'DELETE':
            member_hash = md5()
            member_hash.update(member.encode())
            member_url = url + '/' + str(member_hash.hexdigest())
            resp = requests.delete(member_url, auth=auth, headers=HEADERS)

        results.append(resp.status_code if resp else None)

    return results


def get_users(get_response):
    members = get_response['members']
    users = []
    for i in members:
        user = {
            'email': i['email_address'],
            'first_name': i['merge_fields']['FNAME'],
            'last_name': i['merge_fields']['LNAME']
        }
        users.append(user)

    return users


def main():
    # results = update_mailchimp_list(URL_BASE + MEMBERS_ENDPOINT,
    #                                 ['jesse.middleton@synlait.com',
    #                                     'george.mcewan@synlait.com',
    #                                     'buckleigh.johns@synlait.com'],
    #                                    'DELETE')
    results = get_mailchimp_list_users(get_all_properties('properties.json')['groups']['synlait_milk'])
    re = [i['email'] for i in results]

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(re)


if __name__ == '__main__':
    main()
