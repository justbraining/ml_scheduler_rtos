import pandas as pd
from collections import deque

def round_robin_scheduler(task_df, time_quantum=2):
    task_df = task_df.sort_values(by='arrival_time').reset_index(drop=True)
    queue = deque()
    time = 0
    timeline = []
    task_df['remaining_time'] = task_df['execution_time']
    task_df['start_time'] = -1
    task_df['completion_time'] = -1
    task_df['deadline_miss'] = False

    arrived = 0
    completed_tasks = 0
    total_tasks = len(task_df)

    while completed_tasks < total_tasks:
        # Enqueue newly arrived tasks
        while arrived < total_tasks and task_df.loc[arrived, 'arrival_time'] <= time:
            queue.append(task_df.loc[arrived, 'task_id'])
            arrived += 1

        if queue:
            current_task_id = queue.popleft()
            task_index = task_df.index[task_df['task_id'] == current_task_id][0]

            if task_df.loc[task_index, 'start_time'] == -1:
                task_df.loc[task_index, 'start_time'] = time

            exec_time = min(time_quantum, task_df.loc[task_index, 'remaining_time'])
            time += exec_time
            task_df.loc[task_index, 'remaining_time'] -= exec_time
            timeline.append((current_task_id, time))

            if task_df.loc[task_index, 'remaining_time'] == 0:
                task_df.loc[task_index, 'completion_time'] = time
                if time > task_df.loc[task_index, 'deadline']:
                    task_df.loc[task_index, 'deadline_miss'] = True
                completed_tasks += 1
            else:
                queue.append(current_task_id)
        else:
            time += 1  # idle cycle

    return task_df, timeline
