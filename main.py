import os
import json
from ad import get_ou_members
from mailchimp import get_mailchimp_list_emails, update_mailchimp_list

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def get_properties(file):
    with open(os.path.join(__location__, file)) as json_file:
        properties = json.load(json_file)

    return properties


def update_lists():
    properties = get_properties('properties.json')

    for group, group_prop in properties['groups'].items():
        ad_list = get_ou_members(properties['global'], group_prop)
        mc_list = get_mailchimp_list_emails(group_prop)
        add_list = compare_lists(mc_list, ad_list)
        delete_list = compare_lists(ad_list, mc_list)
        update_mailchimp_list(group_prop, add_list, 'ADD')
        update_mailchimp_list(group_prop, delete_list, 'DELETE')

    return None


def compare_lists(base, new):
    """returns the elements in new that are not in base"""

    delta = []
    lower_base = [j.lower() for j in base]

    for member in new:
        if member.lower() not in lower_base:
            delta.append(member.lower())

    return delta


if __name__ == '__main__':
    result = update_lists()

    print(result)
