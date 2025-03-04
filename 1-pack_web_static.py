#!/usr/bin/python3
# Fabric script that generates a .tgz archive from the contents of the
# web_static
# folder of your AirBnB Clone repo, using the function do_pack..
import os.path
from datetime import datetime
from fabric.api import local


def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    datime = datetime.utcnow()
    archivo = "versions/web_static_{}{}{}{}{}{}.tgz".format(datime.year,
                                                            datime.month,
                                                            datime.day,
                                                            datime.hour,
                                                            datime.minute,
                                                            datime.second)
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(archivo)).failed is True:
        return None
    return archivo
