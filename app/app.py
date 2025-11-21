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
app.register_blueprint(newsletter_blp, url_prefix="/newsletter")

app.secret_key = b'_5#y2L"F1234z\n\xec]/'

#g_object_factory = ObjectFactory()

# #----------------------------------------------------------------------------#
# # LogToLogin 
# #----------------------------------------------------------------------------#


# from logto import LogtoClient, LogtoConfig, Storage
# from flask import session
# from typing import Union

# class SessionStorage(Storage):
#     def get(self, key: str) -> Union[str, None]:
#         return session.get(key, None)

#     def set(self, key: str, value: Union[str, None]) -> None:
#         session[key] = value

#     def delete(self, key: str) -> None:
#         session.pop(key, None)


# client_logto = LogtoClient(
#     LogtoConfig(
#         endpoint="https://vqpovc.logto.app/",
#         appId="sajq559bhp2grfct54oc7",
#         appSecret="1rGgpM2aX1Wz0Mqlngv4O9IIWx5mcqyf",
#     ),
#     storage=SessionStorage(),
# )

# # particlestew logto password, gold7fish!

# #----------------------------------------------------------------------------#
# # LogTo Auth Routes.
# #----------------------------------------------------------------------------#

# @app.route("/sign-in")
# async def sign_in_page():
#     # Get the sign-in URL and redirect the user to it
#     url = url_for("log_to_callback")
#     url = "http://localhost:5026/callback"
#     return redirect(await client_logto.signIn(
#         #redirectUri="http://localhost:5026/callback",
#         redirectUri=url,
#     ))

# @app.route("/callback")
# async def log_to_callback():
#     try:
#         await client_logto.handleSignInCallback(request.url) # Handle a lot of stuff
#         #callback_url = url_for("user_home_page")
#         callback_url = "http://localhost:5026"
#         return redirect(callback_url) # Redirect the user to the home page after a successful sign-in
#     except Exception as e:
#         # Change this to your error handling logic
#         return "Error: " + str(e)
    
# @app.route("/sign-out")
# async def sign_out():
#     #home_url = url_for("home"),
#     url = "http://localhost:5026/"
#     return redirect(
#         # Redirect the user to the home page after a successful sign-out
#         await client_logto.signOut(postLogoutRedirectUri=url)
#         #await client_logto.signOut(postLogoutRedirectUri=home_url)
#     )


def render_page(body_components):

    # is_authenticated = client_logto.isAuthenticated()

    # example_links = [
    #     #{"name": "Home", "url": "/"},
    #     {"name": "Features", "url": "/#features"},
    #     {"name": "Pricing", "url": "/#pricing"},
    #     {"name": "FAQs", "url": "/faqs"},
    #     {"name": "About", "url": "/about"}
    # ]

    # if is_authenticated:
    #     sign_in_url = None
    #     sign_up_url = None
    #     sign_out_url = url_for("sign_out")
    # else:
    #     sign_in_url = url_for("sign_in_page")
    #     sign_up_url = url_for("sign_in_page")
    #     sign_out_url = None

    # header_comp = HeaderComponent(
    #     home_page_url="/",
    #     links=example_links,
    #     login_url=sign_in_url,
    #     sign_up_url=sign_up_url,
    #     sign_out_url=sign_out_url,
    #     current_item="Features"
    # )

    header_comp = HeaderComponent.example()
    footer_comp = FooterComponent.example()

    # pb = PageBuilder(page_title='Test Page', page_template="bootstrap_empty.html", header_component=header_comp, footer_component=footer_comp)

    # body_comp = Container(cols=1, components=body_components)
    # pb.add(body_comp)

    page_title = "Playground"
    pb = PageBuilder(page_title=page_title, page_template="bootstrap_empty.html", 
        statics_base_dir=site_config.get_uilib_statics_base_dir())

    #pb.add_header_js(plausible_analytics_js)
    #pb.add_header_js(google_tag_js)
    #pb.add_header_js(google_event_snippet_js)

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


# --------------------------------
# Frost Dates Page
# --------------------------------

@app.route("/api/get-lat-lon", methods=['GET'])
def api_get_lat_lon():
    location = request.args.get('location')
    if location is None:
        return jsonify({"error": "Location is required"}), 400
    
    data = {
        "lat": 37.484722,
        "lon": -122.231278
    }
    return jsonify(data)

@app.route("/frost-dates", methods=['GET'])
def frost_dates_page():

    api_url = url_for("uilib_tests.test_htmx_api_page")
    i = random.randint(1, 1000)
    html = '''
        <div id="parent-div">
            <p>Test: hx-swap = afterend</p>
        </div>
        <button hx-get="%s"
            hx-trigger="click"
            hx-target="#parent-div"
            hx-swap="afterend">
            Click Me! %d
        </button><br><br>
    ''' % (api_url, i)

    # html2 = '''
    #     <div id="parent-div-2">
    #         <p>Test: hx-swap = innerHTML</p>
    #     </div>
    #     <button hx-get="%s"
    #         hx-trigger="click"
    #         hx-target="#parent-div-2"
    #         hx-swap="innerHTML"
    #         hx-indicator="#indicator"
    #     >
    #         Click Me!
    #     </button><br><br>
    # ''' % api_url

    # html3 = '''
    #     <button class="btn btn-primary" type="button" disabled>
    #         <div>
    #             <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
    #             <span class="sr-only">Loading...</span>
    #         </div>
    #     </button>

    # '''

    # html4 = test_htmx_add_object_component()

    # # '''
    # # hx-post="%s"
    # #         hx-trigger="click"
    # #         hx-target="#parent-div-2"
    # #         hx-swap="innerHTML"
    # #         hx-indicator="#indicator"
    # # '''
    pb = PageBuilder()

    c = HTMLComponent(html)
    pb.add(c)


    # c = HTMLComponent(html2)
    # pb.add(c)

    # spinner = '''
    #     <div id="indicator" class="spinner-border htmx-indicator" role="status">
    #         <span class="sr-only"></span>
    #     </div><br><br>
    # '''
    #c = HTMLComponent(spinner)
    #pb.add(c)

