import pandas as pd

def linux_rr_scheduler(task_df, time_quantum=2):
    task_df = task_df.sort_values(by='arrival_time').reset_index(drop=True)
    time = 0
    timeline = []
    completed = 0
    n = len(task_df)

    task_df['remaining_time'] = task_df['execution_time']
    task_df['start_time'] = -1
    task_df['completion_time'] = -1
    task_df['is_completed'] = False
    task_df['deadline_miss'] = False

    while completed < n:
        progress = False
        for idx, task in task_df.iterrows():
            if task['arrival_time'] <= time and not task['is_completed']:
                if task_df.at[idx, 'start_time'] == -1:
                    task_df.at[idx, 'start_time'] = time

                exec_time = min(time_quantum, task_df.at[idx, 'remaining_time'])
                time += exec_time
                task_df.at[idx, 'remaining_time'] -= exec_time

                if task_df.at[idx, 'remaining_time'] == 0:
                    task_df.at[idx, 'completion_time'] = time
                    task_df.at[idx, 'is_completed'] = True
                    task_df.at[idx, 'deadline_miss'] = time > task['deadline']
                    completed += 1

                timeline.append((task['task_id'], time))
                progress = True
        if not progress:
            time += 1  # idle time

    return task_df, timeline
