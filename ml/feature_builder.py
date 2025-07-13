import pandas as pd

def build_training_data(task_df, scheduler_name):
    data = []

    for _, row in task_df.iterrows():
        data.append({
            "arrival_time": row["arrival_time"],
            "execution_time": row["execution_time"],
            "deadline": row["deadline"],
            "priority": row["priority"],
            "task_type": 1 if row["task_type"] == "CPU" else 0,  # Encode
            "start_time": row["start_time"],
            "completion_time": row["completion_time"],
            "wait_time": row["start_time"] - row["arrival_time"],
            "scheduled_by": scheduler_name
        })

    df = pd.DataFrame(data)
    return df
