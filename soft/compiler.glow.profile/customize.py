#
# Collective Knowledge (individual environment - setup)
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

    env        = i['env']
    cus        = i.get('customize',{})
    env_prefix = cus.get('env_prefix','CK_ENV_')
    full_path  = cus.get('full_path','')

    env[env_prefix + '_PROFILE_DIR']  = os.path.dirname(full_path)
    env[env_prefix + '_PROFILE_YAML'] = full_path
    install_env = cus.get('install_env', '')
    is_aimet = install_env.get('_AIMET_MODEL')
    if is_aimet == 'yes':
       import yaml
       with open('profile.yaml') as file:
          encodings = yaml.load(file, Loader=yaml.FullLoader)
          node = encodings['activation_encodings']
          output1_node=node['325'][0]
          output1_scale = output1_node['scale']
          output1_offset = -output1_node['offset'] - 128
       env[env_prefix + '_NODE_PRECISION_FILE']  = os.path.dirname(full_path)+"/node-precision.yaml"
       env['CK_ENV_ONNX_MODEL_ONNX_FILEPATH'] = os.path.dirname(full_path)+"/ssd_resnet34_aimet.onnx"
       #env[env_prefix + '_OUTPUT1_SCALE']  = output1_scale
       #env[env_prefix + '_OUTPUT1_OFFSET']  = output1_offset
       env['CK_ENV_ABC_LOC_SCALE']  = output1_scale
       env['CK_ENV_ABC_LOC_OFFSET']  = output1_offset

    return {'return':0, 'bat':''}
