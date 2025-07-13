def calculate_metrics(df):
    df['waiting_time'] = df['start_time'] - df['arrival_time']
    df['turnaround_time'] = df['completion_time'] - df['arrival_time']

    avg_waiting_time = df['waiting_time'].mean()
    avg_turnaround_time = df['turnaround_time'].mean()
    deadline_misses = df['deadline_miss'].sum()
    total_tasks = len(df)

    results = {
        "Average Waiting Time": round(avg_waiting_time, 2),
        "Average Turnaround Time": round(avg_turnaround_time, 2),
        "Deadline Misses": int(deadline_misses),
        "Total Tasks": total_tasks
    }

    return results
