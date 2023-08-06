
"""
    Title: init.py
    Author: Akash D.
    Modified By: Kushagra A.
    Language: Python
    Date Created: 26-07-2021
    Date Modified: 31-08-2021
    Description:
        ###############################################################
        ## Create a webhook on a specific repository   ## 
         ###############################################################
 """
import time
import dotenv
import requests
import json
import os 
import pathlib
import yaml
import git
import click
import sys
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config, view_defaults
from pyramid.response import Response
from github import Github
import datetime
from dotenv import load_dotenv
from pathlib import Path



ENDPOINT = "webhook"

dotenv_path = Path('./.env')
load_dotenv(dotenv_path=dotenv_path)


         
def github(project_id, path, token, username, repo_name):
    
    try:
        
        # Before creating
        dir_list = os.listdir(path) 
        print("List of directories and files before creation:")
        print(dir_list)
        print()
                           

        access_token =token # access token of github account 
        OWNER = username  # github account name
        REPO_NAME =repo_name # github repository name
        EVENTS = ["*"]      # Events on github
        HOST = os.getenv('HOST')  # server ip (E.g. - ngrok tunnel)
    
        config = {
            "url": "http://{host}/{endpoint}".format(host=HOST, endpoint=ENDPOINT),
            "content_type": "json"
        }
    
        # login to github account
        g = Github(access_token)
        # accessing a particular repository of a account
        repo = g.get_repo("{owner}/{repo_name}".format(owner=OWNER, repo_name=REPO_NAME))
        print(repo)

        push_commit = os.getenv('PUSH_COMMIT_URL')
        fetch_log = os.getenv('FETCH_LOG_URL')
        loop = os.getenv('TIME')
        
        # creating a webhook on a particular repository
        try:
          repo.create_hook("web", config, EVENTS, active=True)
         
        #   pull
          for i in range(int(loop)):
                response = requests.get(push_commit)
                res=response.content
                res=str(res)
                index=res.index("'")
                index1=res.index("'",index+1)
                res=res[index+1:index1]
                print("commit found for repo ",res) 
                val=len(res)
              
      
                if val >0 and res==repo_name:
                    repo = git.Repo(path)
                    origin = repo.remote(name='origin')
                    res=origin.pull()
                    print("Looking for Pull Opeartion")
                    time.sleep(10)
                    curtime = datetime.datetime.now()          
                    response2 = requests.post(fetch_log,data={'project_id':project_id,'repo_name':repo_name,'Time ':curtime,'user_name':username,'message':"pull success",'status':'pull operation performed'}) 

                    val=0
                else:
                    print("no files to pull")
                    time.sleep(10)
                    curtime = datetime.datetime.now()          
                    response2 = requests.post(fetch_log,data={'project_id':project_id,'repo_name':repo_name,'Time ':curtime,'user_name':username,'message':"pull failed",'status':'pull operation performed'}) 

          
        except:
            print("webhook already exists on this repository ")
            flag=0
            print("done")
            #   pull

            for i in range(int(loop)):
                print("1")
                response = requests.get(push_commit)
                res=response.content
                print("2")
                res=str(res)
                index=res.index("'")
                index1=res.index("'",index+1)
                res=res[index+1:index1]
                print("commit found for repo ",res) 
                val=len(res)
    
                if val > 0 and res==repo_name:
                    repo = git.Repo(path)
                    origin = repo.remote(name='origin')
                    res=origin.pull()
                    print("Looking for Pull Opeartion")
                    flag=flag+1
                    time.sleep(60)
                    curtime = datetime.datetime.now()
                    response2 = requests.post(fetch_log,data={'project_id':project_id,'repo_name':repo_name,'Time ':curtime,'user_name':username,'message':"pull success",'status':'pull operation performed'})
                    
                    
                else:
                    print("no files to pull")
                    time.sleep(60)
                    flag=0
                    curtime = datetime.datetime.now()
                    response2 = requests.post(fetch_log,data={'project_id':project_id,'repo_name':repo_name,'Time ':curtime,'user_name':username,'message': "pull failed",'status':'pull operation performed'})
    

          
    except:
        print("config file not found")

# if __name__ == "__main__":
#     config = Configurator()

#     config.add_route(ENDPOINT, "/{}".format(ENDPOINT))
#     config.scan()

#     app = config.make_wsgi_app()
#     server = make_server("localhost", 80, app)
   
#     init()
   
#     server.serve_forever()


