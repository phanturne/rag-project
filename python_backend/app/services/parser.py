# background task to parse the uploaded file

from fastapi import BackgroundTasks
import time

def parse_file(file_path: str, background_tasks: BackgroundTasks):
    # Simulate a long-running file parsing operation
    background_tasks.add_task(parse_file_task, file_path)

def parse_file_task(file_path: str):
    # Replace this with actual parsing logic
    time.sleep(10)  # Simulate long parsing task
    print(f"File {file_path} parsed successfully")
    # Simulate sending notification
    notify_user(file_path, "Parsing complete")

def notify_user(file_path: str, message: str):
    print(f"Notification for {file_path}: {message}")