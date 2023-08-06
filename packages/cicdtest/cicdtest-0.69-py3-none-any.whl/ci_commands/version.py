

"""
    Title: version.py
    Author: Akash Dwivedi
    Language: Python
    Date Created: 26-07-2021
    Date Modified: 14-08-2021
    Description:
        ###############################################################
        ## Checks the version of the cli  ## 
         ###############################################################
 """
import click
import json
from dotenv import load_dotenv
import os
from pathlib import Path

dotenv_path = Path('./.env')
load_dotenv(dotenv_path=dotenv_path)



@click.command()
def version():
    '''
    Display the current version of the buildpan
    '''
    """
    Variables Used:
    a : Carries the description of the cli
    y : stores the instance of the json
    version : stores the version of the cli  
    
    return: Nil
   """

    version=os.getenv("version")
    a = '{"version": "0.3", "languages": "Python"}'
    y = json.loads(a)
    version = y["version"]
    # with open(file_path, 'r') as f:
    #      data = json.load(f)
    #      version = data["Version"]
    
    print(f'Current Buildspan version is {version}')