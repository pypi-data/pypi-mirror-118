import requests, json, os, subprocess, time
import click

from . import util

@click.command()
@click.option('--yes', '-y', is_flag=True, help='Force Y on overwriting local copy')
@click.option('--with-uploads', is_flag=True, help='Include the wp-content/uploads directory')
@click.option('--delete', is_flag=True, help='Delete files from local copy that do not exist on production')
def download(yes, with_uploads, delete):
	'''Download files from production to your working copy'''
	root = util.find_root()
	sail_config = util.get_sail_config()

	if not yes:
		click.confirm('Downloading files from production may overwrite '
			+ 'your local copy. Continue?',
			abort=True
		)

	app_id = sail_config['app_id']

	click.echo()
	click.echo('# Downloading application files from production')

	rsync_args = ['rsync', ('-rtlv' if util.debug() else '-rtl')]
	if delete:
		rsync_args.extend(['--delete'])
	rsync_args.extend(['-e', 'ssh -i %s/.sail/ssh.key -o UserKnownHostsFile=%s/.sail/known_hosts -o IdentitiesOnly=yes -o IdentityFile=%s/.sail/ssh.key' % (root, root, root)])

	# Download files FROM production
	p = subprocess.Popen(rsync_args + [
		'--filter', '- .*', # Exclude all dotfiles
		'--filter', '- wp-content/debug.log',
		'--filter', '- wp-content/uploads',
		'root@%s.sailed.io:/var/www/public/' % app_id,
		'%s/' % root,
	])

	while p.poll() is None:
		util.loader()

	if p.returncode != 0:
		raise click.ClickException('An error occurred during download. Please try again.')

	if with_uploads:
		click.echo('- Downloading wp-content/uploads')

		# Download uploads from production
		p = subprocess.Popen(rsync_args + [
			'root@%s.sailed.io:/var/www/uploads/' % app_id,
			'%s/wp-content/uploads/' % root,
		])

		while p.poll() is None:
			util.loader()

		if p.returncode != 0:
			raise click.ClickException('An error occurred during download. Please try again.')

	click.echo('- Files download completed')
