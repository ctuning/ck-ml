#!/usr/bin/env python3

import json
import math
import os
import pickle
import subprocess
import sys
import numpy as np
import onnxruntime

BERT_CODE_ROOT=os.environ['CK_ENV_MLPERF_INFERENCE']+'/language/bert'

sys.path.insert(0, BERT_CODE_ROOT)
sys.path.insert(0, BERT_CODE_ROOT + '/DeepLearningExamples/TensorFlow/LanguageModeling/BERT')


## SQuAD dataset - original and tokenized
#
SQUAD_DATASET_ORIGINAL_PATH     = os.environ['CK_ENV_DATASET_SQUAD_ORIGINAL']
SQUAD_DATASET_TOKENIZED_PATH    = os.environ['CK_ENV_DATASET_SQUAD_TOKENIZED']

## BERT model:
#
BERT_MODEL_PATH                 = os.environ['CK_ENV_ONNX_MODEL_ONNX_FILEPATH']

## Processing by batches:
#
BATCH_SIZE                      = int(os.getenv('CK_BATCH_SIZE', 1))
BATCH_COUNT                     = int(os.getenv('CK_BATCH_COUNT', 1))


sess_options = onnxruntime.SessionOptions()
print("Loading BERT model and weights from {} ...".format(BERT_MODEL_PATH))
sess = onnxruntime.InferenceSession(BERT_MODEL_PATH, sess_options)


print("Loading tokenized SQuAD dataset as features from {} ...".format(SQUAD_DATASET_TOKENIZED_PATH))
with open(SQUAD_DATASET_TOKENIZED_PATH, 'rb') as tokenized_features_file:
    eval_features = pickle.load(tokenized_features_file)

print("Example width: {}".format(len(eval_features[0].input_ids)))

TOTAL_EXAMPLES  = len(eval_features)
print("Total examples available: {}".format(TOTAL_EXAMPLES))
if BATCH_COUNT<1:
    BATCH_COUNT = math.ceil(TOTAL_EXAMPLES/BATCH_SIZE)
    selected_size = TOTAL_EXAMPLES
else:
    selected_size = BATCH_COUNT * BATCH_SIZE

encoded_accuracy_log = []
for batch_index in range(BATCH_COUNT):

    if (batch_index+1)*BATCH_SIZE <= TOTAL_EXAMPLES:    # regular batch
        this_batch_size = BATCH_SIZE
    else:
        this_batch_size = TOTAL_EXAMPLES % BATCH_SIZE   # last incomplete batch of a full dataset run

    input_ids_stack     = []
    input_mask_stack    = []
    segment_ids_stack   = []

    for index_in_batch in range(this_batch_size):
        global_index = batch_index * BATCH_SIZE + index_in_batch
        selected_feature = eval_features[global_index]

        input_ids_stack.append( np.array(selected_feature.input_ids) )
        input_mask_stack.append( np.array(selected_feature.input_mask) )
        segment_ids_stack.append( np.array(selected_feature.segment_ids) )

    batch_input_dict = {
        "input_ids":    np.stack( input_ids_stack ).astype(np.int64),
        "input_mask":   np.stack( input_mask_stack ).astype(np.int64),
        "segment_ids":  np.stack( segment_ids_stack ).astype(np.int64),
    }
    scores = sess.run([o.name for o in sess.get_outputs()], batch_input_dict)

    batch_output = np.stack(scores, axis=-1)

    for index_in_batch in range(this_batch_size):
        global_index = batch_index * BATCH_SIZE + index_in_batch
        encoded_accuracy_log.append({'qsl_idx': global_index, 'data': batch_output[index_in_batch].tobytes().hex()})

    print("Batch[{}] #{}/{} done".format(this_batch_size, batch_index+1, BATCH_COUNT))


with open('accuracy_log.json', 'w') as accuracy_log_file:
    json.dump(encoded_accuracy_log, accuracy_log_file)

cmd = "python3 "+BERT_CODE_ROOT+"/accuracy-squad.py --val_data={} --features_cache_file={} --log_file=accuracy_log.json --out_file=predictions.json --max_examples={}".format(SQUAD_DATASET_ORIGINAL_PATH, SQUAD_DATASET_TOKENIZED_PATH, selected_size)
subprocess.check_call(cmd, shell=True)
