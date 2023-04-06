import time
import csv

import vk


def authorize_in_app(login: str, password: str):
    client_id = '51576983'  # App ID
    v = '5.131'  # API version
    api_session = vk.UserAPI(user_login=login, user_password=password, client_id=client_id, v=v)
    return api_session


def get_1000_users(api_session: vk.UserAPI, **params):
    """
    :type params: parameters of Vk API-method users.search, more information: https://dev.vk.com/method/users.search

    """
    offset = 0
    count = 200
    users = []
    while offset < 1000:
        response = api_session.users.search(offset=offset, count=count, **params)
        users.extend(response['items'])
        time.sleep(0.25)
        offset += 200
    return users


def save_results(users):
    columns = set(i for d in users for i in d)  # getting all key names from passed list of dicts "users"
    columns2 = []
    for d in users:
        for i in d:
            columns2.append(i)
    columns2 = set(columns2)

    with open('../vk_parser/out.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for row in users:
            writer.writerow(row)


if __name__ == '__main__':
    user_login = 'enter_login'  # change to access
    user_pass = 'enter_pass'   # change to access

    api = authorize_in_app(user_login, user_pass)

    fields = [
        'city',
        'photo_max_orig'
    ]

    results = get_1000_users(api, has_photo=1, fields=fields)
    save_results(results)
