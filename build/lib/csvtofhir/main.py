#main.py

import sys
import click
import os.path
from csvtofhir import tofhir

default_file = os.path.abspath(os.path.join(os.path.dirname(__file__),"..")) + 'NSCLCStageIIIAnonymized.csv'

@click.group()
def cli():
    pass

@click.command()
@click.option('-- input','--i',default= default_file, type=click.path(), help = "Input path for csv file")
@click.option('--bundle','--b',default = 1, type=(bool), help = "Flag for bundle creation of the resources")
@click.pass_context
def tofhir(ctx, input,):
    click.echo(input)


@click.command()
def profile():
    click.echo("Add Profiles/ Delete Profiles/ List profiles")

def map():
    click.echo("List Profiles, map header to profiles templates")

if __name__== "__main__":
    cli()

