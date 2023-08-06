import json

import click

from .lib import (
    list_bags,
    print_available_space,
    delete_keep,
    delete_until,
    copy_bag,
    get_available_remote,
)
from .config import get_config, save_config


def get_remote(func):
    def wrapper(*args, **kwargs):
        config = kwargs["config"]
        if remote := get_available_remote(config["remotes"], verbose=kwargs["verbose"]):
            func(*args, **kwargs, remote=remote)
        else:
            click.secho("No available remote found", fg="red")

    return wrapper


@click.group()
@click.version_option()
def cli():
    """Zotac tools
    This package simplifies remote manipulation of rosbags on zotac.
    It lets you copy rosbags to your PC and delete old robags.
    It also provides a view of all rosbags grouped by date.
    """


@cli.command("copy")
@click.argument("n", default=-2, type=int)
@click.argument("path", default=".", type=click.Path(exists=True))
@click.option("-l", "--logs-only", is_flag=True)
@click.option("-v", "--verbose", is_flag=True)
@get_config
@get_remote
def copy(n, path, logs_only, verbose, config, remote):
    copy_bag(config["log-directory"], path, n, remote, logs_only=logs_only, verbose=verbose)


@cli.command("delete")
@click.option("-u", "--until", type=int)
@click.option("-k", "--keep", type=int)
@click.option("-a", "--all", is_flag=True)
@click.option("-v", "--verbose", is_flag=True)
@get_config
@get_remote
def delete(until, keep, all, verbose, config, remote):
    if until:
        delete_until(config["log-directory"], until, remote, verbose=verbose)
    elif keep:
        delete_keep(config["log-directory"], keep, remote, verbose=verbose)
    elif all:
        delete_keep(config["log-directory"], 0, remote, verbose=verbose)


@cli.command("status")
@click.option("-v", "--verbose", is_flag=True)
@get_config
@get_remote
def status(verbose, config, remote):
    print_available_space(config["disk-name"], remote, verbose=verbose)


@cli.command("list")
@click.option("-v", "--verbose", is_flag=True)
@get_config
@get_remote
def list(verbose, config, remote):
    list_bags(config["log-directory"], remote, verbose=verbose)


@cli.command("config")
@click.option("-s", "--show", is_flag=True)
@click.argument("args", nargs=-1)
@click.option("-v", "--verbose", is_flag=True)
@get_config
def configure(show, args, verbose, config):
    if show:
        return click.echo(json.dumps(config, indent=2))

    d = dict(zip(args[::2], args[1::2]))
    for key, value in d.items():
        if key == "remotes":
            config["remotes"] = value.split(",")
        elif key == "logdir" or key == "log-directory":
            config["log-directory"] = value
        elif key == "disk" or key == "disk-name":
            config["disk-name"] = value

    if verbose:
        click.secho("New config:", fg="yellow")
        click.echo(json.dumps(config, indent=2))

    save_config(config)


if __name__ == "__main__":
    cli()
