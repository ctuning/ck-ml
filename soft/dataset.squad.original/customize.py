#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer(s):
# - Anton Lokhmotov, anton@dividiti.com
#

import os

##############################################################################
# setup environment setup

def setup(i):
    """
    Input:  {
              cfg              - meta of this soft entry
              self_cfg         - meta of module soft
              ck_kernel        - import CK kernel module (to reuse functions)

              host_os_uoa      - host OS UOA
              host_os_uid      - host OS UID
              host_os_dict     - host OS meta

              target_os_uoa    - target OS UOA
              target_os_uid    - target OS UID
              target_os_dict   - target OS meta

              target_device_id - target device ID (if via ADB)

              tags             - list of tags used to search this entry

              env              - updated environment vars from meta
              customize        - updated customize vars from meta

              deps             - resolved dependencies for this soft

              interactive      - if 'yes', can ask questions, otherwise quiet
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              bat          - prepared string for bat file
            }

    """

    import os

    s=''

    cus             = i.get('customize',{})
    env_prefix      = cus['env_prefix']
    full_path       = cus.get('full_path','')
    install_env     = cus.get('install_env', {})

    env             = i['env']
    env[env_prefix] = full_path

    for varname in install_env.keys():
        if varname.startswith('DATASET_'):
            env[env_prefix+varname[len('DATASET'):]] = install_env[varname]

    return {'return':0, 'bat':s}
