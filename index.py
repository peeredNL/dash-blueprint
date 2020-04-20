import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from app import app

from layout.navbar import Navbar 
from pages.dashboard import Dashboard

nav = Navbar()

app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    nav,
    html.Div(id="page-content")
])

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def display_page(pathname):
    # if pathname == 'path-to-page':
    return Dashboard()

if __name__ == "__main__":
    app.run_server(debug=True)