import click

from . import util, config

# Commands
from . import init
from . import deploy
from . import download
from . import admin
from . import ssh
from . import mysql
from . import wp
from . import domain
from . import sizes
from . import regions
from . import backup
from . import logs
from . import rollback

@click.group()
@click.version_option(config.VERSION, message='%(version)s')
@click.option('--debug', '-d', is_flag=True, help='Enable verbose debug logging')
def cli(debug):
	util.debug(debug)

cli.add_command(init.init)
cli.add_command(deploy.deploy)
cli.add_command(download.download)
cli.add_command(admin.admin)
cli.add_command(ssh.ssh)
cli.add_command(mysql.mysql)
cli.add_command(wp.wp)
cli.add_command(domain.domain)
cli.add_command(sizes.sizes)
cli.add_command(regions.regions)
cli.add_command(backup.backup)
cli.add_command(logs.logs)
cli.add_command(rollback.rollback)

@cli.command('config')
@click.argument('name', required=True, nargs=1)
@click.argument('value', required=False)
@click.option('--delete', is_flag=True)
def config_cmd(name, value=None, delete=False):
	'''Set reusable config variables'''
	valid_names = [
		'provider-token',
		'email',
		'api-base',
	]

	if name not in valid_names:
		raise click.ClickException('Invalid config name: %s' % name)

	import pathlib, json
	filename = (pathlib.Path.home() / '.sail-defaults.json').resolve()
	data = {}

	try:
		with open(filename) as f:
			data = json.load(f)

	except:
		pass

	if not value and not delete:
		if name not in data:
			raise click.ClickException('The option is not set')

		click.echo(data[name])
		return

	if value and delete:
		raise click.ClickException('The --delete flag does not expect an option value')

	if delete and name not in data:
		raise click.ClickException('The option is not set, nothing to delete')

	if delete:
		del data[name]
		click.echo('Option %s deleted' % name)
	else:
		data[name] = value
		click.echo('Option %s set' % name)

	with open(filename, 'w+') as f:
		json.dump(data, f, indent='\t')
