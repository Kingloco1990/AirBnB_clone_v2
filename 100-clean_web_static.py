#!/usr/bin/python3
"""This script deletes out-of-date archives using the function do_clean."""
from fabric.api import local, run, env
from os.path import exists

# Define the list of host IP addresses
env.hosts = ['54.164.209.217', '18.204.9.187']


def do_clean(number=0):
    """
    Deletes out-of-date archives.

    Args:
        number (int): Number of archives, including the most recent, to keep.
            Defaults to 0.

    Returns:
        None
    """
    # Delete unnecessary archives in the versions folder
    local("ls -t versions/ | tail -n +{} | sudo xargs rm -fr".format(
        number + 1))

    # Delete unnecessary archives in the /data/web_static/releases folder
    releases_folder = "/data/web_static/releases"
    releases = run("ls -tr {} | tail -n +{}".format(
        releases_folder, number)).split('\n')
    for release in releases:
        run("rm -rf {}/{}".format(releases_folder, release))
