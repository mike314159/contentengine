#!/usr/bin/env python3
"""
Test script to add a work queue task using the HTTP API.

Usage:
    python test_add_work_task_api.py --project "test" --queue "test_queue" [--url http://localhost:5038]
"""

import sys
import json
import argparse
import random

import requests


def main():
    parser = argparse.ArgumentParser(
        description="Test adding a work queue task via the /newsletter/work-queue/add API"
    )
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
    parser.add_argument(
        "--url",
        default="http://localhost:5038",
        help="Base URL of the Flask app (default: http://localhost:5038)",
    )
    args = parser.parse_args()

    project = args.project
    queue = args.queue

    # Create a simple text payload with a random number to make it unique
    random_number = random.randint(1000, 999999)
    text = f"Test Task from API {random_number}"

    endpoint = f"{args.url}/newsletter/work-queue/{project}/{queue}/add"
    #endpoint = f"https://playground-8n3t.onrender.com/newsletter/work-queue/{project}/{queue}/add"
    # params = {
    #     "project": project,
    #     "queue": queue,
    # }
    payload = {
        "task_type": "text",
        "text": text,
    }

    payload = {
        "quote": "Never invest in a business you cannot understand.",
        "author": "Warren Buffett",
        "interpretation": "Stick to businesses you can explain so you avoid hidden risks and surprises."
    }

    print("POSTing to work queue API...")
    print(f"URL: {endpoint}")
    #print(f"Query params: {json.dumps(params, indent=2)}")
    print(f"Payload: {json.dumps(payload, indent=2)}\n")

    try:
        resp = requests.post(
            endpoint,
            #params=params,
            json=payload,
            headers={"Content-Type": "application/json"},
        )

        print(f"Status Code: {resp.status_code}")
        try:
            data = resp.json()
            print("Response JSON:")
            print(json.dumps(data, indent=2))
        except ValueError:
            print("Response Text:")
            print(resp.text)

        if resp.status_code == 201:
            print("\n✓ Work queue task added successfully via API!")
            return 0
        else:
            print("\n✗ Failed to add work queue task via API.")
            return 1

    except requests.exceptions.ConnectionError:
        print(f"✗ Error: Could not connect to {endpoint}")
        print("  Make sure the Flask app is running.")
        return 1
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())


