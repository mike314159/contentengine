#!/usr/bin/env python3
"""
Test script to add a work queue task with an image using the HTTP API.

Usage:
    python test_add_work_task_image_api.py --project "test" --queue "test_queue" [--url http://localhost:5038]
"""

import sys
import json
import argparse
import base64
from pathlib import Path

import requests


def main():
    parser = argparse.ArgumentParser(
        description="Test adding a work queue task with an image via the /newsletter/work-queue/<project>/<queue>/add API"
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

    # Get the path to image.jpg in the newsletter directory
    script_dir = Path(__file__).parent
    image_path = script_dir / "image.jpg"
    
    if not image_path.exists():
        print(f"✗ Error: Image file not found at {image_path}")
        return 1

    # Read and encode the image as base64
    try:
        with open(image_path, "rb") as f:
            image_bytes = f.read()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        print(f"✓ Loaded image: {image_path} ({len(image_bytes)} bytes)")
    except Exception as e:
        print(f"✗ Error reading image file: {e}")
        return 1

    endpoint = f"{args.url}/newsletter/work-queue/{project}/{queue}/add"
    payload = {
        "task_type": "image",
        "image": image_base64,
    }

    print("POSTing to work queue API...")
    print(f"URL: {endpoint}")
    print(f"Payload keys: {list(payload.keys())}")
    print(f"Image data length: {len(image_base64)} characters (base64)\n")

    try:
        resp = requests.post(
            endpoint,
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
            print("\n✓ Work queue task with image added successfully via API!")
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

