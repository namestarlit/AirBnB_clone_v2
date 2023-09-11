#!/usr/bin/python3
"""Distribute an archive to web servers using Fabric."""

import os
from fabric.api import env, put, run


env.user = 'ubuntu'
env.hosts = ['54.158.187.197', '100.25.188.196']
env.warn_only = True


def do_deploy(archive_path):
    """Distribute an archive to web servers."""
    if not os.path.isfile(archive_path):
        return False

    try:
        # Upload the archive to the '/tmp/' directory on the web servers
        put(archive_path, '/tmp/')

        # Extract the archive to the releases directory
        archive_filename = os.path.basename(archive_path)
        release_name = os.path.splitext(archive_filename)[0]
        release_path = '/data/web_static/releases'

        run(f'mkdir -p {release_path}/{release_name}/')
        run('tar -xzf /tmp/{} -C {}/{}/'
            .format(archive_filename, release_path, release_name))

        # Delete the archive from the web servers
        run(f'rm /tmp/{archive_filename}')

        # Move web_static files to web_static current version directory
        move_command = (f'mv {release_path}/{release_name}/web_static/* '
                        f'{release_path}/{release_name}/')
        run(move_command)
        run(f'rm -rf {release_path}/{release_name}/web_static')

        # Delete the symbolic link '/data/web_static/current' if exists
        current_symlink = '/data/web_static/current'
        run(f'rm -rf {current_symlink}')

        # Create a new symbolic link to the new version
        new_symlink = f'{release_path}/{release_name}'
        run(f'ln -s {new_symlink} {current_symlink}')

        print("New version deployed!")
        return True
    except Exception:
        return False
