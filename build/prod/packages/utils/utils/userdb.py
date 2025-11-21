import json
import os
import pandas as pd
import peewee
import datetime

import uuid
import pickle
import sys
import hashlib
import glob
import re
import time
import pytz
import bcrypt
import hmac
from pydantic import BaseModel, ValidationError
from typing import Optional


class UserDBEntry(peewee.Model):

    id = peewee.PrimaryKeyField(primary_key=True)

    guid = peewee.CharField(unique=True)
    parent_guid = peewee.CharField(index=True, null=True)

    deployment = peewee.CharField()
    host = peewee.CharField()
    env = peewee.CharField()

    email = peewee.CharField(index=True, unique=True, null=True)
    username = peewee.CharField(index=True, unique=True, null=True)
    name = peewee.CharField(null=True)
    password_hash = peewee.CharField(null=True)

    added_ts = peewee.IntegerField()

    # Sign-Up stuff
    # Timestamps are used both to indicate they did something as well as the time.
    # Default for them is 0, which meants they have not done anything.
    # account_signup_requested_ts = peewee.IntegerField(default=0)
    # account_signup_confirmed_ts = peewee.IntegerField(default=0)

    account_canceled_ts = peewee.IntegerField(default=0)
    account_canceled_reason = peewee.CharField(null=True)

    account_verify_token = peewee.CharField(null=True)
    account_verify_token_sent_ts = peewee.IntegerField(default=0)
    account_verify_confirmed_ts = peewee.IntegerField(default=0)

    password_reset_token = peewee.CharField(null=True)
    password_reset_token_sent_ts = peewee.IntegerField(default=0)
    password_reset_ts = peewee.IntegerField(default=0)

    email_change_token = peewee.CharField(null=True)
    email_change_token_sent_ts = peewee.IntegerField(default=0)
    email_change_ts = peewee.IntegerField(default=0)
    email_change_new_email = peewee.CharField(null=True)

    user_roles = peewee.TextField(null=True)
    extra_attrs = peewee.TextField(null=True)

    # Newsletter stuff
    # Timestamps are used both to indicate they did something as well as the time.
    # Default for them is 0, which meants they have not done anything.
    newsletter_requested_ts = peewee.IntegerField(default=0)
    newsletter_confirmed_ts = peewee.IntegerField(default=0)
    newsletter_canceled_ts = peewee.IntegerField(default=0)
    newsletter_canceled_reason = peewee.CharField(null=True)

    # LemonSqueezy Subscription Lifecycle
    subscription_source = peewee.IntegerField(null=True)
    subscription_customer_id = peewee.CharField(null=True)
    subscription_store_id = peewee.IntegerField(null=True)
    subscription_status = peewee.CharField(null=True)
    subscription_created_at = peewee.IntegerField(null=True)
    subscription_updated_at = peewee.IntegerField(null=True)
    subscription_active = peewee.IntegerField(null=True)

    subscription_plan = peewee.CharField(null=True)
    subscription_plan_last_update_ts = peewee.IntegerField(null=True)
    subscription_plan_active = peewee.IntegerField(null=True)

    signup_offer = peewee.CharField(null=True)

    # Transacation emails. No opting out of these emails.
    # Signup Confirmation email
    # Welcome email, product intro
    # Account cancellation email
    # Password reset email

    # Progress emails
    # whats happening with students, kids. 

    # Engagement Reminder emails    
    # Sign-up reactivation email 
    # Re-engagement email

    # Marketing emails    
    # Feature education email, New Feature adoption email
    # Product update email, new releases

    transaction_emails_unsubscribed_ts = peewee.IntegerField(null=True)
    engagement_emails_unsubscribed_ts = peewee.IntegerField(null=True)
    marketing_emails_unsubscribed_ts = peewee.IntegerField(null=True)
    progress_emails_unsubscribed_ts = peewee.IntegerField(null=True)

    class Meta:

        table_name = "users"
        database = peewee.DatabaseProxy()


