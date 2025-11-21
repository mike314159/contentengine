#!/usr/bin/env python3
"""
Test script to add a snippet through the API.

Usage:
    python test_post_snippet.py [--url URL]
    
Example:
    python test_post_snippet.py --url http://localhost:5038
"""

import sys
import json
import requests
import argparse
import uuid

def main():
    parser = argparse.ArgumentParser(description='Test adding a snippet through the API')
    parser.add_argument('--url', default='http://localhost:5038', 
                       help='Base URL of the Flask app (default: http://localhost:5038)')
    args = parser.parse_args()
    
    # API endpoint
    url = f"{args.url}/newsletter/snippets"
    
    # Sample snippet data
    snippet_data = {
        "project": f"test-project-{uuid.uuid4().hex[:8]}",
        "category": "test",
        "text": f"Test snippet added via API - {uuid.uuid4().hex[:8]}",
        "approval_state": 0,
        "deleted": 0
    }
    
    print(f"POSTing to: {url}")
    print(f"Data: {json.dumps(snippet_data, indent=2)}")
    print()
    
    try:
        response = requests.post(
            url,
            json=snippet_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 201:
            print("\n✓ Snippet added successfully!")
            return 0
        else:
            print(f"\n✗ Failed to add snippet. Status: {response.status_code}")
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

