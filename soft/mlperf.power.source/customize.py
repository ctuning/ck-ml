#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#

import os


def setup(i):
    env_prefix = i["customize"]["env_prefix"]
    root_dir = os.path.dirname(os.path.dirname(i["customize"]["full_path"]))
    i["env"][env_prefix + "_ROOT"] = root_dir
    i["env"][env_prefix + "_CLIENT_SERVER_DIR"] = os.path.join(root_dir, "ptd_client_server")
    i["env"][env_prefix + "_CLIENT_PY"] = os.path.join(root_dir, "ptd_client_server", "client.py")
    i["env"][env_prefix + "_SERVER_PY"] = os.path.join(root_dir, "ptd_client_server", "server.py")
    return {"return": 0, "bat": ""}
