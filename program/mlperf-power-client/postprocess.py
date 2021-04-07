#!/usr/bin/env python3

import base64
import json
import os
import subprocess
import sys


def load_json(fname):
    with open(fname) as f:
        return json.load(f)


def load_lines(fname):
    with open(fname) as f:
        return list(map(lambda x: x.rstrip("\n\r"), f))


def load_raw(fname):
    with open(fname, "rb") as f:
        return base64.encodebytes(f.read()).decode("utf8")


def load_dir(basename, raw=False):
    result = {}
    for path, dirs, files in os.walk(basename, topdown=True):
        for file in files:
            p = os.path.join(path, file)
            if raw:
                r = load_raw(p)
            else:
                r = load_lines(p)
            result[os.path.relpath(p, basename)] = r
    result.pop("tmp-ck-timer.json", None)  # avoid self-containing
    return result


def main():
    result = {
        "power": {
            "client.json": load_json("power/client.json"),
            "client.log": load_lines("power/client.log"),
            "ptd_logs.txt": load_lines("power/ptd_logs.txt"),
            "server.json": load_json("power/server.json"),
            "server.log": load_lines("power/server.log"),
        },
        "ranging": load_dir("ranging"),
        "run_1": load_dir("run_1"),
        "raw": load_dir(".", True),
    }

    with open("tmp-ck-timer.json", "w") as f:
        json.dump(result, f, indent=2)


main()
