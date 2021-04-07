#!/usr/bin/env python3

import argparse
import ck.kernel as ck
import json
import math
import os.path
import sys


def ck_access(**kwargs):
    r = ck.access(kwargs)
    if r["return"] > 0:
        print("Error: %s" % r["error"])
        exit(1)
    return r


def parse_ck_tags(tags):
    result = {}
    for tag in tags:
        if "." in tag:
            key, value = tag.split(".", 1)
            result[key] = value
        else:
            result[tag] = None
    return result


def parse_mlperf_log_detail(lines):
    PREFIX = ":::MLLOG "
    result = {}
    for line in lines:
        if not line.startswith(PREFIX):
            continue
        line = json.loads(line[len(PREFIX) :])
        if "key" in line and "value" in line:
            result[line["key"]] = line["value"]
    return result


def main(args):
    experiments = ck_access(
        repo_uoa=args.repo_uoa,
        action="search",
        module_uoa="experiment",
        tags="mlperf,scenario.range_singlestream"
        + ("," + args.tags if args.tags else ""),
    )["lst"]

    for experiment in experiments:
        pipeline = ck_access(
            action="load_pipeline",
            repo_uoa=experiment["repo_uoa"],
            module_uoa=experiment["module_uoa"],
            data_uoa=experiment["data_uoa"],
        )["pipeline"]

        points = ck_access(
            action="list_points",
            repo_uoa=experiment["repo_uoa"],
            module_uoa=experiment["module_uoa"],
            data_uoa=experiment["data_uoa"],
        )

        tags = parse_ck_tags(points["dict"]["tags"])
        library_backend = (
            tags["inference_engine"]
            + "-"
            + tags["inference_engine_version"]
            + (
                ("-" + tags["inference_engine_backend"])
                if "inference_engine_backend" in tags
                else ""
            )
        )

        for point in points["points"]:
            point_file_path = os.path.join(points["path"], "ckp-%s.0001.json" % point)
            with open(point_file_path) as point_file:
                point_data_raw = json.load(point_file)

            for characteristic in point_data_raw["characteristics_list"]:
                detail = parse_mlperf_log_detail(
                    characteristic["run"]["mlperf_log"]["detail"]
                )
                latency_ms = math.ceil(detail["result_mean_latency_ns"] / 10 ** 6)

                print(
                    "{:35} {:-4} # max_query_count={}".format(
                        tags["platform"]
                        + ","
                        + library_backend
                        + ","
                        + tags["workload"],
                        latency_ms,
                        tags["max_query_count"],
                    ),
                    file=args.out,
                )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-uoa",
        metavar="REPO_UOA",
        type=str,
        default="local",
        help="defaults to 'local'",
    )
    parser.add_argument(
        "--tags",
        metavar="TAGS",
        type=str,
        default="",
    )
    parser.add_argument(
        "--out",
        metavar="FILE",
        type=argparse.FileType("w"),
        default=sys.stdout,
    )
    main(parser.parse_args())
