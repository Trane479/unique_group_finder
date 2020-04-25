from pprint import pprint
from urllib.parse import urlencode
import requests
from config import TOKEN
import time
import json


class User:
    def __init__(self, token, char_id):
        self.token = token
        self.char_id = char_id
        self.user_info = self.get_id()
        self.user_name = self.user_info['response'][0]['first_name']
        self.user_last_name = self.user_info['response'][0]['last_name']
        self.user_id = self.user_info['response'][0]['id']

    def get_id(self):
        response = requests.get('https://api.vk.com/method/users.get',
                                params={
                                    'access_token': self.token,
                                    'user_ids': self.char_id,
                                    'v': '5.89'

                                })
        json_ = response.json()
        return json_

    def friends_get(self):

        response = requests.get('https://api.vk.com/method/friends.get',
                                params={
                                    'user_id': self.user_id,
                                    'access_token': self.token,
                                    'v': '5.8'
                                }
                                )
        json_ = response.json()

        friends = json_['response']['items']

        return friends

    def groups_get(self):
        response = requests.get('https://api.vk.com/method/groups.get',
                                params={
                                    'user_id': self.user_id,
                                    'access_token': self.token,
                                    'v': '5.8'
                                }
                                )
        time.sleep(1)
        json_ = response.json()
        print('...')
        if 'error' in json_:
            if self.user_name == 'DELETED':
                print('Пользователь удален')
            else:
                print(f' Пользователь {self.user_name} {self.user_last_name} недоступен')
            return []
        else:
            groups = json_['response']['items']
            return groups

    def __str__(self):
        return 'vk.com/' + str(self.char_id)


def get_group_names(groups):
    response = requests.get('https://api.vk.com/method/groups.getById',
                            params={
                                'group_ids': groups,
                                'access_token': TOKEN,
                                'v': '5.103'
                            })
    json_ = response.json()
    time.sleep(1)
    return json_


def get_group_members(group):
    response = requests.get('https://api.vk.com/method/groups.getMembers',
                            params={
                                'group_id': group,
                                'access_token': TOKEN,
                                'v': '5.103'
                            })
    json_ = response.json()
    # print(json_)
    time.sleep(1)
    return json_['response']['count']


def get_friend_list(username):
    all_friends_group = []
    friend_list = username.friends_get()
    for friend in friend_list:
        user = User(TOKEN, str(friend))
        all_friends_group.extend(user.groups_get())

    return all_friends_group


def main():
    group_list = []
    user = input('Введите id пользователя: ')
    user = User(TOKEN, user)
    groups1 = user.groups_get()
    # print(user.get_id())
    all_friends_group = get_friend_list(user)
    # print(type(all_friends_group), set(all_friends_group))
    # print(type(groups1), groups1)
    mutual_groups = list(set(groups1).difference(set(all_friends_group)))

    for group in mutual_groups:
        group_name = get_group_names(group)['response'][0]['name']
        gid = get_group_names(group)['response'][0]['id']
        members = get_group_members(group)

        # print(group_name, gid, members)
        group_list.append({
            'name': group_name,
            'gid': gid,
            'members_count': members
        })
    # print(group_list)
    with open('groups.json', 'wt', encoding='utf-8') as f:
        f.write(json.dumps(group_list, ensure_ascii=False))


main()