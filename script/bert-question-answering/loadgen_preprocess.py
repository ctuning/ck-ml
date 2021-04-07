#
# Copyright (c) 2018 cTuning foundation.
# See CK COPYRIGHT.txt for copyright details.
#
# SPDX-License-Identifier: BSD-3-Clause.
# See CK LICENSE.txt for licensing details.
#

import os
from shutil import copy2


def user_conf_and_audit_config(i):

    def dep_env(dep, var): return i['deps'][dep]['dict']['env'].get(var)
    deps=i['deps']
    env=i['env']

    # Try ML_MODEL_MODEL_NAME from the environment, then from the 'weights' model dependency, then try to find MODEL_NAME of its 'model-source' dependency:
    model_name = env.get('ML_MODEL_MODEL_NAME') or dep_env('model', 'ML_MODEL_MODEL_NAME')
    print('\n-=-=-=-=-= Generating user.conf for model "{}" ...'.format(model_name))
    scenario            = env['CK_LOADGEN_SCENARIO']
    user_conf_rel_path  = env['CK_LOADGEN_USER_CONF']
    user_conf           = []
    env_to_conf         = {
        'CK_LOADGEN_MULTISTREAMNESS':                   ('samples_per_query', 1),

        'CK_LOADGEN_MIN_QUERY_COUNT':                   ('min_query_count', 1),
        'CK_LOADGEN_MAX_QUERY_COUNT':                   ('max_query_count', 1),
        'CK_LOADGEN_BUFFER_SIZE':                       ('performance_sample_count_override', 1),
        'CK_LOADGEN_SAMPLES_PER_QUERY':                 ('samples_per_query', 1),
        'CK_LOADGEN_TARGET_LATENCY':                    ('target_latency', 1),
        'CK_LOADGEN_TARGET_QPS':                        ('target_qps', 1),

        'CK_LOADGEN_MAX_DURATION_S':                    ('max_duration_ms', 1000),
        'CK_LOADGEN_OFFLINE_EXPECTED_QPS':              ('offline_expected_qps', 1),
    }
    for env_key in env_to_conf.keys():
        if env_key in env:
            orig_value = env[env_key]
            if orig_value!="":
                (config_category_name, multiplier) = env_to_conf[env_key]
                new_value = orig_value if multiplier==1 else float(orig_value)*multiplier
                user_conf.append("{}.{}.{} = {}\n".format(model_name, scenario, config_category_name, new_value))

    # Write 'user.conf' into the current directory ('tmp').
    user_conf_abs_path = os.path.join(os.path.abspath(os.path.curdir), user_conf_rel_path)
    with open(user_conf_abs_path, 'w') as user_conf_file:
         user_conf_file.writelines(user_conf)

    # Copy 'audit.config' for compliance testing into the current directory ('tmp').
    compliance_test_config = 'audit.config'
    compliance_test = env.get('CK_MLPERF_COMPLIANCE_TEST','')
    compliance_test_config_target_path = os.path.join(os.path.abspath(os.path.curdir), compliance_test_config)
    if compliance_test != '':
        inference_root = dep_env('mlperf-inference-src', 'CK_ENV_MLPERF_INFERENCE')
        if inference_root != '':
            if compliance_test in [ 'TEST01', 'TEST04-A', 'TEST04-B', 'TEST05' ]:
                compliance_test_source_dir = os.path.join(inference_root, 'compliance', 'nvidia', compliance_test)
                if compliance_test in [ 'TEST01' ]: compliance_test_source_dir = os.path.join(compliance_test_source_dir, model_name)
                compliance_test_config_source_path = os.path.join(compliance_test_source_dir, compliance_test_config)
                copy2(compliance_test_config_source_path, compliance_test_config_target_path)
            else:
                raise Exception("Error: Unsupported compliance test: '{}'".format(compliance_test))
        else:
                raise Exception("Error: the environment variable CK_ENV_MLPERF_INFERENCE necessary to run compliance tests is empty")
    elif os.path.isfile(compliance_test_config_target_path):
        print("Not in compliance test mode - deleting the file '{}'".format(compliance_test_config_target_path))
        os.remove(compliance_test_config_target_path)

    print('=-=-=-=-=- done.\n')

    return {'return':0}


def ck_preprocess(i):
    return user_conf_and_audit_config(i)

# Do not add anything here!
