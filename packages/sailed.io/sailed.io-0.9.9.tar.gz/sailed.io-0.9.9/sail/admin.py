import webbrowser
import click

from . import util

@click.command()
def admin():
	'''Open your default web browser to the wp-login.php location of your site'''
	root = util.find_root()
	sail_config = util.get_sail_config()

	webbrowser.open(sail_config['login_url'])
