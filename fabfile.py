from fabric import task
from datetime import datetime
import os
import shutil

@task
def do_pack():
    """Create a tar gzipped archive of the web_static folder."""
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    archive_name = f"web_static_{timestamp}.tgz"
    archive_path = f"versions/{archive_name}"

    # Create the versions directory if it doesn't exist
    os.makedirs("versions", exist_ok=True)

    try:
        shutil.make_archive("web_static", "gztar", "web_static")
        shutil.move("web_static.tar.gz", archive_path)
        print(f"Archive created: {archive_path}")
        return archive_path
    except Exception as e:
        print(f"Error creating archive: {e}")
        return None

