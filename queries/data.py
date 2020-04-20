import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from flask_caching import Cache

import pandas as pd
import os, sys, inspect, logging
from app import app, cache 

# import custom package with database connection class 
from db_connect import DBConnector
db = DBConnector()

# Cache timeout
TIMEOUT = 604800 

@cache.memoize(timeout=TIMEOUT)
def getData():
    df = db.runQuery("""
    -- SQL query
    """)
    return df
