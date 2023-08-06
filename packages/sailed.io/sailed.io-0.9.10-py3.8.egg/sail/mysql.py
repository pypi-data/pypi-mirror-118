import os, subprocess
import click

from . import util

@click.command()
def mysql():
	'''Open an interactive MySQL shell on the production host'''
	root = util.find_root()
	sail_config = util.get_sail_config()

	click.echo('Spawning an interactive MySQL shell at %s.sailed.io' % sail_config['app_id'])

	os.execlp('ssh', 'ssh', '-t',
		'-i', '%s/.sail/ssh.key' % root,
		'-o', 'UserKnownHostsFile=%s/.sail/known_hosts' % root,
		'-o', 'IdentitiesOnly=yes',
		'-o', 'IdentityFile=%s/.sail/ssh.key' % root,
		'root@%s.sailed.io' % sail_config['app_id'],
		'docker exec -it sail sudo -u www-data wp --path=/var/www/public db cli'
	)
