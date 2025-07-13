import random
import pandas as pd

def generate_tasks(num_tasks=20):
    tasks = []
    for i in range(num_tasks):
        task = {
            "task_id":f"T{i+1}",
            "arrival_time":random.randint(0,10),
            "execution_time":random.randint(1,5),
            "deadline":random.randint(10,25),
            "priority":random.randint(1,5),
            "task_type":random.choice(["IO", "CPU"])
        }
        tasks.append(task)

    df = pd.DataFrame(tasks)
    df.to_csv("data/task_log.csv", index = False)
    print(f"{num_tasks} tasks generated and saved to task_log.csv")

if __name__ == "__main__":
    generate_tasks()