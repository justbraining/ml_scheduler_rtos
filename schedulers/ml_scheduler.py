
import pandas as pd
import joblib


def ml_scheduler(task_df, model_path="data/model.pkl"):
    model = joblib.load(model_path)
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
        ready_tasks = task_df[
            (task_df['arrival_time'] <= time) &
            (~task_df['is_completed'])
        ]

        if not ready_tasks.empty:
            predictions = []

            for _, task in ready_tasks.iterrows():
                # Prepare named feature DataFrame to silence warnings
                input_df = pd.DataFrame([{
                    "arrival_time": task['arrival_time'],
                    "execution_time": task['execution_time'],
                    "deadline": task['deadline'],
                    "priority": task['priority'],
                    "task_type": 1 if task['task_type'] == 'CPU' else 0
                }])

                predicted_wait = model.predict(input_df)[0]
                predictions.append((task['task_id'], predicted_wait))

            # Pick task with lowest predicted wait time
            best_task_id = min(predictions, key=lambda x: x[1])[0]
            task_index = task_df.index[task_df['task_id'] == best_task_id][0]
            task = task_df.loc[task_index]

            task_df.at[task_index, 'start_time'] = time
            time += task['execution_time']
            task_df.at[task_index, 'completion_time'] = time
            task_df.at[task_index, 'is_completed'] = True
            task_df.at[task_index, 'deadline_miss'] = time > task['deadline']

            timeline.append((task['task_id'], time))
            completed_tasks += 1
        else:
            time += 1  # System idle

    return task_df, timeline
