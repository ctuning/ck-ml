#!/usr/bin/env bash

set -e

die() {
	echo "$*"
	exit 1
}

[ "$CK_MLPERF_POWER_CLIENT_ADDRESS" ] || die "CK_MLPERF_POWER_CLIENT_ADDRESS empty"
[ "$CK_MLPERF_POWER_CLIENT_LOADGEN_LOGS" ] || die "CK_MLPERF_POWER_CLIENT_LOADGEN_LOGS empty"

[ "${PWD##*/}" = tmp ] || die "not in tmp?"
rm -rf "$PWD"/*

"$CK_ENV_COMPILER_PYTHON_FILE" \
    "$CK_ENV_MLPERF_POWER_CLIENT_PY" \
    --run-workload "$CK_MLPERF_POWER_CLIENT_WORKLOAD" \
    --addr "$CK_MLPERF_POWER_CLIENT_ADDRESS" \
    --port "$CK_MLPERF_POWER_CLIENT_PORT" \
    --label "$CK_MLPERF_POWER_CLIENT_LABEL" \
    --ntp "$CK_MLPERF_POWER_CLIENT_NTP" \
    --loadgen-logs "$CK_MLPERF_POWER_CLIENT_LOADGEN_LOGS" \
    --output "$PWD" \
    --fetch-logs \
    --force

# Move tmp/2021-02-19_16-50-28/* into tmp/*
A=( ./* )
mv "${A[0]}/"* .
rmdir "${A[0]}"
