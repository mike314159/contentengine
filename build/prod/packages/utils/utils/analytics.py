import uuid
from ua_parser import user_agent_parser
import json
from utils.deploymentinfo import DeploymentInfo
from posthog import Posthog

# Useful stuff fo adding analytics to the site


class Analytics:

    def __init__(self):
        # self.ph = post_hog_analytics
        # self.events_db = events_db
        self.env = DeploymentInfo().get_env()
        excl_browsers = [
            "AhrefsBot",
            "SemrushBot",
            "Bytespider",
            "MJ12bot",
            "YandexBot",
            "FacebookBot",
            "robot",
            "DotBot",
            "spider",
            "crawler"
        ]
        self.exclude_paths = None
        self.excluded_browsers = set()
        for browser in excl_browsers:
            self.excluded_browsers.add(browser.lower())

    def set_exclude_paths(self, exclude_paths):
        self.exclude_paths = set(exclude_paths)

    # # shorthand version for logging events to keep code cleaner
    # def event(self, u, e, r, p):

    #     if u is None:
    #         u = "unk"

    #     if self.ph is not None:
    #         self.ph.log_event(
    #             object=u,
    #             verb=e,
    #             request=r,
    #             properties=p,
    #         )

    #     if self.events_db is not None:
    #         resource = r.path
    #         self.events_db.log_event(
    #             event_name=e, user_id=u, resource=resource, properties=p
    #         )

    # def log_event(self, object, verb, request, properties):

    #     if self.ph is not None:
    #         self.ph.log_event(
    #             object=object, verb=verb, request=request, properties=properties
    #         )

    #     if self.events_db is not None:
    #         resource = request.path
    #         self.events_db.log_event(
    #             event_name=verb,
    #             user_id=object,
    #             resource=resource,
    #             properties=properties,
    #         )

    def get_request_properties(self, request):

        properties = {}
        if request is not None:
            properties["request_url"] = request.url
            properties["full_path"] = request.full_path
            properties["$current_url"] = request.path
            properties["$referrer"] = request.referrer
            properties["$ip"] = request.remote_addr
            properties["$host"] = request.host
            properties["env"] = self.env

            ua = request.user_agent.string
            result_dict = user_agent_parser.Parse(ua)
            browser = result_dict.get("user_agent", {}).get("family", "Unknown")
            os = result_dict.get("os", {}).get("family", "Unknown")

            properties["$browser"] = browser
            properties["$os"] = os

        return properties

    def add_request_properties(self, properties, request):
        if request is not None:
            properties["request_url"] = request.url
            properties["full_path"] = request.full_path
            properties["$current_url"] = request.path
            properties["$referrer"] = request.referrer
            properties["$ip"] = request.remote_addr
            properties["$host"] = request.host
            properties["env"] = self.env

            ua = request.user_agent.string
            result_dict = user_agent_parser.Parse(ua)
            browser = result_dict.get("user_agent", {}).get("family", "Unknown")
            os = result_dict.get("os", {}).get("family", "Unknown")
            properties["$browser"] = browser
            properties["$os"] = os
        return properties

    # bcookie is a unique identifier for this browser on this device
    def get_bcookie_id(session):
        bcookie_id = session.get("bcookie", None)
        if bcookie_id is None:
            bcookie_id = uuid.uuid4()
            session["bcookie"] = bcookie_id
        return bcookie_id

    def _get_props_to_print(self, properties):
        np = properties.copy()
        if "$browser" in np:
            del np["$browser"]
        if "$os" in np:
            del np["$os"]
        if "$lib" in np:
            del np["$lib"]
        if "$lib_version" in np:
            del np["$lib_version"]
        if "$geoip_disable" in np:
            del np["$geoip_disable"]
        return np


class AnalyticsBackendPostHog(Analytics):

    def __init__(self, posthog_project_key):
        super().__init__()
        self.post_hog_client = Posthog(posthog_project_key)
        self.env = DeploymentInfo().get_env()

    def log_event(self, object, verb, request, properties):

        properties = self.add_request_properties(properties, request)


        try:
            self.post_hog_client.capture(object, verb, properties=properties)
        except Exception as e:
            print("Error logging event: ", e)

        np = self._get_props_to_print(properties)
        print(json.dumps(np, indent=2))


    # shorthand version for logging events to keep code cleaner
    def event(self, u, e, r, p):
        self.log_event(object=u, verb=e, request=r, properties=p)


    # expects a flask request object
    def log_pageview(self, request, user_guid):

        path = request.path
        if self.exclude_paths is not None:
            for excl_path in self.exclude_paths:
                if path.startswith(excl_path):
                    print("Exclude logging path: ", path)
                    return

        properties = self.get_request_properties(request)

        browser = properties.get("$browser", None).lower()
        if "bot" in browser.lower():
            print("Exclude logging browser, bot in name: ", browser)
            return

        if browser in self.excluded_browsers:
            print("Exclude logging browser: ", browser)
            return

        # if exclude_images:
        #     extension = request.path.split(".")[-1]
        #     if extension in ["png", "jpg", "jpeg", "ico"]:
        #         #print("Exclude logging image request: ", request.path)
        #         return

        # properties = {}
        # properties = self.add_request_properties(properties, request)
        # browser = properties.get("$browser", None)

        if user_guid is None:
            user_guid = "unk"
        # self.ph.log_pageview_event(user_guid, properties)

        try:
            self.post_hog_client.capture(user_guid, "$pageview", properties)
        except Exception as e:
            print("Error logging pageview: ", e)

        print("Logged Pageview")
        np = self._get_props_to_print(properties)
        print(json.dumps(np, indent=2))
