import configparser

import click
import keyring

from ..utils import taskstatus


@click.command()
@click.argument("service", required=False)
@click.pass_obj
def logout(lancet, service):
    """Forget saved passwords for the web services."""

    default = ["tracker", "timer", "scm-manager"]
    services = [service] if service else default

    try:
        for service in services:
            url = lancet.get_config_from_key(service, "url")
            username = lancet.get_config_from_key(service, "username")
            key = "lancet+{}".format(url)
            with taskstatus("Logging out from {}", url) as ts:
                if keyring.get_password(key, username):
                    keyring.delete_password(key, username)
                    ts.ok("Logged out from {}", url)
                else:
                    ts.ok("Already logged out from {}", url)
    except configparser.NoOptionError as error:
        click.secho(str(error), fg="red")


@click.command()
@click.pass_obj
def _services(lancet):
    """List all currently configured services."""

    def get_services(config):
        for s in config.sections():
            url = config.has_option(s, "url")
            username = config.has_option(s, "username")
            # make sure empty values are not shown
            if url and username and lancet.config.get(s, "url"):
                yield s

    for s in get_services(lancet.config):
        click.echo("{}[Logout from {}]".format(s, lancet.config.get(s, "url")))
