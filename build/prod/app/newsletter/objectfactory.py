
#from siteconfig import SiteConfig
# from utils.resendemailer import ResendEmailer
# from utils.analytics import AnalyticsBackendPostHog
# from utils.posthogclient import PostHogClient
from utils.secrets_store import get_secret
# from utils.object_db_pg import ObjectDBPostgres, ObjectDBEntry
# from utils.contact_db_pg import ContactDBPostgres, ContactDBEntry
# from utils.localandremoteobjectstore import LocalAndRemoteObjectStore
from peewee import PostgresqlDatabase
from .snippet_db_pg import SnippetDBEntry, SnippetDBPostgres
from .work_queue_db import WorkQueueDBEntry, WorkQueueDBPostgres
from .work_queue_task_db import WorkQueueTaskDBEntry, WorkQueueTaskDBPostgres
from .prompt_db import PromptDBEntry, PromptDBPostgres

# from settings import Settings
# from siteconfig import SiteConfig
# from utils.dataframecache import LocalDataFrameCache
# from pybt.financedataproviders import TiingoDataProvider
# from pybt.financialpricesource import FinancialPriceSource
# from pybt.portfoliolibrary import PortfolioLibrary
# from posthog import Posthog
# from backtestcache import BacktestCache
# from perfreportcache import PerfReportCache
#from recapscache import RecapsCache

class ObjectFactory:

    def __init__(self):
        self.objs = {}
        #self.site_config = SiteConfig()

    SNIPPET_DB = "snippet_db"
    WORK_QUEUE_DB = "work_queue_db"
    WORK_QUEUE_TASK_DB = "work_queue_task_db"
    PROMPT_DB = "prompt_db"
    PG_CONNECTION = "pg_connection"

    def get_pg_config(self):
        pg_connect_config = get_secret("render_pg_connect")
        return pg_connect_config

    def get_pg_config_prod(self):
        pg_connect_config = get_secret("render_pg_connect")
        pg_connect_config["schema"] = "crunch"
        return pg_connect_config

    def get_obj(self, obj_name):

        if obj_name in self.objs:
            return self.objs[obj_name]


        if obj_name == ObjectFactory.PG_CONNECTION:
            pg_connect_config = self.get_pg_config()
            pg_db = PostgresqlDatabase(
                database=pg_connect_config["dbname"],
                user=pg_connect_config["user"],
                password=pg_connect_config["password"],
                host=pg_connect_config["host"],
            )
            self.objs[obj_name] = pg_db
            return self.objs[obj_name]


        if obj_name == ObjectFactory.SNIPPET_DB:
            pg_db = self.get_obj(ObjectFactory.PG_CONNECTION)
            pg_connect_config = self.get_pg_config()
            SnippetDBEntry._meta.database.initialize(pg_db)
            SnippetDBEntry._meta.schema = 'newsletter_dev'
            self.objs[obj_name] = SnippetDBPostgres()
            return self.objs[obj_name]


        if obj_name == ObjectFactory.WORK_QUEUE_DB:
            pg_db = self.get_obj(ObjectFactory.PG_CONNECTION)
            pg_connect_config = self.get_pg_config()
            WorkQueueDBEntry._meta.database.initialize(pg_db)
            WorkQueueDBEntry._meta.schema = 'newsletter_dev'
            self.objs[obj_name] = WorkQueueDBPostgres()
            return self.objs[obj_name]


        if obj_name == ObjectFactory.WORK_QUEUE_TASK_DB:
            pg_db = self.get_obj(ObjectFactory.PG_CONNECTION)
            pg_connect_config = self.get_pg_config()
            WorkQueueTaskDBEntry._meta.database.initialize(pg_db)
            WorkQueueTaskDBEntry._meta.schema = 'newsletter_dev'
            self.objs[obj_name] = WorkQueueTaskDBPostgres()
            return self.objs[obj_name]

        if obj_name == ObjectFactory.PROMPT_DB:
            pg_db = self.get_obj(ObjectFactory.PG_CONNECTION)
            pg_connect_config = self.get_pg_config()
            PromptDBEntry._meta.database.initialize(pg_db)
            PromptDBEntry._meta.schema = 'newsletter_dev'
            self.objs[obj_name] = PromptDBPostgres()
            return self.objs[obj_name]

