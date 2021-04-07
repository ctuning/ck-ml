import argparse
import sys
import json
import copy

def parse_args():
    parser = argparse.ArgumentParser(description='Gen BERT calibration dataset.')
    parser.add_argument('-f', '--full', type=str, help="Full dataset")
    parser.add_argument('-l', '--list', type=str, help="Calibration set list")
    parser.add_argument('-o', '--out', type=str, help="Calibration dataset to output")

    return parser.parse_args()


def main(args):

    with open(args.full) as json_file:
        data = json.load(json_file)

    with open(args.list) as list_file:
        lines = list_file.readlines()


    for i in range(len(lines)):
        lines[i] = int(lines[i])

    lines.sort()

    data_out = copy.deepcopy(data)

    counter = 0
    for e, entry in enumerate(data['data']):
        for p, para in enumerate(entry['paragraphs']):
            data_out['data'][e]['paragraphs'][p]['qas']=[]
            for q, qas in enumerate(para['qas']):
                if counter in lines:
                    data_out['data'][e]['paragraphs'][p]['qas'].append(qas)
                counter += 1

    with open(args.out, 'w') as outfile:
        json.dump(data_out, outfile)

if __name__ == "__main__":
    args = parse_args()

    main(args)

