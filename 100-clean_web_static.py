#!/usr/bin/python3
"""Deletes out-of-date archives on web servers using Fabric."""

import os
from fabric.api import cd, env, local, run


env.user = 'ubuntu'
env.hosts = ['54.158.187.197', '100.25.188.196']
env.warn_only = True


def do_clean(number=0):
    """Deletes out-of-date archives."""
    try:
        number = int(number)
        if number < 1:
            number = 1

        # Ensure we have at least 'number' to keep
        number_to_keep = max(number, 1)

        # Delete local archives (this is a local command)
        local('ls -t versions | tail -n +{} | '
              'xargs -I {{}} rm -rf versions/{{}}'.format(number_to_keep + 1))

        # List all archives in '/data/web_static/releases' directory (remote)
        releases_path = '/data/web_static/releases'
        with cd(releases_path):
            archives = run('ls -t').split()

        # Delete archives in '/data/web_static/releases' (remote)
        for archive in archives[number_to_keep:]:
            run('rm -rf {}'
                .format(os.path.join(releases_path, archive)))

        print('Archives deleted successfully')
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
