import subprocess
from subprocess import check_output
import os
import sys
import datetime
from datetime import datetime
from collections import defaultdict

import click


def execute_on_remote(command, remote):
    return check_output(["ssh", remote, command]).decode("utf-8")


def copy_from_remote(source, target, remote):
    # run() does not properly preserve quotes when passed as a list
    subprocess.run(
        " ".join(["scp", "-T", "-r", f"{remote}:{source}", target]),
        shell=True,
        stderr=sys.stderr,
        stdout=sys.stdout,
    )


def print_available_space(disk, remote):
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


def list_bags(source, remote):
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


def delete_until(source, until, remote):
    bags = list_dir(source, remote)

    if bags[:until]:
        command = "rm -r"
        for bag in bags[:until]:
            command += f" {os.path.join(source, bag)}"
        execute_on_remote(command, remote)


def delete_keep(source, keep, remote):
    bags = list_dir(source, remote)

    if bags[:-keep]:
        command = "rm -r"
        for bag in bags[:-keep]:
            command += f" {os.path.join(source, bag)}"
        execute_on_remote(command, remote)


def copy_bag(source, target, n, remote, logs_only=False):
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

        logs = [os.path.join(path, log) for log in logs]
        logs = " ".join(logs)
        logs = f'"{logs}"'

        target = os.path.join(target, bag)
        os.mkdir(target)
        copy_from_remote(logs, target, remote)

    else:
        copy_from_remote(os.path.join(source, bag), target, remote)
