#! /usr/bin/env python
from typing import Dict, List, Any, Generator
from datetime import datetime as dt
from collections import deque
import multiprocessing as mp
import logging
import signal
import time
import math
import json
import pdb
import sys

import plotext as plt
import docker

log = logging.getLogger(__file__)

shared_memory_manager = mp.Manager()

client = docker.from_env()
data_queue = shared_memory_manager.Queue()


def start_container_collection(name):
    log.debug(f"starting stats for {name}...")
    container = client.containers.get(name)
    try:
        for data in container.stats(decode=True):
            data['time'] = time.time()
            data_queue.put(data)
    except (KeyboardInterrupt, SystemExit) as err:
        ...
    log.debug(f"finished retrieving stats for {name}")


def process_record(record: Dict) -> Generator[Dict, None, None]:
    def get_block_io_mb_stats() -> Dict:
        ret_val = {}
        for stat in record['blkio_stats']['io_service_bytes_recursive']:
            op = stat['op'].lower()
            if op in {'read', 'write'}:
                ret_val[f"block_io_mb_{op}"] = stat['value'] * 1e-6
        return ret_val


    def get_cpu_stats() -> Dict:
        current_cpu = record['cpu_stats']['cpu_usage']['total_usage']
        pre_cpu = record['precpu_stats']['cpu_usage']['total_usage']

        cpu_delta = float(current_cpu - pre_cpu) if pre_cpu > 0 else 0

        current_total = record['cpu_stats']['system_cpu_usage']
        pre_total = record['precpu_stats'].get('system_cpu_usage', 0)
        total_delta = float(current_total - pre_total) if pre_total > 0 else 0

        cpu_used = None
        if cpu_delta > 0 and total_delta > 0:
            cpu_used = round(cpu_delta / total_delta * 100, 4)

        cores_used = None
        current_cores_used = record['cpu_stats']['cpu_usage']['percpu_usage']
        pre_cores_used = record['precpu_stats']['cpu_usage'].get('percpu_usage', [])

        cores_used = None
        if len(current_cores_used) > 0 and len(pre_cores_used) > 0:
            cores_used = len([
                i for i, (curr, prev) 
                in enumerate(zip(current_cores_used, pre_cores_used))
                if curr - prev > 0
            ])

        return {"cpu_used": cpu_used, "cores_used": cores_used}

    def get_memory_used() -> Dict:
        mem_cache_mb = record['memory_stats']['stats']['cache'] * 1e-6
        mem_total_used_mb = record['memory_stats']['usage'] * 1e-6
        total_memory = record['memory_stats']['limit'] * 1e-6
        return {
            "mem_cache_mb": mem_cache_mb,
            "mem_total_used_mb": mem_total_used_mb,
            "mem_used_mb": mem_total_used_mb - mem_cache_mb,
            "mem_used_%": mem_total_used_mb / total_memory
        }

    def get_pids() -> Dict:
        return {
            "pids": float(record['pids_stats']['current'])
        }

    metadata = {
        "name": record['name'],
        "time": record['time'],
        "timestamp": record['read']
    }

    for metric, value in get_block_io_mb_stats().items():
        yield {**metadata, "metric": metric, "value": value}

    for metric, value in get_cpu_stats().items():
        yield {**metadata, "metric": metric, "value": value}

    for metric, value in get_memory_used().items():
        yield {**metadata, "metric": metric, "value": value}

    for metric, value in get_pids().items():
        yield {**metadata, "metric": metric, "value": value}

def stream_docker_stats(container_names: List[str]) -> Generator[Dict, None, None]:
    processes = [
        mp.Process(target=start_container_collection, args=(container_name,))
        for container_name in container_names
    ]
    try:
        for process in processes:
            process.start()

        while True:
            record = data_queue.get()
            yield from process_record(record)
    except (KeyboardInterrupt, SystemExit) as err:
        ...
    except Exception as err:
        log.exception(err)
    finally:
        for process in processes:
            process.terminate()


def get_all_containers():
    return tuple(
        container.name
        for container in client.containers.list()
    )


if __name__ == '__main__':

    stats_stream = stream_docker_stats(get_all_containers())

    for record in stats_stream:
        print(record)
