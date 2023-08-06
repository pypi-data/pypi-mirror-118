from typing import List
import plotext as plt
import pandas as pd

def plot(df: pd.DataFrame, ordered_keys: List[str], max_rows: int, max_cols: int):
    trimmed_keys = ordered_keys[:max_rows * max_cols]

    plot_positions = [
        (row, col)
        for row in range(1, max_rows + 1)
        for col in range(1, max_cols + 1)
    ]

    key_to_position = dict(zip(trimmed_keys, plot_positions))

    plt.clp()

    plt.subplots(max_rows, max_cols)
    plt.colorless()

    plots_used = []

    for metric in trimmed_keys: 
        data = df[df.metric == metric]
        row, column = key_to_position[metric]
        plots_used.append((row, column))
        plt.subplot(row, column)
        plt.colorless()
        should_legend = bool(row == 1 and column == 1)
        plt.title(metric)
        max_y = 0
        min_y = None

        for name, group_by_name_with_nans in data.groupby('name'):
            group = group_by_name_with_nans.dropna()
            if len(group) > 0:
                max_y = max(group.value.max() * 2.0, max_y)
                min_y = min(group.value.min(), min_y) if min_y else group.value.min()
                plt.plot(
                    group.time.tolist(),
                    group.value.tolist(),
                    label=name if should_legend else None
                )

                plt.xticks(
                    group.time.tolist(),
                    [dt.time().strftime("%H:%M:%S") for dt in group.timestamp.tolist()]
                )
                plt.xlabel('time')

        if max_y > 0.0 and should_legend:
            plt.ylim(min_y, max_y)

    for row, column in set(plot_positions) - set(plots_used):
        plt.subplot(row, column)
        plt.colorless()

    plt.show()


