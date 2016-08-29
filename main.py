from ad import get_ou_members
from mailchimp import get_mailchimp_list_users, update_mailchimp_list
from properties import get_all_properties


def update_lists():
    properties = get_all_properties('properties.json')

    for group, group_prop in properties['groups'].items():
        ad_list = get_ou_members(properties['global'], group_prop)
        mc_list = get_mailchimp_list_users(group_prop)
        ad_email = [i['email'] for i in ad_list]
        mc_email = [i['email'] for i in mc_list]
        add_list = compare_lists(mc_email, ad_email)
        delete_list = compare_lists(ad_email, mc_email)
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


def get_updates(ad_list, mc_list):
    pass


if __name__ == '__main__':
    result = update_lists()

    print(result)
