# background task to parse the uploaded file

from fastapi import BackgroundTasks
from llama_parse import LlamaParse

def parse_file(file_path: str, background_tasks: BackgroundTasks):
    # Simulate a long-running file parsing operation
    background_tasks.add_task(parse_file_task, file_path)

def parse_file_task(file_path: str):
    # Replace this with actual parsing logic
    parser = LlamaParse(
    #api_key=,  # can also be set in your env as LLAMA_CLOUD_API_KEY
    result_type="markdown",  # "markdown" and "text" are available
    num_workers=4,  # if multiple files passed, split in `num_workers` API calls
    verbose=True,
    language="en",  # Optionally you can define a language, default=en
    )

    # sync
    documents = parser.load_data("Orientation Documents-Spring 2024 Orientation Document.pdf")
    documents

    # save the parsed data
    parse_path = "parsed_data.md"
    with open(parse_path, "w") as f:
        f.write(documents[0].text)

    print(f"File {file_path} parsed successfully")
    # Simulate sending notification
    notify_user(file_path, "Parsing complete")

def notify_user(file_path: str, message: str):
    print(f"Notification for {file_path}: {message}")