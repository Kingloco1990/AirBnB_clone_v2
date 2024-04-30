#!/usr/bin/python3
"""
Deployment script for distributing an archive to web servers.
"""
from fabric.api import run, env, put
from os.path import exists

# Define the list of host IP addresses
env.hosts = ['54.164.209.217', '18.204.9.187']


def do_deploy(archive_path):
    """
    Distributes an archive to web servers.

    :param archive_path: Path to the archive file to deploy.
    :type archive_path: str
    :return: True if deployment was successful, False otherwise.
    :rtype: bool
    """

    # Check if the archive file exists
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory on the web server
        put(archive_path, '/tmp/')

        # Extract the archive to the folder:
        # /data/web_static/releases/<archive filename without extension>
        archive_name = archive_path.split('/')[-1]
        folder_name = archive_name.split('.')[0]
        run('mkdir -p /data/web_static/releases/{}/'.format(folder_name))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.format(
            archive_name, folder_name))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(archive_name))

        # Move the contents of the extracted folder to the parent folder
        run('mv /data/web_static/releases/{}/web_static/* '
            '/data/web_static/releases/{}/'.format(folder_name, folder_name))

        # Remove the extracted folder
        run('rm -rf /data/web_static/releases/{}/web_static'.format(
            folder_name))

        # Remove the current symbolic link
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link linked to the new version of the code
        run('ln -s /data/web_static/releases/{}/ '
            '/data/web_static/current'.format(folder_name))

        return True

    except Exception:
        return False
