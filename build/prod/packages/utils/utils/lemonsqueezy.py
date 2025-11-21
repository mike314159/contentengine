import requests
import json
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)
from utils.secrets_store import get_secret


class LemonSqueezyEvent:

    PURCHASE_TYPE_ORDER = "order"
    PURCHASE_TYPE_SUBSCRIPTION = "subscription"

    def __init__(
        self,
        event_name,
        purchase_type,
        store_id,
        customer_id,
        customer_email,
        order_id,
        product_name,
        product_id,
        variant_name,
        variant_id,
        price,
        price_id,
        status,
        customer_portal_url,
    ):
        self.event_name = event_name
        self.purchase_type = purchase_type
        self.store_id = store_id
        self.customer_id = customer_id
        self.customer_email = customer_email
        self.order_id = order_id
        self.product_name = product_name
        self.product_id = product_id
        self.variant_name = variant_name
        self.variant_id = variant_id
        self.price = price
        self.price_id = price_id
        self.status = status
        self.customer_portal_url = customer_portal_url

        if self._valid_str(self.customer_email, "customer_email"):
            self.valid = True
        else:
            self.valid = False

    # def _valid_int(self, value_int, name):
    #     if type(value_int) != int:
    #         print(
    #             f"ERROR LemonSqueezyEvent: {name} ({value_int}) is not an integer, type: {type(value_int)}"
    #         )
    #         return False
    #     return True

    def _valid_str(self, value_str, name):
        if type(value_str) != str:
            print(
                f"ERROR LemonSqueezyEvent: {name} ({value_str}) is not a string, type: {type(value_str)}"
            )
            return False
        if len(value_str) == 0:
            print(f"ERROR LemonSqueezyEvent: {name} ({value_str}) is empty")
            return False
        return True

    def is_valid(self):
        return self.valid

    # i think the way it works is it gets cancelled first and then when that period is over, it gets expired
    # it wont hurt me to be generous here until i know the exact logic
    def is_active(self):

        if self.event_name == "subscription_expired":
            return False
        
        return True
    

    def __str__(self):
        return f"""
LemonSqueezyEvent:
    purchase_type: {self.purchase_type}
    store_id: {self.store_id}
    customer_id: {self.customer_id}
    customer_email: {self.customer_email}
    order_id: {self.order_id}
    product_name: {self.product_name}
    product_id: {self.product_id}
    variant_name: {self.variant_name}
    variant_id: {self.variant_id}
    price: {self.price}
    price_id: {self.price_id}
    status: {self.status}
    customer_portal_url: {self.customer_portal_url}
    valid: {self.valid}
"""


