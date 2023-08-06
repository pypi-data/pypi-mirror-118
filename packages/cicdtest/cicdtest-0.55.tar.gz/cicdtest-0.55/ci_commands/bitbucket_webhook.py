
"""
    Title: init.py
    Author: Kushagra A.
    Language: Python
    Date Created: 31-08-2021
    Date Modified: 31-08-2021
    Description:
        ###############################################################
        ## Create a webhook on a specific bitbucket repository   ## 
         ###############################################################
 """

import requests
import os
import time
import datetime
import git
import subprocess
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from pathlib import Path


dotenv_path = Path('./.env')
load_dotenv(dotenv_path=dotenv_path)


         
def bitbucket(project_id, path, refresh_token, key, secret, name, repo_name):
    print("called")
    try:
        
        # Before creating
        print("2")
        dir_list = os.listdir(path) 
        print("List of directories and files before creation:")
        print(dir_list)
        print()

        # generating access token
        url1 = "https://bitbucket.org/site/oauth2/access_token"
        body1 = {
        "grant_type": 'refresh_token',
        "refresh_token": refresh_token
        }
        username = key
        pwd = secret

        response1 = requests.post(url1, auth=HTTPBasicAuth(username, pwd), data=body1)
        token = response1.json()['access_token']

        # url2 = f"https://api.bitbucket.org/2.0/repositories/{name}"
        # using generated token for other tasks
        header = {
            "Authorization": 'Bearer ' + token,
            'Content-Type': 'application/json',

        }

        # response2 = requests.get(url2, headers=header)
        # full_name = response2.json()['values'][0]['full_name'].split('/')
        # repo_name = full_name[1]
        # print(repo_name)
        
            
        # creating a webhook on a particular repository
        url3 = f"https://api.bitbucket.org/2.0/repositories/{name}/{repo_name}/hooks"

        response3 = requests.get(url3, headers=header)
        data = response3.json()['values']
        hook_url = "http://35.225.89.124/bit_webhook"

        body2 = {
            "description": "Webhook Description",
            "url": hook_url,
            "active": True,
            "events": [
                "repo:push",
                "issue:created",
                "issue:updated",
                "repo:commit_comment_created",
                "pullrequest:created",
                "pullrequest:updated"
            ]
        }
        uuid = None
        loop = os.getenv('TIME')
        push_commit = os.getenv('PUSH_COMMIT_URL')
        print("before hook")
        print(data[0]["url"])

        if len(data) == 0 or data[0]["url"] != hook_url:
            print("in again")
            print(url3)
            print(header)
            print(body2)
            response4 = requests.post(url3, headers=header, json=body2)
            uuid = response4.json()["uuid"]
            print("post")

            response6 = requests.post("http://35.225.89.124/get_token",
                                    data={"token": token, "name": name, "repo_name": repo_name})
            print("Webhook created")
            
            #   pull
            for i in range(int(loop)):
                response = requests.get(push_commit)
                res=response.content
                res=str(res)
                index=res.index("'")
                index1=res.index("'",index+1)
                res=res[index+1:index1]
                print(res)
                print("commit found for repo ",res) 
                val=len(res)
                
        
                if val >0 and res==repo_name:
                    repo = git.Repo(path)
                    res=subprocess.run(["git","pull"],check=True)
                    print("Looking for Pull Opeartion")
                    time.sleep(10)
                    print("done")
                    # curtime = datetime.datetime.now()          
                    # response2 = requests.post("fetch_log",data={'project_id':project_id,'repo_name':repo_name,'Time ':curtime,'user_name':username,'message':"pull success",'status':'pull operation performed'}) 

                    val=0
                else:
                    print("no files to pull")
                    time.sleep(10)
                    # curtime = datetime.datetime.now()          
                    # response2 = requests.post("fetch_log",data={'project_id':project_id,'repo_name':repo_name,'Time ':curtime,'user_name':username,'message':"pull failed",'status':'pull operation performed'})
        else:
            uuid = data[0]["uuid"][1:-1]
            # print(uuid)

            url4 = url3 + f"/{uuid}"
            # print(url4)

            response5 = requests.put(url4, headers=header, json=body2)
            response6 = requests.post("http://35.225.89.124/get_token", data={"token": token, "name":name, "repo_name":repo_name})
            print("Webhook already exists")

            # pull
            for i in range(int(loop)):
                print("1")
                response = requests.get(push_commit)
                res=response.content
                print("2")
                res=str(res)
                index=res.index("'")
                index1=res.index("'",index+1)
                res=res[index+1:index1]
                print(res)
                print("commit found for repo ",res) 
                val=len(res)
        
                if val > 0 and res==repo_name:
                    repo = git.Repo(path)
                    res=subprocess.run(["git","pull"],check=True)
                    print("Looking for Pull Opeartion")
                    flag=flag+1
                    time.sleep(60)
                    # curtime = datetime.datetime.now()
                    # response2 = requests.post("fetch_log",data={'project_id':project_id,'repo_name':repo_name,'Time ':curtime,'user_name':username,'message':"pull success",'status':'pull operation performed'})
                        
                        
                else:
                    print("no files to pull")
                    time.sleep(60)
                    flag=0
                    # curtime = datetime.datetime.now()
                    # response2 = requests.post("fetch_log",data={'project_id':project_id,'repo_name':repo_name,'Time ':curtime,'user_name':username,'message': "pull failed",'status':'pull operation performed'})
        

          
    except:
        print("exception occured")
