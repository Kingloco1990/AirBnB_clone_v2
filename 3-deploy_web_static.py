#!/usr/bin/python3
"""This script creates and distributes an archive to your web servers,
   using the function deploy.
"""
from fabric.api import local, run, env, put
from datetime import datetime
from os.path import exists

# Define the list of host IP addresses
env.hosts = ['54.164.209.217', '18.204.9.187']


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.

    Returns:
        str: Path to the generated archive on success, None on failure.
    """
    # Create the versions directory if it doesn't exist
    local("mkdir -p versions")

    # Get the current date and time
    now = datetime.now()

    # Format the current date and time to use in the archive name
    timestamp = now.strftime("%Y%m%d%H%M%S")

    # Create the archive file name
    archive_name = "web_static_" + timestamp + ".tgz"

    # Compress the web_static folder into the archive
    result = local("tar -cvzf versions/{} web_static".format(archive_name))

    # Check if the archive was successfully created
    if result.failed:
        return None
    else:
        # Return the path to the archive
        return "versions/{}".format(archive_name)


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


def deploy():
    """
    Deploys the archive to the web servers.
    """
    # Call do_pack to create the archive
    archive_path = do_pack()

    if archive_path is None:
        return False

    # Call do_deploy to distribute the archive
    result = do_deploy(archive_path)

    return result