#    c = HTMLComponent(html3)
#    pb.add(c)

    # c = HTMLComponent(html4)
    # pb.add(c)

    return pb.render()




# --------------------------------
# BlueSky Post Page
# --------------------------------

# @app.route("/bluesky/post", methods=["POST"])
# def bluesky_post_api():

#     if not request.is_json and not request.form:
#         return jsonify({"error": "Invalid content type"}), 400
    
#     try:
#         # Handle both JSON and form data
#         data = request.get_json() if request.is_json else request.form.to_dict()
#         print("Received data:", data)
        
#         message = data.get("message")
#         key = data.get("key")
#         print("Message:", message)
#         print("Key:", key)

#         if not BlueskyClient.key_is_valid(key):
#             return jsonify({"error": "Invalid key"}), 400
#         else:
#             print("Key is valid")
    
#         if message is None:
#             return jsonify({"error": "Message is required"}), 400

#         bluesky_client = g_object_factory.get_obj(ObjectFactory.BLUESKY_CLIENT)
#         bluesky_client.post_message(message)

#         print("Message posted")

#         return jsonify({"status": "success"}), 200
    
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


"""
This route will play a game of rock paper scissors between a human and a computer player.
The computer player will be a simple AI player that uses a random strategy.
The human player will click one of 3 buttons, rock, paper, or scissors.
This causes an HTMX request to the server to get the computer's choice and the result of the round.
The winner of the round will be displayed.

"""
@app.route("/rock-paper-scissors")
def rock_paper_scissors_page():
    components = []
    
    # Add title
    components.append(HTMLComponent("<h1>Rock Paper Scissors</h1>"))
    
    # Add game buttons with HTMX
    buttons_html = """
    <div class="text-center mb-4">
        <button class="btn btn-primary m-2" hx-post="/play-rps" hx-vals='{"choice": "rock"}' hx-target="#result">
            🪨 Rock
        </button>
        <button class="btn btn-primary m-2" hx-post="/play-rps" hx-vals='{"choice": "paper"}' hx-target="#result">
            📄 Paper
        </button>
        <button class="btn btn-primary m-2" hx-post="/play-rps" hx-vals='{"choice": "scissors"}' hx-target="#result">
            ✂️ Scissors
        </button>
    </div>
    <div id="result" class="text-center">
        Make your choice!
    </div>
    """
    components.append(HTMLComponent(buttons_html))
    
    return render_page(components)

@app.route("/play-rps", methods=["POST"])
def play_rps():
    player_choice = request.form.get("choice")
    choices = ["rock", "paper", "scissors"]
    computer_choice = random.choice(choices)
    
    # Determine winner
    if player_choice == computer_choice:
        result = "Tie!"
    elif (
        (player_choice == "rock" and computer_choice == "scissors") or
        (player_choice == "paper" and computer_choice == "rock") or
        (player_choice == "scissors" and computer_choice == "paper")
    ):
        result = "You win!"
    else:
        result = "Computer wins!"
        
    response_html = f"""
    <div class="mt-4">
        <p>You chose: {player_choice}</p>
        <p>Computer chose: {computer_choice}</p>
        <h3>{result}</h3>
    </div>
    """
    
    return response_html

# #----------------------------------------------------------------------------#
# # App Private Routes.
# #----------------------------------------------------------------------------#

# @app.route("/user-home-page")
# async def user_home_page():
#     if client_logto.isAuthenticated() is False:
#         url = "http://localhost:5026/sign-in"
#         print("Not authenticated <a href='/sign-in'>Sign in</a>")
#         #sign_in_url = url_for("sign_in_page")
#         return redirect(url)
#     else:
#         return (
#             # Get local ID token claims
#             client_logto.getIdTokenClaims().model_dump_json(exclude_unset=True)
#             + "<br>"
#         )
    

#     '''
#     {"iss":"https://vqpovc.logto.app/oidc","sub":"v53cc3ojvfw6","aud":"sajq559bhp2grfct54oc7",
#     "exp":1714325286,"iat":1714321686,"at_hash":"ZsvcB9oqJ5xM0D2GzrOIG1J2kQwenDsO",
#     "name":null,"username":null,"picture":null,"updated_at":1714321684625,"created_at":1714321683894}
#     '''
#     # return (
#     #     # Get local ID token claims
#     #     client_logto.getIdTokenClaims().model_dump_json(exclude_unset=True)
#     #     + "<br>"
#     #     # Fetch user info from Logto userinfo endpoint
#     #     (await client_logto.fetchUserInfo()).model_dump_json(exclude_unset=True)
#     #     + "<br><a href='/sign-out'>Sign out</a>"
#     # )

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
        port = 5038
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

