#!/usr/bin/python3
"""Creates and distributes an archieve to web servers using Fabric."""

import os

try:
    do_pack = __import__('1-pack_web_static').do_pack
    do_deploy = __import__('2-do_deploy_web_static').do_deploy
except ImportError as e:
    print(f"Error: {e}")


def deploy():
    """Create and distribute an archive to web servers."""
    # Create archive file
    try:
        archive_path = do_pack()
        if not os.path.isfile(archive_path):
            return False
        return do_deploy(archive_path)
    except Exception:
        return False
