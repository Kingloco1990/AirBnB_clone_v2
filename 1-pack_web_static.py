#!/usr/bin/python3
"""This script creates a compressed .tgz archive of the web_static folder."""

from fabric.api import local
from datetime import datetime


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
