import random
import os
import socket

from uilib import renderhelpers as rh
from uilib.components import dygraphchart as dg

from flask import (
    send_from_directory,
)

import pandas as pd
import datetime
from flask import current_app


from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

statics_page = Blueprint('statics_page', __name__)


@statics_page.route("/<path:file>")
def static_file(file):
    site_config = current_app.config['SITE_CONFIG']
    ui_lib_statics_base_dir = site_config.get_uilib_statics_base_dir()
    site_specific_statcs_dir = site_config.get_site_specific_statcs_dir()
    
    # Handle subdirectories by splitting the path
    file_parts = file.split('/')
    if len(file_parts) > 1:
        subdir = file_parts[0]
        filename = file_parts[1]
        dirs = [
            os.path.join(ui_lib_statics_base_dir, subdir),
            os.path.join(site_specific_statcs_dir, subdir)
        ]
    else:
        filename = file
        dirs = [
            os.path.join(ui_lib_statics_base_dir, 'bootstrap/css'),
            os.path.join(ui_lib_statics_base_dir, 'bootstrap/js'),
            os.path.join(ui_lib_statics_base_dir, 'autocomplete'),
            os.path.join(ui_lib_statics_base_dir, 'style'),
            os.path.join(ui_lib_statics_base_dir, 'billboard'),
            os.path.join(ui_lib_statics_base_dir, 'bootstrap/'),
            os.path.join(ui_lib_statics_base_dir, 'images'),
            site_specific_statcs_dir
        ]
    
    for dir in dirs:
        fn = os.path.join(dir, filename)
        if os.path.exists(fn):
            return send_from_directory(dir, filename)
    print("Static Route Not Found '%s'" % (file))
    print("Dirs", dirs)
    return '[FILE NOT FOUND]'


