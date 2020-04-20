import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc

import sys, os.path
from app import app

def Navbar():
    navbar = dbc.Navbar(
        [
            dbc.Row(
                [
                    dbc.Col(html.Img(src=app.get_asset_url('logo.png'), height="30px")),
                    dbc.Col(dbc.NavbarBrand("Brand Name", className="ml-2")),
                ],
                align="center",
                no_gutters=True,
            ),
        ],
        color='dark',
        dark=True,
    )
    return navbar