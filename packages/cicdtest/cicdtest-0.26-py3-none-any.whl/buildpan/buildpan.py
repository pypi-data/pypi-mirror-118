"""
    Title: buildpan
    Module Name: buildpan
    Author: Akash Dwivedi
    Language: Python
    Date Created: 26-07-2021
    Date Modified: 20-08-2021
    Description:
        ###############################################################
        ##  Main operating file for all the cli commands             ## 
         ###############################################################
 """

import git
import os
import click
import git
import sys
from github import Github
import subprocess

from pyfiglet import Figlet

'''
This contains the code snippet for the cli header.
'''
f = Figlet(font='slant')
print (f.renderText('Buildpan'))


# cli_commands for the buildpan 

from cli_commands import init
from cli_commands import version

@click.group(help="CLI tool to manage CI- CD of projects")
def buildpan():
    pass

'''
 This containes all the commands for the buildpan cli
'''
buildpan.add_command(init.init)
buildpan.add_command(version.version)

if __name__ == '__main__':
    buildpan()