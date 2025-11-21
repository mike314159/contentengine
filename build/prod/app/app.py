import socket
import random
import os
import json
import argparse
import sys
from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    send_from_directory,
    url_for,
    make_response,
	redirect,
    flash
)
from siteconfig import SiteConfig
from utils.deploymentinfo import DeploymentInfo
from uilib.components import *
from uilib.pagebuilder import PageBuilder
from uilib.components import HeaderComponent
from factory import ObjectFactory


#----------------------------------------------------------------------------#
# Blueprints.
#----------------------------------------------------------------------------#

from uilib.uilibtestroutes import uilib_tests_blp
from uilib.staticroutes import statics_page
from newsletter.routes import newsletter_blp


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)

app.register_blueprint(uilib_tests_blp, url_prefix="/tests")
app.register_blueprint(statics_page, url_prefix="/statics")
app.register_blueprint(newsletter_blp, url_prefix="/app")

app.secret_key = b'_5#y2L"F1234z\n\xec]/'


def render_page(body_components):



    header_comp = HeaderComponent.example()
    footer_comp = FooterComponent.example()


    page_title = "Playground"
    pb = PageBuilder(page_title=page_title, page_template="bootstrap_empty.html", 
        statics_base_dir=site_config.get_uilib_statics_base_dir())


    body_comp = Container(cols=1, components=body_components)

    pb.add(header_comp, position="header")
    pb.add(footer_comp, position="footer")
    pb.add(body_comp, position="body")

    return pb.render()


#----------------------------------------------------------------------------#
# App Public Routes.
#----------------------------------------------------------------------------#

@app.route("/test")
def test_page():

    posthog = '''
        <script>
            !function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.async=!0,p.src=s.api_host.replace(".i.posthog.com","-assets.i.posthog.com")+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="capture identify alias people.set people.set_once set_config register register_once unregister opt_out_capturing has_opted_out_capturing opt_in_capturing reset isFeatureEnabled onFeatureFlags getFeatureFlag getFeatureFlagPayload reloadFeatureFlags group updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures getActiveMatchingSurveys getSurveys onSessionId".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);
            posthog.init('phc_MEzCHrC21qpBw3nOq2Ploye8xiqsOkr0Mdre8tzNnMB',{api_host:'https://us.i.posthog.com'})
        </script>
    '''
    tmpl = '''
        <html>
            <head>
                <title>Hello World!</title>
                {tracking}
            </head>
            <body>
                <h3>Hello!</h3>
                <b>Hostname:</b> {hostname}<br/>
                <b>Random:</b> {num}
                <br><br>
                <a href='{url}'>UI Library Tests</a>
            </body>
        </html>
    '''
    ui_lib_url = url_for("uilib_tests.tests_home_page")
    rnum = random.randint(1, 100)
    return tmpl.format(hostname=socket.gethostname(), num=rnum, tracking=posthog, url=ui_lib_url)


@app.route("/")
def home_page():
        
    h = HTMLComponent("<h1>Home Page</h1>")
    body = [
        h,
        #HeroComponent.example(),
        #FeaturesComponent.example(),
        #PricingPlansComponent.example(),
    ]
    return render_page(body)

# --------------------------------
# Health Check Page
# --------------------------------

@app.route("/health")
def health_check_page():
    return "OK"




if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Run the Flask app')
    parser.add_argument('--url', type=str, help='Test a single URL')
    args = parser.parse_args()

    site_config = SiteConfig()
    deploy_info = DeploymentInfo()
    print("Deployment Info:\n", json.dumps(deploy_info.get_app_env(), indent=4))
    debug_mode = deploy_info.is_not_production()

    if deploy_info.is_local_venv():
        port = 5057
    else:
        port = 5000

    # Handle single URL testing
    if args.url:
        print(f"Testing single URL: {args.url}")
        try:
            with app.test_client() as client:
                response = client.get(args.url)
                print(f"Status Code: {response.status_code}")
                print(f"Content-Type: {response.content_type}")
                print(f"Content Length: {len(response.data)} bytes")
                print("\n" + "=" * 80)
                print("RESPONSE CONTENT:")
                print("=" * 80)
                print(response.get_data(as_text=True))
                print("=" * 80)
                print("URL test completed successfully!")
        except Exception as e:
            print(f"Error testing URL {args.url}: {e}")
            import traceback

            traceback.print_exc()
        sys.exit(0)

    # Run the app normally
    app.run(host="0.0.0.0", debug=debug_mode, port=port)

