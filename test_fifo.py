from linux_sim.linux_fifo_scheduler import linux_fifo_scheduler
from utils.metrics import calculate_metrics
import pandas as pd

df = pd.read_csv("data/task_log.csv")
result_df, _ = linux_fifo_scheduler(df.copy())

print("FIFO Scheduler Metrics:")
for k, v in calculate_metrics(result_df).items():
    print(f"{k}: {v}")
