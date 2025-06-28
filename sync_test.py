import time

def fetch_data(task_id):
    print(f"Task {task_id} started")
    time.sleep(2)
    print(f"Task {task_id} finished")
    return f"Result from task {task_id}"

def main():
    results = []
    for i in range(3):
        result = fetch_data(i)
        results.append(result)
    print("All tasks done:", results)

main()
