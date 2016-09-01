from ad import get_ou_members
from mailchimp import get_mailchimp_list_users, update_mailchimp_list
from properties import get_all_properties


def update_lists():
    properties = get_all_properties('properties.json')
    reponses = list()

    for group, group_prop in properties['groups'].items():
        ad_dict = get_ou_members(properties['global'], group_prop)
        mc_dict = get_mailchimp_list_users(group_prop)
        update_dict = get_updates(ad_dict, mc_dict)
        add_dict = compare_dicts(mc_dict, ad_dict)
        delete_dict = compare_dicts(ad_dict, mc_dict)
        update_mailchimp_list(group_prop, add_dict, 'ADD')
        update_mailchimp_list(group_prop, delete_dict, 'DELETE')
        reponses.append(update_mailchimp_list(group_prop, update_dict, 'UPDATE'))

    return reponses


def compare_dicts(base, new):
    """returns the elements in new that are not in base"""

    delta = {}
    lower_base = [j.lower() for j in base]

    for member, name in new.items():
        if member.lower() not in lower_base:
            delta.update({member.lower(): {'first_name': name['first_name'], 'last_name': name['last_name']}})

    return delta


def get_updates(base_dict, to_update_dict):
    update_dict = dict()
    lower_update_dict = dict((k.lower(), v) for k, v in to_update_dict.items())

    for person, name in base_dict.items():
        if (person.lower() in lower_update_dict
                and (name['first_name'] != lower_update_dict[person.lower()]['first_name']
                     or name['last_name'] != lower_update_dict[person.lower()]['last_name'])):
            update_dict.update({person: name})

    return update_dict


if __name__ == '__main__':
    result = update_lists()

    # properties = get_all_properties('properties.json')
    #
    # for group, group_prop in properties['groups'].items():
    #     ad_list = get_ou_members(properties['global'], group_prop)
    #     print(ad_list)
    #     mc_list = get_mailchimp_list_users(group_prop)
    #     print(mc_list)
    #     result = get_updates(ad_list, mc_list)

    print(result)
