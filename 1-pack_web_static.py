#!/usr/bin/python3
import os
from datetime import datetime
from fabric.api import local, runs_once


@runs_once
def do_pack():
    """Creates and compresses an archive of web_static directory."""
    try:
        # Get the current timestamp for the archive name.
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

        # Create archive directory if it doesn't exist.
        if not os.path.isdir('versions'):
            os.mkdir('versions')

        # Create the archive name.
        archive_name = f"versions/web_static_{timestamp}.tgz"

        # Compress the contents of the web_static directory into the archive.
        print(f"Packing web_static to {archive_name}")
        local(f'tar -czvf {archive_name} web_static')

        # Check if the archive was created successfully.
        if os.path.isfile(archive_name):
            archive_size = os.stat(archive_name).st_size
            print(f"web_static packed: {archive_name} -> {archive_size} Bytes")
            return archive_name
        else:
            return None
    except OSError as e:
        print(f"Error: {e}")
        return None
