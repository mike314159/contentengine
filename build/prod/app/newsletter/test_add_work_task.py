#!/usr/bin/env python3
"""
Test script to add a work queue task using WorkQueueManager.

Usage:
    python test_add_work_task.py --project "test" --queue "test_queue"
"""

import sys
import json
import argparse
import random
from pathlib import Path

# Ensure the parent app directory is on sys.path so we can import newsletter.*
CURRENT_FILE = Path(__file__).resolve()
APP_DIR = CURRENT_FILE.parent.parent  # .../app
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from newsletter.objectfactory import ObjectFactory
from newsletter.work_queue_mgr import WorkQueueManager


def main():
    parser = argparse.ArgumentParser(description="Test adding a work queue task via WorkQueueManager")
    parser.add_argument(
        "--project",
        required=True,
        help="Project name for the task",
    )
    parser.add_argument(
        "--queue",
        required=True,
        help="Queue name for the task",
    )
    args = parser.parse_args()

    project = args.project
    queue = args.queue

    # Create a simple text payload with a random number to make it unique
    random_number = random.randint(1000, 999999)
    text = f"Test Task {random_number}"

    factory = ObjectFactory()
    mgr = WorkQueueManager(factory=factory)

    print("Adding task to work queue...")
    print(json.dumps(
        {
            "project": project,
            "queue": queue,
            "task_type": "text",
            "text": text,
        },
        indent=2,
    ))

    task_uuid = mgr.add_task(factory, project, queue, task_type="text", text=text)

    if task_uuid is None:
        print("✗ Failed to add work queue task.")
        return 1

    print("\n✓ Work queue task added successfully!")
    print(f"  task_uuid: {task_uuid}")
    print(f"  project:   {project}")
    print(f"  queue:     {queue}")
    print(f"  text:      {text}")
    return 0


if __name__ == "__main__":
    sys.exit(main())


