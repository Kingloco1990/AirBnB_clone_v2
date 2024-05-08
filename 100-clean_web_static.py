#!/usr/bin/python3
"""This script deletes out-of-date archives using the do_clean function."""
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
    # Ensure the number of archives is at least 1
    if int(number) == 0:
        number = 1
    number = int(number) + 1

    # Delete unnecessary archives in the versions folder
    local("ls -t versions/ | tail -n +{} | sudo xargs "
          "-I {{}} rm versions/{{}}".format(number))

    # Delete unnecessary archives in the /data/web_static/releases folder
    releases_folder = "/data/web_static/releases"
    # Get the list of releases and split them into a list
    releases = run("ls -tr {} | tail -n +{}".format(
        releases_folder, number)).split('\n')
    for release in releases:
        # Remove each release
        run("rm -rf {}/{}".format(releases_folder, release))
