import asyncio

async def fetch_data(task_id):
    print(f"Task {task_id} started")
    await asyncio.sleep(2)  # Simulate delay (e.g., HTTP request)
    print(f"Task {task_id} finished")
    return f"Result from task {task_id}"

async def main():
    # Run multiple coroutines concurrently
    tasks = [fetch_data(i) for i in range(3)]
    results = await asyncio.gather(*tasks)
    print("All tasks done:", results)

asyncio.run(main())
