#!/usr/bin/python3
"""2-do_deploy_web_static.py module"""
from fabric.api import *
from os.path import isfile

prv_ky_pth = "~/.ssh/school"
env.user = ['ubuntu']
env.hosts = ["ubuntu@18.204.16.34", "ubuntu@100.26.246.77"]
env.key_filename = prv_ky_pth


def do_deploy(archive_path):
    """Distributes an archive to your web servers
    archive_path: Path to archive
    Returns: True if all operations done sucessful, otherwise False
    """
    if isfile(archive_path) is False:
        return False

    achv_tgz = archive_path.split('/')[1]
    achv = archive_path.split('/')[1].split('.')[0]

    try:
        put(archive_path, "/tmp/")
        run("mkdir -p /data/web_static/releases/{}/".
            format(achv))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
            format(achv_tgz, achv))
        run("rm /tmp/{}".format(achv_tgz))
        run("mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/".format(achv, achv))
        run("rm -rf /data/web_static/releases/{}/web_static".
            format(achv))
        run("rm -rf /data/web_static/current")
        run("ln -sf /data/web_static/releases/{}/ \
            /data/web_static/current".format(achv))
        print("New version deployed!")
        return True
    except Exception:
        return False
