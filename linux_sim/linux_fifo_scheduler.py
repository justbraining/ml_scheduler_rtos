import pandas as pd

def linux_fifo_scheduler(task_df):
    task_df = task_df.sort_values(by='arrival_time').reset_index(drop=True)
    time = 0
    timeline = []
    completed = 0
    total = len(task_df)

    task_df['start_time'] = -1
    task_df['completion_time'] = -1
    task_df['is_completed'] = False
    task_df['deadline_miss'] = False

    while completed < total:
        ready = task_df[
            (task_df['arrival_time'] <= time) &
            (~task_df['is_completed'])
        ]

        if not ready.empty:
            # Select task with highest static priority (lower number = higher priority)
            next_task_index = ready['priority'].idxmin()
            task = task_df.loc[next_task_index]

            task_df.at[next_task_index, 'start_time'] = time
            time += task['execution_time']
            task_df.at[next_task_index, 'completion_time'] = time
            task_df.at[next_task_index, 'is_completed'] = True
            task_df.at[next_task_index, 'deadline_miss'] = time > task['deadline']

            timeline.append((task['task_id'], time))
            completed += 1
        else:
            time += 1  # CPU idle

    return task_df, timeline
