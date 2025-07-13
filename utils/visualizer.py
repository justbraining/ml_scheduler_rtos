import matplotlib.pyplot as plt

def plot_metrics_comparison(metrics_dict):
    schedulers = list(metrics_dict.keys())
    deadline_misses = [metrics_dict[s]['Deadline Misses'] for s in schedulers]
    avg_waits = [metrics_dict[s]['Average Waiting Time'] for s in schedulers]

    # Bar Chart: Deadline Misses
    plt.figure(figsize=(8, 5))
    plt.bar(schedulers, deadline_misses, color='salmon')
    plt.title('Deadline Misses per Scheduler')
    plt.ylabel('Misses')
    plt.grid(True, axis='y')
    plt.tight_layout()
    plt.show()

    # Line Chart: Average Wait Time
    plt.figure(figsize=(8, 5))
    plt.plot(schedulers, avg_waits, marker='o', color='steelblue', linestyle='-')
    plt.title('Average Waiting Time per Scheduler')
    plt.ylabel('Time Units')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# for gantt chart

import matplotlib.pyplot as plt

def plot_gantt_chart(task_df, title="Task Execution Timeline", save_path=None):
    plt.figure(figsize=(12, 6))
    colors = plt.cm.tab20.colors
    y_pos = 10

    for i, row in task_df.iterrows():
        start = row["start_time"]
        duration = row["execution_time"]
        task_id = row["task_id"]

        plt.barh(y=task_id, width=duration, left=start, height=0.5, color=colors[i % len(colors)])
        plt.text(start + duration / 2, task_id, f"{task_id}", va='center', ha='center', fontsize=8, color="white")

    plt.xlabel("Time")
    plt.ylabel("Task ID")
    plt.title(title)
    plt.grid(True, axis='x', linestyle='--', alpha=0.5)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        print(f"Gantt chart saved to: {save_path}")
    else:
        plt.show()
