import click
import os
import sqlite3
from sqlite3 import Error
from .connection import *

@click.command(name='store', help='Stores the given data (service email password)')
@click.argument('service', type=str)
@click.argument('email', type=str)
@click.argument('password', type=str)
def store(service, email, password):
	storePassword(f"{service}",f"{email}",f"{password}")