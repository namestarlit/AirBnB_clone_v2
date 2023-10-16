#!/usr/bin/python3
"""1-pack_web_static module"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """Generates .tgz archive from web_static dir
    Returns: Archive path, otherwise False
    """
    fmt = datetime.now().strftime("%Y%m%d%H%M%S")

    local("mkdir -p versions")
    local("tar -cvzf versions/web_static_{}.tgz web_static".format(fmt))

    try:
        return ("versions/web_static_{}.tgz".format(fmt))
    except Exception:
        return None
