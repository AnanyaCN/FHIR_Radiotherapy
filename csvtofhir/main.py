#main.py

import sys
import click
import os.path
from csvtofhir.tofhir import radData

default_file = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")),'NSCLCStageIIIAnonymized.csv')

@click.group()
def cli():
    click.secho("Radiotherapy Clinical Data to FHIR cli", fg='blue', bold=True)

@click.command()
@click.option('--flag',default=True,type= bool, help="Default Mode Set")
@click.argument('name',type= click.Path(), required = False)
def tofhir(flag,name):
    if flag:
        click.secho("Parsing with default file - NSCLC Stage III Anonymized ~ Maastro", fg='green', bold = True)
        csvfile = default_file
    else:
        csvfile = click.format_filename(name)

    df = radData()
    df.parse_csv(csvfile)

@click.command()
@click.option('--count',default=1, help="Profiling")
@click.argument('naam')
def profile(count,naam):
    for x in range(count):
        click.echo('Profile adding %s' %naam)



cli.add_command(tofhir)
cli.add_command(profile)


if __name__== "__main__":
    cli()
