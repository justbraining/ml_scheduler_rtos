import pandas as pd

def priority_scheduler(task_df):
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
        # Get available tasks at current time that aren't done
        ready_tasks = task_df[
            (task_df['arrival_time'] <= time) & 
            (~task_df['is_completed'])
        ]

        if not ready_tasks.empty:
            # Pick task with highest priority (lowest number)
            next_task_index = ready_tasks['priority'].idxmin()
            task = task_df.loc[next_task_index]

            # Start and finish task
            task_df.at[next_task_index, 'start_time'] = time
            time += task['execution_time']
            task_df.at[next_task_index, 'completion_time'] = time
            task_df.at[next_task_index, 'is_completed'] = True

            # Check for deadline miss
            if time > task['deadline']:
                task_df.at[next_task_index, 'deadline_miss'] = True

            timeline.append((task['task_id'], time))
            completed_tasks += 1
        else:
            time += 1  # idle if no tasks available

    return task_df, timeline
