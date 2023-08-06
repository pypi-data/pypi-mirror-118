import requests, json
import click
from prettytable import PrettyTable

from . import util
from . import config

@click.command()
def sizes():
	'''Get available droplet sizes'''
	click.echo()
	click.echo('# Getting available droplet sizes')

	data = util.request('/sizes/', anon=True)
	t = PrettyTable(['Size', 'Price', 'Description'])

	for slug, size in data.items():
		t.add_row([slug, size['price_monthly'], size['description']])

	t.align = 'l'
	t.sortby = 'Price'
	click.echo(t.get_string())
