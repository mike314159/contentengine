
import urllib
from utils.deploymentinfo import DeploymentInfo
import os

class SiteConfig:

    def __init__(self):
        #self.domain_name = 'portfoliocrunch.com'
        #self.site_name = 'Portfolio Crunch'
        # self.logo_src = '/statics/logo.png'

        #self.site_email_from_name = 'Portfolio Crunch'

        # # This is the from email address in verification emails sent by the site.
        #self.site_email_from_addr =  "info@portfoliocrunch.com"

        # # This is the email address where messages submitted from the Contact Us form are sent.
        #self.contact_us_to_email_address = 'portfoliocrunch@carbonlake.com'

        # self.checkout_page_url = 'https://mathstar.lemonsqueezy.com/buy/260cdd62-1489-4496-8d02-f8d3d9b0a027'

        # # These are the hostnames that should be tracked by Plausible Analytics.
        # self.prod_hostnames = ['quizzer-q65s.onrender.com', 'mathstar.ai']

        # # If this is true, then all signup links on the site go around subscription flow
        # # and users who signup get free subscriptions.
        # self.bypass_subscriptions = True
        # self.discount_code_free_subscription = "earlyaccess"

        # # This is the Google Tag for Google Ads.
        # # Its tied to the pageview conversion tracking.
        # #Copy the tag below and paste it in between the <head></head> tags of every page of your website. 
        # #You only need to install the Google tag once per account, even if you are tracking multiple actions.
        # self.google_tag = '''
        #     <!-- Google tag (gtag.js) -->
        #     <script async src="https://www.googletagmanager.com/gtag/js?id=AW-977662468"></script>
        #     <script>
        #     window.dataLayer = window.dataLayer || [];
        #     function gtag(){dataLayer.push(arguments);}
        #     gtag('js', new Date());
        #     gtag('config', 'AW-977662468');
        #     </script>
        # '''

        # #  2. Paste it in between the <head></head> tags of the page(s) you'd like to track, right after the Google tag.
        # self.google_event_snippet = '''
        #     <!-- Event snippet for Page view conversion page -->
        #     <script>
        #     gtag('event', 'conversion', {
        #         'send_to': 'AW-977662468/J_zbCKz7ktgZEITkl9ID',
        #         'value': 1.0,
        #         'currency': 'USD'
        #     });
        #     </script>
        # '''
        
        self.deployment_info = DeploymentInfo()


    # def get_google_tag(self):
    #     return self.google_tag
    # def get_google_event_snippet(self):
    #     return self.google_event_snippet

    # def get_domain_name(self):
    #     return self.domain_name
    
    # def get_canonical_url(self, relative_url):
    #     """Convert a relative URL to an absolute canonical URL."""
    #     return "https://" + self.domain_name + relative_url
    
    # def get_site_name(self):
    #     return self.site_name
    
    # def get_logo_src(self):
    #     return "/statics/logo.png"
    
    # def get_site_email_from_addr(self):
    #     return self.site_email_from_addr

    # def get_site_email_from_name(self):
    #     return self.site_email_from_name
     
    # def get_contact_us_to_email_address(self):
    #     return self.contact_us_to_email_address
    
    # # def get_checkout_page_url(self):
    # #     return self.checkout_page_url
    
    # # def get_bypass_subscriptions(self):
    # #     return self.bypass_subscriptions
    
    # # def get_discount_code_free_subscription(self):
    # #     return self.discount_code_free_subscription
    
    # # def is_free_subscription_discount_code(self, discount_code):
    # #     return discount_code == self.discount_code_free_subscription


    def get_uilib_statics_base_dir(self):
        if self.deployment_info.is_local_venv():
            return '/Volumes/t7shield/Dropbox/code/packages/uilib/uilib/statics/'
        else:
            return '/packages/uilib/uilib/statics/'

    # def get_local_app_dir(self):
    #     if self.deployment_info.is_local_venv():
    #         return '/Volumes/t7shield/Dropbox/code/gitmike/portfolio-crunch/app'
    #     else:
    #         return '/app'
        
    # def get_site_specific_statcs_dir(self):
    #     dir = self.get_local_app_dir()
    #     return os.path.join(dir, 'statics')
    #     #if self.deployment_info.is_local_venv():
    #     #     return '/Volumes/t7shield/Dropbox/code/gitmike/portfolio-crunch/app/statics'
    #     # else:
    #     #     return 'app/statics'

    # def get_data_dir(self):
    #     if self.deployment_info.is_local_venv():
    #         dir = self.get_local_app_dir()
    #         return os.path.join(dir, 'data')
    #         # return '/Volumes/t7shield/Dropbox/code/gitmike/portfolio-crunch/app/data'
    #     else:
    #         return '/data'

    # def get_log_dir(self):
    #     if self.deployment_info.is_local_venv():
    #         data_dir = self.get_data_dir()
    #         if not os.path.exists(data_dir):
    #             os.makedirs(data_dir, exist_ok=True)
    #         return os.path.join(data_dir, 'logs')
    #     else:
    #         return '/var/log'


    # # PRICES_CACHE_DIR = '/data/cache/tiingo_prices'
    # # BASE_CACHE_DATA_DIR = '/data/cache'
    # # BACKTESTS_CACHE_DIR = '/data/cache/backtests'
    # # PERF_REPORTS_DIR = '/data/cache/perf_reports'
    # # BACKTESTS_RUNS_FN = '/data/cache/backtests/backtest_runs.pkl'
    # # OBJECTS_CACHE_DIR = '/data/cache/objects'

    # # def get_base_cache_data_dir(self):
    # #     data_dir = self.get_data_dir()
    # #     return os.path.join(data_dir, 'cache')

    # # def get_prices_cache_dir(self):
    # #     cache_data_dir = self.get_base_cache_data_dir()
    # #     return os.path.join(cache_data_dir, 'tiingo_prices')



    # # def get_backtests_cache_dir(self):
    # #     cache_data_dir = self.get_base_cache_data_dir()
    # #     return os.path.join(cache_data_dir, 'backtests')

    # # def get_perf_reports_cache_dir(self):
    # #     cache_data_dir = self.get_base_cache_data_dir()
    # #     return os.path.join(cache_data_dir, 'perf_reports')

    # # def get_backtests_runs_fn(self):
    # #     cache_data_dir = self.get_base_cache_data_dir()
    # #     return os.path.join(cache_data_dir, 'backtests', 'backtest_runs.pkl')

    # # def get_objects_cache_dir(self):
    # #     cache_data_dir = self.get_base_cache_data_dir()
    # #     return os.path.join(cache_data_dir, 'objects')

    # def get_pybt_config_dir(self):
    #     if self.deployment_info.is_local_venv():
    #         return '/Volumes/t7shield/Dropbox/code/packages/pybt/config'
    #     else:
    #         return '/packages/pybt/config'

    # def get_local_obj_dir(self):
    #     data_dir = self.get_data_dir()
    #     return os.path.join(data_dir, 'objects')
    


    # def get_portfolio_summaries_dir(self):
    #     dir = self.get_local_app_dir()
    #     return os.path.join(dir, 'content/portfolio_summaries') 
    #     #if self.deployment_info.is_local_venv():
    #     #     return '/Volumes/t7shield/Dropbox/code/gitmike/portfolio-crunch/app/content/portfolio_summaries'
    #     # else:
    #     #     return '/app/content/portfolio_summaries'

    # def get_blog_articles_dir(self):
    #     dir = self.get_local_app_dir()
    #     return os.path.join(dir, 'blog/articles')
    #     # if self.deployment_info.is_local_venv():
    #     #     return '/Volumes/t7shield/Dropbox/code/gitmike/portfolio-crunch/app/blog/articles'
    #     # else:
    #     #     return '/app/blog/articles'