class UserModel(BaseModel):

    guid: str
    parent_guid: Optional[str] = None
    deployment: str
    host: str
    env: str
    name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    extra_attrs: dict
    password_hash: str
    user_roles: Optional[str] = None
    added_ts: int

    account_verify_token: str
    account_verify_token_sent_ts: int
    account_verify_confirmed_ts: int

    email_signin_token: Optional[str] = None
    email_signin_sent_ts: Optional[int] = None

    subscription_source: Optional[int] = None
    subscription_customer_id: Optional[str] = None
    subscription_store_id: Optional[int] = None
    subscription_status: Optional[str] = None
    subscription_created_at: Optional[int] = None
    subscription_updated_at: Optional[int] = None
    subscription_active: Optional[int] = None

    subscription_plan: Optional[str] = None
    subscription_plan_last_update_ts: Optional[int] = None
    subscription_plan_active: Optional[int] = None

    email_change_token: Optional[str] = None
    email_change_token_sent_ts: Optional[int] = None
    email_change_ts: Optional[int] = None

    signup_offer: Optional[str] = None

    transaction_emails_unsubscribed_ts: Optional[int] = None
    engagement_emails_unsubscribed_ts: Optional[int] = None
    marketing_emails_unsubscribed_ts: Optional[int] = None
    progress_emails_unsubscribed_ts: Optional[int] = None

class UserObj:

    def __init__(self, user_model):
        self.model = user_model

    def get_roles_list(self):
        if self.model.user_roles is None:
            return []
        return self.model.user_roles.split(",")

    def find_first_role(self, choices=[]):
        roles = self.get_roles_list()
        for role in roles:
            if role in choices:
                return role
        return None

    def get_email(self):
        return self.model.email

    def get_name(self):
        return self.model.name
    
    def get_roles(self):
        return self.model.user_roles
    
    def get_subscription_plan(self):
        return self.model.subscription_plan
    
    def get_guid(self):
        return self.model.guid

