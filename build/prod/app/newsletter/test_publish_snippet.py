#!/usr/bin/env python3
"""
Test script to publish a snippet through the API.

Usage:
    python test_publish_snippet.py --uuid <uuid_prefix> --published <date>
    
Example:
    python test_publish_snippet.py --uuid 30c2d00 --published "2025-10-11"
"""

import sys
import json
import requests
import argparse

def main():
    parser = argparse.ArgumentParser(description='Test publishing a snippet through the API')
    parser.add_argument('--uuid', required=True,
                       help='First 7 characters of the UUID to publish')
    parser.add_argument('--published', required=True,
                       help='Published date value (e.g., "2025-10-11")')
    parser.add_argument('--url', default='http://localhost:5038',
                       help='Base URL of the Flask app (default: http://localhost:5038)')
    args = parser.parse_args()
    
    # Validate UUID prefix is 7 characters
    if len(args.uuid) != 7:
        print(f"✗ Error: UUID prefix must be exactly 7 characters, got {len(args.uuid)}: {args.uuid}")
        return 1
    
    # API endpoint
    url = f"{args.url}/newsletter/api/publish-snippet"
    
    # Request data
    request_data = {
        "uuid": args.uuid,
        "published": args.published
    }
    
    print(f"POSTing to: {url}")
    print(f"Data: {json.dumps(request_data, indent=2)}")
    print()
    
    try:
        response = requests.post(
            url,
            json=request_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("\n✓ Snippet published successfully!")
            print(f"  - UUID prefix: {args.uuid}")
            print(f"  - Published value: {args.published}")
            print(f"  - published_ts set to current timestamp")
            return 0
        else:
            print(f"\n✗ Failed to publish snippet. Status: {response.status_code}")
            return 1
            
    except requests.exceptions.ConnectionError:
        print(f"✗ Error: Could not connect to {url}")
        print("  Make sure the Flask app is running.")
        return 1
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())