class LemonSqueezy:

    def __init__(self, api_key):
        self.api_key = api_key

    def _call_lemon_squeezy(self, url, method="GET", data=None):

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/vnd.api+json",
            "Authorization": f"Bearer {self.api_key}",
        }

        # Configure retry strategy
        retry_strategy = Retry(total=2, backoff_factor=0.1)
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session = requests.Session()
        session.mount("https://", adapter)

        try:
            response = session.get(
                url=f"{url}",
                headers=headers,
                timeout=10,
            )
            response.raise_for_status()
        except requests.RequestException as e:
            print("Exception")
            print(e)
            exit(1)

        dict = response.json()
        # print(json.dumps(dict, indent=4))
        return dict

    def get_customers(self):

        url = "https://api.lemonsqueezy.com/v1/customers"
        response = self._call_lemon_squeezy(url)
        customers = response.get("data", [])
        for customer in customers:
            record_type = customer.get("type", "")
            if record_type != "customers":
                print("Why am I seeing a non-customer record type?")
                print(customer)
                continue

            customer_id = customer.get("id", "")
            attributes = customer.get("attributes", {})
            store_id = attributes.get("store_id", "")
            customer_email = attributes.get("email", "")
            customer_name = attributes.get("name", "")
            customer_status = attributes.get("status", "")
            customer_status_formatted = attributes.get("status_formatted", "")
            created_at = attributes.get("created_at", "")
            updated_at = attributes.get("updated_at", "")
            test_mode = attributes.get("test_mode", "")

            print(
                f"Customer ID: {customer_id}, Email: {customer_email}",
                "Status: ",
                customer_status,
                "Updated At: ",
                updated_at,
            )

    def _get_customer_info(self, record):
        customer_id = record.get("id", "")
        attributes = record.get("attributes", {})
        store_id = attributes.get("store_id", 0)
        customer_email = attributes.get("email", "")
        customer_name = attributes.get("name", "")
        customer_status = attributes.get("status", "")
        customer_status_formatted = attributes.get("status_formatted", "")
        created_at_str = attributes.get(
            "created_at", ""
        )  # "2024-09-19T00:15:02.000000Z"
        updated_at_str = attributes.get(
            "updated_at", ""
        )  # "2024-09-19T00:20:30.000000Z"
        test_mode = attributes.get("test_mode", None)

        created_at_ts = int(
            datetime.strptime(created_at_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            .replace(tzinfo=timezone.utc)
            .timestamp()
        )
        updated_at_ts = int(
            datetime.strptime(updated_at_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            .replace(tzinfo=timezone.utc)
            .timestamp()
        )

        info = {
            "customer_id": customer_id,
            "store_id": store_id,
            "email": customer_email,
            "name": customer_name,
            "status": customer_status,
            "created_at_ts": created_at_ts,
            "updated_at_ts": updated_at_ts,
            "test_mode": test_mode,
        }
        return info

    def get_customer_by_email(self, email):
        url = f"https://api.lemonsqueezy.com/v1/customers/?filter[email]={email}"
        response = self._call_lemon_squeezy(url)
        # print("get_customer_by_email result:")
        # print(json.dumps(response, indent=4))

        customers = response.get("data", [])
        for customer in customers:
            record_type = customer.get("type", "")
            if record_type != "customers":
                print("Why am I seeing a non-customer record type?")
                print(customer)
                continue

            info = self._get_customer_info(customer)
            info_email = info.get("email", "")
            if info_email == email:
                return info

        return None

    def get_webhook_order_details(data):

        event_name = data.get("meta", {}).get("event_name", None)
        if event_name == "order_created":
            order_id = data.get("data", {}).get("id", None)
            attributes = data.get("data", {}).get("attributes", {})
            store_id = attributes.get("store_id", None)
            customer_email = attributes.get("user_email", None)
            customer_id = attributes.get("customer_id", None)

            first_order_item = attributes.get("first_order_item", {})

            product_name = first_order_item.get("product_name", None)
            product_id = first_order_item.get("product_id", None)

            variant_name = first_order_item.get("variant_name", None)
            variant_id = first_order_item.get("variant_id", None)

            return {
                "order_id": order_id,
                "store_id": store_id,
                "customer_email": customer_email,
                "customer_id": customer_id,
                "product_name": product_name,
                "product_id": product_id,
                "variant_name": variant_name,
                "variant_id": variant_id,
            }
        return None

    def parse_webhook_event_data(self, data):

        event_name = data.get("meta", {}).get("event_name", None)
        print("event_name: ", event_name)

        attributes = data.get("data", {}).get("attributes", {})

        store_id = attributes.get("store_id", None)
        customer_id = attributes.get("customer_id", None)
        customer_email = attributes.get("user_email", None)
        status = attributes.get("status", None)

        purchase_type = None
        order_id = None
        product_name = None
        product_id = None
        variant_name = None
        variant_id = None
        price = None
        price_id = None
        customer_portal_url = None

        if event_name not in ["order_created", "subscription_created", "subscription_updated", "subscription_cancelled"]:
            return None

        if event_name == "order_created":
            """
            "first_order_item": {
                "id": 4039882,
                "order_id": 4097378,
                "product_id": 355794,
                "variant_id": 528414,
                "price_id": 900174,
                "product_name": "MathStar",
                "variant_name": "Lifetime Subscription",
                "price": 4000,
                "quantity": 1,
                "created_at": "2024-11-14T22:38:55.000000Z",
                "updated_at": "2024-11-14T22:38:55.000000Z",
                "test_mode": true
            },
            """
            first_order_item = attributes.get("first_order_item", {})
            product_name = first_order_item.get("product_name", None)
            product_id = first_order_item.get("product_id", None)
            variant_name = first_order_item.get("variant_name", None)
            variant_id = first_order_item.get("variant_id", None)
            price = first_order_item.get("price", None)
            price_id = first_order_item.get("price_id", None)
            order_id = first_order_item.get("order_id", None)
            purchase_type = LemonSqueezyEvent.PURCHASE_TYPE_ORDER
            customer_portal_url = None

        if (
            event_name == "subscription_created"
            or event_name == "subscription_updated"
            or event_name == "subscription_cancelled"
        ):

            product_name = attributes.get("product_name", None)
            product_id = attributes.get("product_id", None)
            variant_name = attributes.get("variant_name", None)
            variant_id = attributes.get("variant_id", None)
            price = attributes.get("price", None)
            order_id = attributes.get("order_id", None)
            customer_portal_url = attributes.get("urls", {}).get(
                "customer_portal", None
            )

            first_subscription_item = attributes.get("first_subscription_item", {})
            price_id = first_subscription_item.get("price_id", None)
            purchase_type = LemonSqueezyEvent.PURCHASE_TYPE_SUBSCRIPTION

        event = LemonSqueezyEvent(
            event_name=event_name,
            purchase_type=purchase_type,
            store_id=store_id,
            customer_id=customer_id,
            customer_email=customer_email,
            order_id=order_id,
            product_name=product_name,
            product_id=product_id,
            variant_name=variant_name,
            variant_id=variant_id,
            price=price,
            price_id=price_id,
            status=status,
            customer_portal_url=customer_portal_url,
        )
        return event

    def get_webhook_event_info(self, data):
        id = data.get("data", {}).get("id", None)
        event_name = data.get("meta", {}).get("event_name", None)
        return id, event_name
