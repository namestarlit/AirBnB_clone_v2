#!/usr/bin/python3
# Fabfile to generates a .tgz archive from the contents of web_static.
import os.path
from datetime import datetime
from fabric.api import local


def do_pack():
    """Create a tar gzipped archive of the web_static folder."""
    dt = datetime.utcnow()
    file = "versions/web_static_{}{}{}{}{}{}.tgz".format(dt.year,
                                                         dt.month,
                                                         dt.day,
                                                         dt.hour,
                                                         dt.minute,
                                                         dt.second)
    if os.path.isdir("web_static") is False:
        print("Error: web_static folder not found.")
        return None

    if os.path.isdir("versions") is False:
        os.makedirs("versions")

    if local("tar -cvzf {} web_static".format(file)).failed is True:
        print("Error: Failed to create the archive.")
        return None

    print("Archive created: {}".format(file))
    return file
