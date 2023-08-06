
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
from github_webhook import github


         
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

        response = requests.get("https://app.buildpan.com/api/v1/projects/detail/"+project_id)
        data = response.json()

        provider = data['project']["provider"]

        if provider == "github":
            github(project_id, path)

          
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


