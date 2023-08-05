import json

import click

from lib import list_bags, print_available_space, delete_keep, delete_until, copy_bag
from config import get_config, save_config


@click.group()
@click.version_option()
def cli():
    """Zotac tools
    This package simplifies remote manipulation of rosbags on zotac.
    It lets you copy rosbags to your PC and delete old robags.
    It also provides a view of all rosbags grouped by date.
    """


@cli.command()
@click.argument("n", default=-2, type=int)
@click.argument("path", default=".", type=click.Path(exists=True))
@click.option("-l", "--logs-only", is_flag=True)
def copy(n, path, logs_only):
    config = get_config()
    copy_bag(config["log-directory"], path, n, config["remote"], logs_only=logs_only)


@cli.command()
@click.option("-u", "--until", type=int)
@click.option("-k", "--keep", type=int)
@click.option("-a", "--all", is_flag=True)
def delete(until, keep, all):
    config = get_config()
    if until:
        delete_until(config["log-directory"], until, config["remote"])
    elif keep:
        delete_keep(config["log-directory"], keep, config["remote"])
    elif all:
        delete_keep(config["log-directory"], 0, config["remote"])


@cli.command()
def status():
    config = get_config()
    print_available_space(config["disk-name"], config["remote"])


@cli.command()
def list():
    config = get_config()
    list_bags(config["log-directory"], config["remote"])


@cli.command("config")
@click.option("-s", "--show", is_flag=True)
@click.argument("args", nargs=-1)
def configure(show, args):
    config = get_config()

    if show:
        return click.echo(json.dumps(config, indent=2))

    d = dict(zip(args[::2], args[1::2]))
    for key, value in d.items():
        if key == "remote":
            config["remote"] = value
        elif key == "logdir" or key == "log-directory":
            config["log-directory"] = value
        elif key == "disk" or key == "disk-name":
            config["disk-name"] = value

    save_config(config)


if __name__ == "__main__":
    cli()
