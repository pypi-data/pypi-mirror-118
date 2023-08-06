import pandas as pd
import numpy as np
import argparse
import math

from docker_load_graph import docker_helper as d
from docker_load_graph import plotting

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--rows", type=int, default=3)
    p.add_argument("--cols", type=int, default=2)
    args = p.parse_args()

    max_rows = args.rows
    max_cols = args.cols

    ordered_valid_keys = [
        'block_io_mb_write',
        'block_io_mb_read',
        'mem_used_mb',
        'cpu_used',
        'cores_used',
        'pids',
        'mem_used_%',
        'mem_cache_mb',
        'mem_total_used_mb',
    ]

    df = pd.DataFrame()
    try:
        for record in d.stream_docker_stats(d.get_all_containers()):
            record['timestamp'] = pd.to_datetime(record['timestamp'])
            df = df.append(record, ignore_index=True)
            plotting.plot(
                df, 
                ordered_keys=ordered_valid_keys, 
                max_rows=max_rows,
                max_cols=max_cols
            )
    except KeyboardInterrupt as err:
        ...

if __name__ == '__main__':
    main()
