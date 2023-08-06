import requests, json, os, subprocess, time
import click

from . import util
from . import config

@click.command()
@click.option('--with-uploads', is_flag=True, help='Include the wp-content/uploads directory')
@click.option('--delete', is_flag=True, help='Delete files from production that do not exist in your working copy')
def deploy(with_uploads, delete):
	'''Deploy your working copy to production'''
	root = util.find_root()
	sail_config = util.get_sail_config()

	app_id = sail_config['app_id']
	release_name = str(int(time.time()))

	click.echo()
	click.echo('# Deploying to production')

	rsync_args = ['rsync', ('-rtlv' if util.debug() else '-rtl')]
	if delete:
		rsync_args.extend(['--delete'])
	rsync_args.extend(['--rsync-path', 'sudo -u www-data rsync'])
	rsync_args.extend(['-e', 'ssh -i %s/.sail/ssh.key -o UserKnownHostsFile=%s/.sail/known_hosts -o IdentitiesOnly=yes -o IdentityFile=%s/.sail/ssh.key' % (root, root, root)])

	click.echo('- Uploading application files to production')

	# Ship some files to production.
	p = subprocess.Popen(rsync_args + [
		'--filter', '- .*', # Exclude all dotfiles
		'--filter', '- wp-content/debug.log',
		'--filter', '- wp-content/uploads',
		'--copy-dest', '/var/www/public/',
		'%s/' % root,
		'root@%s.sailed.io:/var/www/releases/%s' % (app_id, release_name)
	])

	while p.poll() is None:
		util.loader()

	if p.returncode != 0:
		raise click.ClickException('An error occurred during upload. Please try again.')

	if with_uploads:
		click.echo('- Uploading wp-content/uploads')

		# Send uploads to production
		p = subprocess.Popen(rsync_args + [
			'%s/wp-content/uploads/' % root,
			'root@%s.sailed.io:/var/www/uploads/' % app_id
		])

		while p.poll() is None:
			util.loader()

		if p.returncode != 0:
			raise click.ClickException('An error occurred during upload. Please try again.')

	click.echo('- Requesting Sail API to deploy: %s' % release_name)

	data = util.request('/deploy/', json={'release': release_name})
	task_id = data.get('task_id')

	if not task_id:
		raise click.ClickException('Could not obain a deploy task_id.')

	click.echo('- Scheduled successfully, waiting for deploy')

	try:
		data = util.wait_for_task(task_id, timeout=300, interval=5)
	except:
		raise click.ClickException('Deploy failed')

	click.echo('- Successfully deployed %s' % release_name)
