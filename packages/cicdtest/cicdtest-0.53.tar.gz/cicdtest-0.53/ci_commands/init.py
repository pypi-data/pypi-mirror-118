
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
from ci_commands import github_webhook, bitbucket_webhook, encrypt


         
@click.command()
def init():
    '''
    For initiating the webhook operation 

    Please store config.yaml in the directory 
    Please create the clone of the repository  
    \f
    
   
    '''
    
    path=pathlib.Path().resolve()
    print("Your current directory  is : ", path)
    os.chdir(path)
    try:
        a_yaml_file = open("./config.yaml")
        parsed_yaml_file = yaml.load(a_yaml_file, Loader=yaml.FullLoader)
        project_id=parsed_yaml_file["project_id"]
        print(project_id)

        response = requests.get("https://app.buildpan.com/api/v1/projects/detail/"+project_id)
        data = response.json()

        provider = data['project']["provider"]
        

        if provider == "github":
            name = data["project"]["repo"]["full_name"].split('/')
            token = data["project"]["githubtoken"]
            username = name[0]
            repo_name = name[1]

            dictionary ={
                "token" : token,
                "username" : username,
                "repo_name" : repo_name,
            }

            # Serializing json 
            json_object = json.dumps(dictionary, indent = 4)
        
            # Writing to sample.json
            with open(project_id+'.json',"w") as outfile:
                outfile.write(json_object)
            
            enc = encrypt.Encryptor()
            #mykey=enc.key_create()
            #enc.key_write(mykey, 'mykey.key')
            loaded_key=enc.key_load('mykey.key')
            # enc.encrypt_file(loaded_key, project_id+'.json')

            enc.decrypt_file(loaded_key, project_id+'.json.enc')
        
            #Reading from json file
            with open(project_id+'.json') as file:
                info = json.load(file)
                username = info["username"]
                token = info["token"]
                repo_name = info["repo_name"]

            github_webhook.github(project_id, path, token, username, repo_name)
        
        elif provider == "bitbucket":
            name = data["project"]["repo"]["full_name"].split('/')
            token = data["project"]["repo"]["refresh_token"]
            username = name[0]
            repo_name = name[1]
            print("in")

            dictionary ={
                "refresh_token" : token,
                "username" : username,
                "repo_name" : repo_name,
            }
            print("1")
            # Serializing json 
            json_object = json.dumps(dictionary, indent = 4)
            
            # Writing to sample.json
            with open(project_id+'.json',"w") as outfile:
                outfile.write(json_object)
            
            print("2")
            # Reading from json file
            with open(project_id+'.json') as file:
                info = json.load(file)
                print("innn")
                username1 = info["username"]
                refresh_token1 = info["refresh_token"]
                print("2")
                repo_name1 = info["repo_name"]
            
            print("4")
            
            key = "HB2xRCZSyKYMcTS9rm"
            secret_key = "pQA5FMShe6deqr2b8Eq3GfDBmhEnn77C"
            
            print("3")
            bitbucket_webhook.bitbucket(project_id, path, refresh_token1, key, secret_key, username1, repo_name1)
            

          
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


