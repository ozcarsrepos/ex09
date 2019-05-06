#!/usr/bin/env python3

import requests
import json
import logging  # NOQA
import sys
logger = logging.getLogger(__name__)    # NOQA


# Get all the repos from the input data
def repos_list(input_data):
    ses = requests.Session()
    resp = ses.get(input_data)
    jdata = json.loads(resp.text)
    result = {}
    for record in jdata:
        proj_name = record['full_name'].split('/')[1]
        proj_desc = record['description']
        result[proj_name] = proj_desc
    return result


# Use repos_list with username
def solve(username):
    input_data = 'https://api.github.com/users/' + username + '/repos'
    result = repos_list(input_data)
    return result


# Main app
def main():
    username = sys.argv[1]
    print('Listing all projects of %s:', username)
    for order, (name, desc) in enumerate(solve(username).items(), 1):
        print('Project {}: {} - {}'.format(order, name, desc))
    print('-------------------\nTotal projects: ', order)


if __name__ == "__main__":
    main()
