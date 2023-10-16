#!/usr/bin/python3
"""100-clean_web_static module"""
from datetime import datetime
from fabric.api import *
from os.path import isfile

prv_ky_pth = "~/.ssh/school"
env.user = ['ubuntu']
env.hosts = ["ubuntu@18.204.16.34", "ubuntu@100.26.246.77"]
env.key_filename = prv_ky_pth


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


def deploy():
    """Creates & distributes an archive to your web servers
    Returns: Value of do_deploy, False if no archive created
    """
    achv_pth = do_pack()
    if achv_pth is None:
        return False
    return do_deploy(achv_pth)


def do_clean(number=0):
    """Deletes out-of-date archives
    number: no. of the archives to keep
    """
    files = local("ls -1t versions", capture=True)
    file_names = files.split("\n")
    n = int(number)
    if n in (0, 1):
        n = 1
    for i in file_names[n:]:
        local("rm versions/{}".format(i))
    dir_wbsvr = run("ls -1t /data/web_static/releases")
    dir_wbsvr_nms = dir_wbsvr.split("\n")
    for i in dir_wbsvr_nms[n:]:
        if i is 'test':
            continue
        run("rm -rf /data/web_static/releases/{}".format(i))
