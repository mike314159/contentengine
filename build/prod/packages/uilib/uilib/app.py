from flask import Flask
import argparse
import sys
import os

# Import blueprints
from staticroutes import statics_page
from uilibtestroutes import uilib_tests_blp

app = Flask(__name__)

# Add configuration for statics blueprint
class MockSiteConfig:
    def get_uilib_statics_base_dir(self):
        return os.path.join(os.path.dirname(__file__), 'statics')
    
    def get_site_specific_statcs_dir(self):
        return os.path.join(os.path.dirname(__file__), 'statics')



app.config['SITE_CONFIG'] = MockSiteConfig()

# Register blueprints
app.register_blueprint(statics_page, url_prefix="/statics")
app.register_blueprint(uilib_tests_blp, url_prefix="/tests")

@app.route("/")
def hello():
    return "hello"

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run the simple Flask app')
    parser.add_argument('--url', type=str, default=None,
                       help='Test a single URL and return the result, then exit (e.g., --url "/")')
    args = parser.parse_args()
    
    # Handle single URL testing
    if args.url:
        print(f"Testing single URL: {args.url}")
        try:
            with app.test_client() as client:
                response = client.get(args.url)
                print(f"Status Code: {response.status_code}")
                print(f"Content-Type: {response.content_type}")
                print(f"Content Length: {len(response.data)} bytes")
                print("\n" + "="*80)
                print("RESPONSE CONTENT:")
                print("="*80)
                print(response.get_data(as_text=True))
                print("="*80)
                print("URL test completed successfully!")
        except Exception as e:
            print(f"Error testing URL {args.url}: {e}")
            import traceback
            traceback.print_exc()
        sys.exit(0)
    
    # Run the app normally
    app.run(debug=True, port=5073)
