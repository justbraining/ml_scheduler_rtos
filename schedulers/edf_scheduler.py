import pandas as pd

def edf_scheduler(task_df):
    task_df = task_df.sort_values(by='arrival_time').reset_index(drop=True)
    time = 0
    timeline = []
    completed_tasks = 0
    total_tasks = len(task_df)

    task_df['start_time'] = -1
    task_df['completion_time'] = -1
    task_df['is_completed'] = False
    task_df['deadline_miss'] = False

    while completed_tasks < total_tasks:
        # Get tasks that have arrived and are not yet completed
        ready_tasks = task_df[
            (task_df['arrival_time'] <= time) &
            (~task_df['is_completed'])
        ]

        if not ready_tasks.empty:
            # Choose task with earliest deadline
            next_task_index = ready_tasks['deadline'].idxmin()
            task = task_df.loc[next_task_index]

            task_df.at[next_task_index, 'start_time'] = time
            time += task['execution_time']
            task_df.at[next_task_index, 'completion_time'] = time
            task_df.at[next_task_index, 'is_completed'] = True

            if time > task['deadline']:
                task_df.at[next_task_index, 'deadline_miss'] = True

            timeline.append((task['task_id'], time))
            completed_tasks += 1
        else:
            time += 1  # No task ready → system idle

    return task_df, timeline
