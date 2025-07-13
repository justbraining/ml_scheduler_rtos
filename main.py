from schedulers.round_robin import round_robin_scheduler
from schedulers.priority_scheduler import priority_scheduler
from schedulers.edf_scheduler import edf_scheduler
from schedulers.ml_scheduler import ml_scheduler

from linux_sim.linux_fifo_scheduler import linux_fifo_scheduler
from linux_sim.linux_rr_scheduler import linux_rr_scheduler  

from utils.metrics import calculate_metrics
from utils.visualizer import plot_metrics_comparison, plot_gantt_chart
from ml.feature_builder import build_training_data

import pandas as pd
import os

# Create results/plots folder if it doesn't exist
os.makedirs("results/plots", exist_ok=True)

# Load task data
df = pd.read_csv("data/task_log.csv")

# Store metrics for each scheduler
metrics_all = {}

# Round Robin
rr_df, _ = round_robin_scheduler(df.copy(), time_quantum=2)
metrics_all['Round Robin'] = calculate_metrics(rr_df)

# Priority Scheduler
prio_df, _ = priority_scheduler(df.copy())
metrics_all['Priority'] = calculate_metrics(prio_df)

# EDF Scheduler
edf_df, _ = edf_scheduler(df.copy())
metrics_all['EDF'] = calculate_metrics(edf_df)

# Linux FIFO Scheduler
fifo_df, _ = linux_fifo_scheduler(df.copy())
metrics_all['Linux FIFO'] = calculate_metrics(fifo_df)

# Linux RR Scheduler
rr_linux_df, _ = linux_rr_scheduler(df.copy())
metrics_all['Linux RR'] = calculate_metrics(rr_linux_df)

# ML Scheduler
ml_df, _ = ml_scheduler(df.copy())
metrics_all['ML Scheduler'] = calculate_metrics(ml_df)

# Save Gantt charts
plot_gantt_chart(ml_df, title="ML Scheduler - Gantt Chart", save_path="results/plots/gantt_ml_scheduler.png")
plot_gantt_chart(fifo_df, title="Linux FIFO - Gantt Chart", save_path="results/plots/gantt_linux_fifo.png")

# Visual comparison
plot_metrics_comparison(metrics_all)

# Save training data from EDF output
edf_features = build_training_data(edf_df, "EDF")
edf_features.to_csv("data/edf_training_data.csv", index=False)

# Print ML metrics
print("\nML Scheduler Metrics:")
for k, v in metrics_all['ML Scheduler'].items():
    print(f"{k}: {v}")
