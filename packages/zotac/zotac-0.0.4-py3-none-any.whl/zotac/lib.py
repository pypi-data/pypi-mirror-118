import subprocess
from subprocess import check_output, CalledProcessError
import os
import sys
import datetime
from datetime import datetime
from collections import defaultdict
import concurrent.futures

import click


def check_connection(remote, timeout):
    try:
        check_output(["ssh", "-q", "-o", f"ConnectTimeout={timeout}", remote, "exit"])
    except CalledProcessError:
        return False

    return True


def get_available_remote(remotes, timeout=2, verbose=False):
    if verbose:
        click.secho("Checking for available remotes:", fg="yellow")
        click.echo("\n".join(f"- {remote}" for remote in remotes))

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(check_connection, remote, timeout) for remote in remotes
        ]

        results = [f.result() for f in futures]

    for remote, result in zip(remotes, results):
        if result:
            if verbose:
                click.secho("Selected remote: ", fg="green", nl=False)
                click.echo(remote)
            return remote

    return None


def execute_on_remote(command, remote, verbose=False):
    if verbose:
        click.echo(f"Executing on remote {remote}: {command}")
    return check_output(["ssh", remote, command]).decode("utf-8")


def copy_from_remote(source, target, remote, verbose=False):
    # run() does not properly preserve quotes when passed as a list
    command = " ".join(["scp", "-T", "-r", f"{remote}:{source}", target])

    if verbose:
        click.echo(f"Copying from remote {remote}: {command}")

    subprocess.run(
        command,
        shell=True,
        stderr=sys.stderr,
        stdout=sys.stdout,
    )


def print_available_space(disk, remote, verbose=False):
    if verbose:
        click.echo("Checking available space..")

    command = "df -h"
    output = execute_on_remote(command, remote).strip().splitlines()
    output = [row.split()[:5] for row in output]

    for disk_name, size, used, avail, use_percent in output:
        if disk_name == disk:
            return click.echo(
                f"{disk}: Available: {avail}, Used: {used}/{size}({use_percent})"
            )

    click.secho("Specified disk not found", fg="red")


def list_dir(folder, remote):
    return execute_on_remote(f"ls {folder}", remote).strip().split()


def get_bags(source, remote):
    command = f"du -h --max-depth=1 {source}"
    bags = execute_on_remote(command, remote)
    bags = bags.strip().splitlines()[:-1]
    bags = [row.split() for row in bags]

    folders = defaultdict(list)

    for size, path in bags:
        bag = os.path.basename(path)
        dt = datetime.fromisoformat(bag)
        date = dt.strftime("%Y-%m-%d")
        time = dt.strftime("%H:%M")
        folders[date].append({"time": time, "size": size})

    return folders


def list_bags(source, remote, verbose=False):
    if verbose:
        click.echo("Collecting bags to display..")

    bag_tree = get_bags(source, remote)

    folders = sorted(bag_tree.keys())
    n_folders = len(folders)
    n = 0

    output = f"{source}\n"

    for i, folder in enumerate(folders):
        last_folder = i == n_folders - 1
        prefix = "└──" if last_folder else "├──"
        output += f"{prefix} {datetime.fromisoformat(folder).strftime('%d/%m/%Y')}\n"

        bags = sorted(bag_tree[folder], key=lambda bag: bag["time"])
        n_bags = len(bags)
        for j, bag in enumerate(bags):
            last_bag = j == n_bags - 1
            folder_prefix = "   " if last_folder else "│  "
            bag_prefix = "└──" if last_bag else "├──"
            output += f"{folder_prefix} {bag_prefix} [{click.style(n, fg='yellow')}] {click.style(bag['time'], fg='cyan')} ({bag['size']})\n"
            n += 1

    click.echo(output)


def delete_until(source, until, remote, verbose=False):
    bags = list_dir(source, remote)

    if bags[:until]:
        if verbose:
            click.secho("Bags selected for deletion:", fg="yellow")
            click.echo("\n".join(f"- {bag}" for bag in bags[:until]))

        command = "rm -r"
        for bag in bags[:until]:
            command += f" {os.path.join(source, bag)}"
        execute_on_remote(command, remote)

    if verbose:
        click.secho("Deleted", fg="green")


def delete_keep(source, keep, remote, verbose=False):
    bags = list_dir(source, remote)

    if bags[:-keep]:
        if verbose:
            click.secho("Bags selected for deletion:", fg="yellow")
            click.echo("\n".join(f"- {bag}" for bag in bags[:-keep]))

        command = "rm -r"
        for bag in bags[:-keep]:
            command += f" {os.path.join(source, bag)}"
        execute_on_remote(command, remote)

    if verbose:
        click.secho("Deleted", fg="green")


def copy_bag(source, target, n, remote, logs_only=False, verbose=False):
    bags = sorted(list_dir(source, remote))
    try:
        bag = bags[n]
    except IndexError:
        return click.secho("Selected bag does not exist", fg="red")

    path = os.path.join(source, bag)

    if logs_only:
        files = list_dir(path, remote)
        logs = [
            file
            for file in files
            if not file.endswith(".active") and not file.endswith(".bag")
        ]

        if verbose:
            click.secho("Selected logs:", fg="yellow")
            click.echo("\n".join(f"- {log}" for log in logs))

        logs = [os.path.join(path, log) for log in logs]
        logs = " ".join(logs)
        logs = f'"{logs}"'

        target = os.path.join(target, bag)
        os.mkdir(target)
        copy_from_remote(logs, target, remote)

    else:
        copy_from_remote(os.path.join(source, bag), target, remote)
