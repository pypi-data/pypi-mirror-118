import click
import os
import sqlite3
from sqlite3 import Error
from .connection import *

@click.command(name='finda', help='Finds data by service')
@click.argument('service')
def finda(service):
	findDataByService(f"{service}")