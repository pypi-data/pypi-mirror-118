import requests, json
import click
from prettytable import PrettyTable

from . import util
from . import config

@click.command()
def regions():
	'''Get available deployment regions'''
	click.echo()
	click.echo('# Getting available regions')

	data = util.request('/regions/', anon=True)
	t = PrettyTable(['Slug', 'Name'])

	for slug, region in data.items():
		t.add_row([slug, region['name']])

	t.align = 'l'
	click.echo(t.get_string())
