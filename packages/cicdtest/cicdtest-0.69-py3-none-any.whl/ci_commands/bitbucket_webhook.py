
"""
    Title: bitbucket_webhook.py
    Author: Kushagra A.
    Language: Python
    Date Created: 31-08-2021
    Date Modified: 03-09-2021
    Description:
        ###############################################################
        ## Create a webhook on a specific bitbucket repository   ## 
         ###############################################################
 """

import requests
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from pathlib import Path
from ci_commands import pull


dotenv_path = Path('./.env')
load_dotenv(dotenv_path=dotenv_path)


         
def bitbucket(project_id, path, refresh_token, key, secret, username, repo_name):
    try:
        
        # Before creating
        print("2")
        dir_list = os.listdir(path) 
        print("List of directories and files before creation:")
        print(dir_list)
        print()

        access_url = "https://bitbucket.org/site/oauth2/access_token"
        grant_body = {
        "grant_type": 'refresh_token',
        "refresh_token": refresh_token
        }

        # generating access token
        response1 = requests.post(access_url, auth=HTTPBasicAuth(key, secret), data=grant_body)
        token = response1.json()['access_token']
        print(token)

        header = {
            "Authorization": 'Bearer ' + token,
            'Content-Type': 'application/json',

        }
            
        # creating a webhook on a particular repository
        hook_url = f"https://api.bitbucket.org/2.0/repositories/{username}/{repo_name}/hooks"
        payload_url = "http://35.225.89.124/bit_webhook"

        response3 = requests.get(hook_url, headers=header)
        data = response3.json()['values']
        print("1")
        hook_body = {
            "description": "Webhook Description",
            "url": payload_url,
            "active": True,
            "events": [
                "repo:push",
                "repo:commit_comment_created",
            ]
        }
        uuid = None
        print("2")

        if len(data) == 0:
            response4 = requests.post(hook_url, headers=header, json=hook_body)

            response6 = requests.post("http://35.225.89.124/get_token",
                                    data={"token": token, "name": username, "repo_name": repo_name})
            print("Webhook created")

            # pull operation
            pull.pull(repo_name, path, project_id, username)
            
        else:
            uuid = data[0]["uuid"][1:-1]
            # print(uuid)

            url4 = hook_url + f"/{uuid}"
            # print(url4)
            print("in")

            response5 = requests.put(url4, headers=header, json=hook_body)
            response6 = requests.post("http://35.225.89.124/get_token", data={"token": token, "name":username, "repo_name":repo_name})
            print("Webhook already exists")

            # pull operation
            pull.pull(repo_name, path, project_id, username)
            

          
    except:
        print("exception occured")
