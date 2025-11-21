
from utils.secrets_store import get_secret
from posthog import Posthog


from ua_parser import user_agent_parser


class PostHogClient():

    def __init__(self, project_key=None):

        assert project_key is not None
        # if project_key is None:
        #     project_key = get_secret("posthog_project_key")

        self.ph = Posthog(
            project_key
        )

    def log_backend_event(self, event_name):
        self.ph.capture(
            'backend', 
            event_name,
            properties={
                "a": 'b'
            }
        )
        print("PostHog Event: ", event_name)


    def log_event(self, object, verb, properties):

        self.ph.capture(
            object, 
            verb, 
            properties=properties
        )
                
    def log_pageview_event(self, user_id, properties):

        object = user_id
        verb = '$pageview'

        # self.log_event(
        #     object, 
        #     verb, 
        #     properties=properties
        # )

        try:
            self.ph.capture(
                object, 
            verb, 
                properties=properties
            )
        except Exception as e:
            print("PostHog Error Logging Pageview Event: ", e)

        

    # session_id = a unique id created for each user session
    def log_backend_pageview(self, session_id, user_id, request):


        ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        ua = request.user_agent.string

        # Parse the user agent
        result_dict = user_agent_parser.Parse(ua)

        # print(result_dict['user_agent'])
        # # {'major': '5', 'minor': '1', 'family': 'Mobile Safari', 'patch': None}

        # print(result_dict['os'])
        # # {'major': '5', 'patch_minor': None, 'minor': '1', 'family': 'iOS', 'patch': None}

        # print(result_dict['device'])
        # # {'is_spider': False, 'is_mobile': True, 'family': 'iPhone'}


        browser = result_dict.get('user_agent', {}).get('family', 'Unknown')
        os = result_dict.get('os', {}).get('family', 'Unknown')


    # print("Request:", request.args.to_dict())
    # print("Cookies:", request.cookies)
    # print("Endpoint:", request.endpoint)
    # #print("Headers:", request.headers)
    # print("Host:", request.host)
    # print("Referrer:", request.referrer)
    # print("Remote Address:", request.remote_addr)
    # print("Remote User:", request.remote_user)
    # print("User Agents:", request.user_agent)

        url = request.path

        self.ph.capture(user_id, '$pageview', 
            properties={
                '$current_url': url,
                '$browser': browser,
                '$os': os,
                '$host': request.host,
                '$raw_user_agent': ua,
                '$referrer': request.referrer,
                '$ip': request.remote_addr,
                '$session_id': session_id,

            }
        )