class UserDB:

    VERIFICATION_TOKEN_VERIFIED = 1
    VERIFICATION_TOKEN_BAD = 2
    VERIFICATION_TOKEN_ALREADY_VERIFIED = 3
    VERIFICATION_USER_GUID_NOT_FOUND = 4

    SUBSCRIPTION_SOURCE_LEMON_SQUEEZY = 1

    EMAIL_TYPE_TRANSACTION = "transaction"
    EMAIL_TYPE_ENGAGEMENT = "engagement"
    EMAIL_TYPE_MARKETING = "marketing"
    EMAIL_TYPE_PROGRESS = "progress"

    def __init__(self, deployment, host, env):
        self.deployment = deployment
        self.host = host
        self.env = env

        try:
            UserDBEntry.create_table()
        except peewee.OperationalError:
            print("ERROR: Failed to create UserDBEntry table")

    def make_user_guuid(self, email):
        s = "guuid-%s-%s-%s-%s" % (self.deployment, self.host, self.env, email)
        return hashlib.md5(email.encode()).hexdigest()

    # This is unix timestampe
    def _get_now_ts(self):
        return int(time.time())

    def add_newsletter_request(self, email):
        user_guuid = self.make_user_guuid(email)
        added_ts = self._get_now_ts()
        item = UserDBEntry(
            guuid=user_guuid,
            deployment=self.deployment,
            host=self.host,
            env=self.env,
            email=email,
            added_ts=added_ts,
            newsletter_requested_ts=added_ts,
        )
        item.save()
        return item.id

    def query_to_df(self, query):
        return pd.DataFrame(list(query.dicts()))

    def get_all_df(self):
        query = UserDBEntry.select()
        return self.query_to_df(query)

    def get_users_df(self, limit=500):
        query = (
            UserDBEntry.select()
            # .where(EventStoreEntry.event_type == event_type)
            .order_by(UserDBEntry.added_ts).limit(limit)
        )
        df = self.query_to_df(query)
        return df
    
    def get_users_since_ts(self, ts_start, ts_end):
        query = (
            UserDBEntry.select()
            .where(UserDBEntry.added_ts >= ts_start)
            .where(UserDBEntry.added_ts <= ts_end)
            .order_by(UserDBEntry.added_ts)
        )
        df = self.query_to_df(query)
        return df

    def _unicode_to_bytes(unicode_string):
        """Converts a unicode string to a bytes object.

        :param unicode_string: The unicode string to convert."""
        if isinstance(unicode_string, str):
            bytes_object = bytes(unicode_string, "utf-8")
        else:
            bytes_object = unicode_string
        return bytes_object

    def _hash_password(password):
        # Python 3 unicode strings must be encoded as bytes before hashing.
        password = UserDB._unicode_to_bytes(password)
        prefix = "2b"
        prefix = UserDB._unicode_to_bytes(prefix)
        salt = bcrypt.gensalt(rounds=12, prefix=prefix)
        password_hashed = bcrypt.hashpw(password, salt)
        return password_hashed

    def verify_password(self, password_hashed_db, password_entered_by_user):
        password_hashed_db = UserDB._unicode_to_bytes(password_hashed_db)
        password_entered_by_user = UserDB._unicode_to_bytes(password_entered_by_user)
        return hmac.compare_digest(
            bcrypt.hashpw(password_entered_by_user, password_hashed_db),
            password_hashed_db,
        )

    def get_and_set_new_email_signin_token(self, user_guid):
        email_signin_token = str(uuid.uuid4())
        email_signin_sent_ts = self._get_now_ts()
        query = UserDBEntry.update(
            email_signin_token=email_signin_token,
            email_signin_sent_ts=email_signin_sent_ts,
        ).where(UserDBEntry.guid == user_guid)
        try:
            query.execute()
            return email_signin_token
        except Exception as e:
            print("Exception: ", e)
            return None

    def get_and_set_new_password_reset_token(self, user_email):
        user_obj = self.get_user_obj_by_email(user_email)
        if user_obj is None:
            print("User email not found '%s'" % user_email)
            return None, None
        user_guid = user_obj.model.guid
        password_reset_token = str(uuid.uuid4())
        password_reset_token_sent_ts = self._get_now_ts()
        query = UserDBEntry.update(
            password_reset_token=password_reset_token,
            password_reset_token_sent_ts=password_reset_token_sent_ts,
        ).where(UserDBEntry.guid == user_guid)
        try:
            query.execute()
            return user_guid, password_reset_token
        except Exception as e:
            print("Exception: ", e)
            return None, None

    def _try_execute(self, query):
        try:
            query.execute()
            return True, "Success"
        except Exception as e:
            print("Exception: ", e)
            return False, "Query execution failed"

    def get_and_set_new_email_reset_token(self, user_guid, new_email):
        reset_token = str(uuid.uuid4())
        reset_token_sent_ts = self._get_now_ts()
        query = UserDBEntry.update(
            email_change_token=reset_token,
            email_change_token_sent_ts=reset_token_sent_ts,
            email_change_new_email=new_email,
        ).where(UserDBEntry.guid == user_guid)

        success, msg = self._try_execute(query)
        if not success:
            return success, msg, None
        return success, "Success", reset_token

    def get_email_change_token_and_new_email(self, user_guid):
        query = UserDBEntry.select(
            UserDBEntry.email_change_token, UserDBEntry.email_change_new_email
        ).where(UserDBEntry.guid == user_guid)
        try:
            user = query.get()
            return user.email_change_token, user.email_change_new_email
        except UserDBEntry.DoesNotExist:
            return None, None

    def clear_email_change_token(self, user_guid):
        query = UserDBEntry.update(
            email_change_token=None,
            email_change_new_email=None,
        ).where(UserDBEntry.guid == user_guid)
        success, msg = self._try_execute(query)
        return success, msg

    def verify_email_change_token_and_change_email(self, user_guid, token):
        email_change_token, new_email = self.get_email_change_token_and_new_email(
            user_guid
        )
        if email_change_token is None or email_change_token != token:
            return False, "Invalid Token"
        query = UserDBEntry.update(email=new_email).where(UserDBEntry.guid == user_guid)
        success, msg = self._try_execute(query)
        if success:
            return self.clear_email_change_token(user_guid)
        return success, msg

    def verify_password_reset_token(self, user_guid, token):
        query = UserDBEntry.select(UserDBEntry.password_reset_token_sent_ts).where(
            (UserDBEntry.guid == user_guid)
            & (UserDBEntry.password_reset_token == token)
        )

        try:
            user = query.get()
            password_reset_token_sent_ts = user.password_reset_token_sent_ts
            current_ts = self._get_now_ts()
            if current_ts - password_reset_token_sent_ts > 3600:
                return (
                    False,
                    "Reset Token Expired. Please request password reset again.",
                )
            return True, None
        except UserDBEntry.DoesNotExist:
            return False, "Invalid Token"

    def _add_user(
        self,
        parent_guid,
        username,
        name,
        email,
        password,
        roles_csv="",
        extra_attrs={},
        user_guid=None,
    ):

        print("Adding user: ", email, password, roles_csv, extra_attrs)
        if user_guid is None:
            user_guid = uuid.uuid4()
        account_verify_token = str(uuid.uuid4())
        account_verify_token_sent_ts = self._get_now_ts()
        password_hashed = UserDB._hash_password(password)
        extra_attrs_str = json.dumps(extra_attrs)

        added_ts = self._get_now_ts()
        try:
            item = UserDBEntry(
                guid=user_guid,
                parent_guid=parent_guid,
                name=name,
                username=username,
                deployment=self.deployment,
                host=self.host,
                env=self.env,
                email=email,
                password_hash=password_hashed,
                added_ts=added_ts,
                account_verify_token=account_verify_token,
                account_verify_token_sent_ts=account_verify_token_sent_ts,
                account_verify_confirmed_ts=0,
                user_roles=roles_csv,
                extra_attrs=extra_attrs_str,
            )
            item.save()
            return True, "", user_guid, account_verify_token
        except peewee.IntegrityError as e:
            # This will catch unique constraint violations, like duplicate email
            print("IntegrityError: ", e)
            return False, f"User already exists. Please try a different one.", None, None
        except Exception as e:
            # This will catch any other unexpected errors
            print("Exception: ", e)
            return False, f"Error adding user", None, None

    # This method adds a new user that is managed by another user, called the parent.
    def add_sub_user(
        self,
        parent_guid,
        sub_user_username,
        sub_user_password,
        sub_user_name,
        roles_csv="",
        extra_attrs={},
        user_guid=None,
    ):
        
        user_obj = self.get_user_obj_by_username(sub_user_username)
        if user_obj is not None:
            return None, None, False, "Username already exists"

        sub_user_email = None
        success, msg, sub_user_guid, sub_user_account_verify_token = self._add_user(
            parent_guid,
            sub_user_username,
            sub_user_name,
            sub_user_email,
            sub_user_password,
            roles_csv,
            extra_attrs,
            user_guid=user_guid,
        )
        return sub_user_guid, sub_user_account_verify_token, success, msg

    def add_user(self, name, email, password, roles_csv="", extra_attrs={}, user_guid=None):
        parent_guid = None
        username = None
        if email is not None:
            email = email.lower()
        success, err_msg, user_guid, account_verify_token = self._add_user(
            parent_guid,
            username,
            name,
            email,
            password,
            roles_csv,
            extra_attrs,
            user_guid=user_guid,
        )
        return success, err_msg, user_guid, account_verify_token

    def permanently_delete_user_with_guid(self, guid):
        query = UserDBEntry.delete().where(UserDBEntry.guid == guid)
        query.execute()

    def permanently_delete_user_with_email(self, email):
        query = UserDBEntry.delete().where(UserDBEntry.email == email)
        query.execute()

    def permanently_delete_user_with_username(self, username):
        query = UserDBEntry.delete().where(UserDBEntry.username == username)
        query.execute()

    # Dont use this for anything except for debugging.
    def get_user_df(self, user_guid):
        query = UserDBEntry.select().where(UserDBEntry.guid == user_guid)
        df = self.query_to_df(query)
        return df

    def _get_user_info_from_query(self, query):
        entries = list(query.dicts())
        if len(entries) < 1:
            return None
        dct = entries[0]
        extra_attrs_str = dct.get("extra_attrs", "{}")
        try:
            extra_attrs_dct = json.loads(extra_attrs_str)
        except Exception as e:
            print("Error parsing extra_attrs: ", extra_attrs_str)
            extra_attrs_dct = {}
        dct["extra_attrs_str"] = extra_attrs_str
        dct["extra_attrs"] = extra_attrs_dct
        # print("User Info:\n", json.dumps(dct, indent=2))
        return dct

    def _get_user_model_from_info(self, user_info):
        user_model = UserModel(**user_info)
        return user_model

    def email_exists(self, email):
        query = UserDBEntry.select().where(UserDBEntry.email == email)
        return query.exists()

    def get_user_obj_by_email(self, email):
        query = UserDBEntry.select().where(UserDBEntry.email == email)
        user_info = self._get_user_info_from_query(query)
        if user_info is None:
            return None
        user_model = self._get_user_model_from_info(user_info)
        return UserObj(user_model)

    def get_user_obj_by_username(self, username):
        query = UserDBEntry.select().where(UserDBEntry.username == username)
        user_info = self._get_user_info_from_query(query)
        if user_info is None:
            return None
        user_model = self._get_user_model_from_info(user_info)
        return UserObj(user_model)

    def get_user_obj_by_guid(self, guid):
        query = UserDBEntry.select().where(UserDBEntry.guid == guid)
        user_info = self._get_user_info_from_query(query)
        if user_info is None:
            return None
        user_model = self._get_user_model_from_info(user_info)
        return UserObj(user_model)

    def get_user_model_by_guid(self, guid):
        query = UserDBEntry.select().where(UserDBEntry.guid == guid)
        user_info = self._get_user_info_from_query(query)
        if user_info is None:
            return None
        return self._get_user_model_from_info(user_info)


    def get_sub_users_from_parent_guid(self, parent_guid):
        query = UserDBEntry.select().where(UserDBEntry.parent_guid == parent_guid)
        df = self.query_to_df(query)
        if len(df) == 0:
            return pd.DataFrame()
        df.sort_values(by="added_ts", ascending=True, inplace=True)
        df = df[["guid", "name", "username", "extra_attrs"]]
        df.set_index("guid", inplace=True, drop=False)
        return df

    def get_sub_user_info_from_parent_guid(self, parent_guid, sub_user_guid):
        query = UserDBEntry.select().where(
            (UserDBEntry.parent_guid == parent_guid)
            & (UserDBEntry.guid == sub_user_guid)
        )
        info = self._get_user_info_from_query(query)
        if info is None:
            return None
        # extra_attrs = json.loads(info["extra_attrs"])
        # info["extra_attrs"] = info["extra_attrs"]
        return info

    def valid_login_email_password(self, email, password):
        user_obj = self.get_user_obj_by_email(email)
        if user_obj is None:
            return False, f"Unknown email '{email}'", None
        password_hash = user_obj.model.password_hash
        valid_pwd = self.verify_password(password_hash, password)
        if not valid_pwd:
            return False, "Incorrect password", None
        return True, None, user_obj

    def valid_login_username_password(self, username, password):
        user_obj = self.get_user_obj_by_username(username)
        if user_obj is None:
            return False, f"Unknown username '{username}'", None
        password_hash = user_obj.model.password_hash
        valid_pwd = self.verify_password(password_hash, password)
        if not valid_pwd:
            return False, "Incorrect password", None
        return True, None, user_obj

    def update_user(self, user_guid, **kwargs):
        query = UserDBEntry.update(**kwargs).where(UserDBEntry.guid == user_guid)
        query.execute()

    def update_password(self, user_guid, password):
        print("Updating password for user guid: ", user_guid, " to ", password)
        password_hashed = UserDB._hash_password(password)
        query = UserDBEntry.update(password_hash=password_hashed).where(
            UserDBEntry.guid == user_guid
        )
        try:
            query.execute()
            return True, ""
        except Exception as e:
            print("Exception: ", e)
            return False, "Error updating password"

    def update_user_settings(self, user_guid, name, password):
        if len(password) > 0:
            password_hashed = UserDB._hash_password(password)
        else:
            password_hashed = None

        if password_hashed is None:
            query = UserDBEntry.update(
                name=name,
            ).where(UserDBEntry.guid == user_guid)
        else:
            query = UserDBEntry.update(
                name=name,
                password_hash=password_hashed,
            ).where(UserDBEntry.guid == user_guid)

        try:
            query.execute()
            return True, ""
        except Exception as e:
            print("Exception: ", e)
            return False, "Error updating user settings"

    def update_parent_sub_user(
        self,
        sub_user_guid,
        sub_user_username,
        sub_user_password,
        sub_user_name,
        roles_csv,
        #extra_attrs,
    ):
        print("update_parent_sub_user()")
        print("sub_user_guid: ", sub_user_guid)
        print("sub_user_username: ", sub_user_username)
        print("sub_user_password: ", sub_user_password)
        print("sub_user_name: ", sub_user_name)
        print("roles_csv: ", roles_csv)
        #print("extra_attrs: ", extra_attrs)

        if len(sub_user_password) > 0:
            password_hashed = UserDB._hash_password(sub_user_password)
            query = UserDBEntry.update(
                username=sub_user_username,
                name=sub_user_name,
                user_roles=roles_csv,
                #extra_attrs=json.dumps(extra_attrs),
                password_hash=password_hashed,
            ).where(UserDBEntry.guid == sub_user_guid)

        else:
            query = UserDBEntry.update(
                username=sub_user_username,
                name=sub_user_name,
                user_roles=roles_csv,
                #extra_attrs=json.dumps(extra_attrs),
            ).where(UserDBEntry.guid == sub_user_guid)

        try:
            query.execute()
            return True, ""
        except Exception as e:
            print("Exception: ", e)
            return False, "Error updating user"

    def verify_user_account_token(self, user_guid, token):

        user_obj = self.get_user_obj_by_guid(user_guid)

        print("Verify user account token for user guid: ", user_guid)
        print("Token: ", token)

        if user_obj is None:
            return None, False, UserDB.VERIFICATION_USER_GUID_NOT_FOUND

        print("Correct token: ", user_obj.model.account_verify_token)

        if user_obj.model.account_verify_confirmed_ts > 0:
            return user_obj, True, UserDB.VERIFICATION_TOKEN_ALREADY_VERIFIED

        if user_obj.model.account_verify_token == token:
            self.update_user(user_guid, account_verify_confirmed_ts=self._get_now_ts())
            return user_obj, True, UserDB.VERIFICATION_TOKEN_VERIFIED

        return user_obj, False, UserDB.VERIFICATION_TOKEN_BAD

    def get_subscription_info_from_email(self, email):
        query = UserDBEntry.select(
            UserDBEntry.guid,
            UserDBEntry.subscription_source,
            UserDBEntry.subscription_customer_id,
            UserDBEntry.subscription_store_id,
            UserDBEntry.subscription_status,
            UserDBEntry.subscription_created_at,
            UserDBEntry.subscription_updated_at,
            UserDBEntry.subscription_active,
        ).where(UserDBEntry.email == email)
        info = self._get_user_info_from_query(query)
        if info is None:
            return None
        return info

    def update_subscription_info(
        self,
        user_guid,
        subscription_plan,
        subscription_plan_last_update_ts,
        subscription_plan_active,
    ):
        query = UserDBEntry.update(
            subscription_plan=subscription_plan,
            subscription_plan_last_update_ts=subscription_plan_last_update_ts,
            subscription_plan_active=subscription_plan_active,
        ).where(UserDBEntry.guid == user_guid)
        try:
            query.execute()
            return True, ""
        except Exception as e:
            print("Exception: ", e)
            return False, "Error updating subscription info"

    def update_user_name_and_role(self, user_guid, name, role):
        query = UserDBEntry.update(name=name, user_roles=role).where(
            UserDBEntry.guid == user_guid
        )
        try:
            query.execute()
            return True, ""
        except Exception as e:
            print("Exception: ", e)
            return False, "Error updating user name and role"

    # This method is used from outside the LemonSqueezy flow.
    # If I give out a special sign-up referral code, then this is how I grant the subscription.
    def activate_special_subscription(self, user_guid, referral_code):
        # source = f"referral:{referral_code}"
        query = UserDBEntry.update(
            # subscription_source=source,
            subscription_active=True
        ).where(UserDBEntry.guid == user_guid)
        try:
            query.execute()
            return True, ""
        except Exception as e:
            print("Exception: ", e)
            return False, "Error updating subscription info"

    def get_current_plan_info(self, user_guid):
        query = UserDBEntry.select(
            UserDBEntry.email,
            UserDBEntry.subscription_plan,
            UserDBEntry.subscription_plan_last_update_ts,
            UserDBEntry.subscription_plan_active
        ).where(UserDBEntry.guid == user_guid)
        info = self._get_user_info_from_query(query)
        print("get_current_subscription_plan() info:\n", json.dumps(info, indent=2))
        """
         {
            "email": "test@test.com",
            "subscription_plan": "free-assessment",
            "subscription_plan_last_update_ts": 1731025887,
            "subscription_plan_active": 1,
            "extra_attrs_str": "{}",
            "extra_attrs": {}
        }
        """
        return info

    
    def update_plan_details(self, user_guid, plan, active):
        active_int = 1 if active else 0
        query = UserDBEntry.update(
            subscription_plan=plan,
            subscription_plan_last_update_ts=self._get_now_ts(),
            subscription_plan_active=active_int,
        ).where(UserDBEntry.guid == user_guid)
        try:
            query.execute()
            
            return True, ""
        except Exception as e:
            print("Exception: ", e)
            return False, "Error updating subscription plan"


    def get_unverified_users(self):
        query = UserDBEntry.select().where(
            (UserDBEntry.email.is_null(False)) &  # email is not NULL
            (UserDBEntry.account_verify_token_sent_ts > 0) &
            (UserDBEntry.account_verify_confirmed_ts == 0)
        )
        df = self.query_to_df(query)
        return df
    
    def update_email_unsubscribed_ts(
            self, 
            user_email, 
            email_type
    ):
        if email_type == UserDB.EMAIL_TYPE_TRANSACTION:
            query = UserDBEntry.update(
                transaction_emails_unsubscribed_ts=self._get_now_ts(),
            ).where(UserDBEntry.email == user_email)
        elif email_type == UserDB.EMAIL_TYPE_ENGAGEMENT:
            query = UserDBEntry.update(
                engagement_emails_unsubscribed_ts=self._get_now_ts(),
            ).where(UserDBEntry.email == user_email)
        elif email_type == UserDB.EMAIL_TYPE_MARKETING:
            query = UserDBEntry.update(
                marketing_emails_unsubscribed_ts=self._get_now_ts(),
            ).where(UserDBEntry.email == user_email)
        elif email_type == UserDB.EMAIL_TYPE_PROGRESS:
            query = UserDBEntry.update(
                progress_emails_unsubscribed_ts=self._get_now_ts(),
            ).where(UserDBEntry.email == user_email)
        try:
            query.execute()
            print("Successfully updated email unsubscribe timestamp ", email_type, " for email: ", user_email)
            return True, ""
        except Exception as e:
            print("Exception: ", e)
            return False, "Error updating email unsubscribe timestamp"
