import requests, json, os, subprocess, time
import click

from . import util
from . import config

@click.command()
@click.argument('release', required=False, type=int, nargs=1)
@click.option('--releases', is_flag=True, help='Get a list of valid releases to rollback')
def rollback(release=None, releases=False):
	'''Rollback production to a previous release'''
	root = util.find_root()
	sail_config = util.get_sail_config()

	if releases or not release:
		data = util.request('/rollback')
		click.echo('# Available releases:')
		if data.get('releases', []):
			for r in data.get('releases', []):
				flags = '(current)' if r == data.get('current_release') else ''
				click.echo('- %s %s' % (r, flags))

			click.echo()
			click.echo('Rollback with: sail rollback <release>')
		else:
			click.echo('- No releases found, perhaps you should deploy something')

		return

	if release:
		release = str(release)

	click.echo()
	click.echo('# Rolling back')

	if release:
		click.echo('- Requesting Sail API to rollback: %s' % release)
	else:
		click.echo('- Requesting Sail API to rollback')

	data = util.request('/rollback/', json={'release': release})
	task_id = data.get('task_id')
	rollback_release = data.get('release')

	if not task_id:
		raise click.ClickException('Could not obain a rollback task_id.')

	click.echo('- Scheduled successfully, waiting for rollback')

	try:
		data = util.wait_for_task(task_id, timeout=300, interval=5)
	except:
		raise click.ClickException('Rollback failed')

	click.echo('- Successfully rolled back to %s' % rollback_release)
