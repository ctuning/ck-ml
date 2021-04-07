#!/usr/bin/env python3

import json
import os
import pickle
import subprocess
import sys

BERT_CODE_ROOT=os.environ['CK_ENV_MLPERF_INFERENCE']+'/language/bert'

sys.path.insert(0, BERT_CODE_ROOT)
sys.path.insert(0, BERT_CODE_ROOT + '/DeepLearningExamples/TensorFlow/LanguageModeling/BERT')

import numpy as np
import torch
from transformers import BertConfig, BertForQuestionAnswering

## SQuAD dataset - original and tokenized
#
SQUAD_DATASET_ORIGINAL_PATH     = os.environ['CK_ENV_DATASET_SQUAD_ORIGINAL']
SQUAD_DATASET_TOKENIZED_PATH    = os.environ['CK_ENV_DATASET_SQUAD_TOKENIZED']

## Model config and weights:
#
BERT_MODEL_HUB_NAME             = os.getenv('CK_BERT_MODEL_HUB_NAME')
BERT_MODEL_CONFIG_PATH          = BERT_CODE_ROOT + '/bert_config.json'
BERT_MODEL_WEIGHTS_PATH         = os.getenv('CK_ENV_MODEL_PYTORCH_FILEPATH')    # only available if BERT_MODEL_HUB_NAME is empty

IO_DUMP_PATH                    = os.getenv('CK_IO_DUMP_PATH')

## Enabling GPU if available and not disabled:
#
USE_CUDA                = torch.cuda.is_available() and (os.getenv('CK_DISABLE_CUDA', '0') in ('NO', 'no', 'OFF', 'off', '0'))
TORCH_DEVICE            = 'cuda:0' if USE_CUDA else 'cpu'

print("Torch execution device: "+TORCH_DEVICE)


if BERT_MODEL_HUB_NAME:
    print("Loading BERT model {} from the hub ...".format(BERT_MODEL_HUB_NAME))
    model = BertForQuestionAnswering.from_pretrained(BERT_MODEL_HUB_NAME)
    bert_config_obj = model.config
    model.eval()
    model.to(TORCH_DEVICE)
else:
    print("Loading BERT config from {} ...".format(BERT_MODEL_CONFIG_PATH))
    with open(BERT_MODEL_CONFIG_PATH) as bert_config_file:
        bert_config_dict = json.load(bert_config_file)
        bert_config_obj = BertConfig( **bert_config_dict )

    model = BertForQuestionAnswering(bert_config_obj)
    model.eval()
    model.to(TORCH_DEVICE)
    print("Loading BERT model weights from {} ...".format(BERT_MODEL_WEIGHTS_PATH))
    model.load_state_dict(torch.load(BERT_MODEL_WEIGHTS_PATH))

print("Vocabulary size: {}".format(bert_config_obj.vocab_size))

print("Loading tokenized SQuAD dataset as features from {} ...".format(SQUAD_DATASET_TOKENIZED_PATH))
with open(SQUAD_DATASET_TOKENIZED_PATH, 'rb') as tokenized_features_file:
    eval_features = pickle.load(tokenized_features_file)

print("Example width: {}".format(len(eval_features[0].input_ids)))

TOTAL_EXAMPLES  = len(eval_features)
print("Total examples available: {}".format(TOTAL_EXAMPLES))

## Processing by batches:
#
BATCH_COUNT             = int(os.getenv('CK_BATCH_COUNT')) or TOTAL_EXAMPLES


encoded_accuracy_log    = []
io_dump_structure       = {}
with torch.no_grad():
    for i in range(BATCH_COUNT):
        selected_feature = eval_features[i]

        start_scores, end_scores = model.forward(input_ids=torch.LongTensor(selected_feature.input_ids).unsqueeze(0).to(TORCH_DEVICE),
            attention_mask=torch.LongTensor(selected_feature.input_mask).unsqueeze(0).to(TORCH_DEVICE),
            token_type_ids=torch.LongTensor(selected_feature.segment_ids).unsqueeze(0).to(TORCH_DEVICE))
        output = torch.stack([start_scores, end_scores], axis=-1).squeeze(0).cpu().numpy()

        encoded_accuracy_log.append({'qsl_idx': i, 'data': output.tobytes().hex()})
        print("Batch #{}/{} done".format(i+1, BATCH_COUNT))

        if IO_DUMP_PATH:
            io_dump_structure[f'sample_{i+1}'] = {
                'input_ids':        selected_feature.input_ids,
                'attention_mask':   selected_feature.input_mask,
                'token_type_ids':   selected_feature.segment_ids,
                'start_scores':     start_scores.tolist(),
                'end_scores':       end_scores.tolist(),
            }

with open('accuracy_log.json', 'w') as accuracy_log_file:
    json.dump(encoded_accuracy_log, accuracy_log_file)

if IO_DUMP_PATH:
    with open(IO_DUMP_PATH, 'w') as io_dump_file:
        json.dump(io_dump_structure, io_dump_file, indent=4)
    print(f"I/O dump stored in {IO_DUMP_PATH}")

cmd = "python3 "+BERT_CODE_ROOT+"/accuracy-squad.py --val_data={} --features_cache_file={} --log_file=accuracy_log.json --out_file=predictions.json --max_examples={}".format(SQUAD_DATASET_ORIGINAL_PATH, SQUAD_DATASET_TOKENIZED_PATH, BATCH_COUNT)
subprocess.check_call(cmd, shell=True)
