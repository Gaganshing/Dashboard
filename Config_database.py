import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, html, callback, dcc, State

dash.register_page(__name__, path='/config_database')



# Define styles for the sidebar and content area
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#343a40",  # Darker background
    "color": "#ffffff",  # White text
    "transition": "all 0.3s",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

# Function to create the sidebar menu
def create_sidebar():
    offcanvas = dbc.Offcanvas(
        [
            html.Div([
                dbc.NavItem(dbc.NavLink(
                    [html.I(className="bi bi-caret-right-fill me-2"), "Database Settings"],
                    href="/config_database"
                )),
                dbc.NavItem(dbc.NavLink(
                    [html.I(className="bi bi-gear-fill me-2"), "Testplace Configuration"],
                    href="/config_tp"
                )),
                dbc.NavItem(dbc.NavLink(
                    [html.I(className="bi bi-pencil-square me-2"), "Edit Testplace"],
                    href="/impl"
                )),
            ]),
        ],
        id="offcanvas",
        title="Testing Menu",
        is_open=False,
    )

    sidebar = html.Div(
        [
            html.Img(src="/static/images/ultratronikLogoU.png", height="60px", style={"margin-bottom": "20px"}),
            dbc.NavbarBrand("UltraTorkWeb", className="ms-2", style={"font-size": "21px", "font-weight": "bold"}),
            dbc.Nav(
                [
                    dbc.NavLink("Dashboard", href="/", className="bi bi-house"),
                    dbc.NavLink("Testing Menu", href="/", id="open-offcanvas", className="bi bi-geo-alt", active=True),
                    dbc.NavLink("Documentation", href="/documentation", className="bi bi-pen"),
                ],
                vertical=True,
                pills=True,
            ),
            offcanvas,
        ],
        style=SIDEBAR_STYLE,
    )

    return sidebar

def MainPage():
    DatabaseTyp = "SqlLite"

    inputDatabaseTyp = dbc.Row([
        dbc.Label("Datenbank Typ", html_for="input-database-typ", width=2),
        dbc.Col(
            dcc.Dropdown(
                id="inputDatabaseTyp",
                options=[
                    {"label": "SqlLite", "value": "SqlLite"},
                    {"label": "MySQL", "value": "MySQL"},
                ],
                value=DatabaseTyp,  # Set default value
                placeholder="Select Database Type"  # Change placeholder
            ),
            width=10,
        )
    ], className="mb-3")

    # Input for sqlite
    inputSQliteParams = html.Div(id='sqlite', children=[
        dbc.Row([
            dbc.Label("Datenbank Name", html_for="input-database-name", width=2),
            dbc.Col(
                dbc.Input(type="text", id="inputDatabaseName", placeholder="Enter Database Name"),
                width=10,
            )
        ], className="mb-3")
    ])

    # Inputs for MySQL
    inputMySQLParams = html.Div(id='mysql-params', children=[
        dbc.Row([
            dbc.Label("DBPath", html_for="input-db-path", width=2),
            dbc.Col(
                dbc.Input(type="text", id="inputDBPath", placeholder="Enter DB Path"),
                width=10,
            )
        ], className="mb-3"),
        dbc.Row([
            dbc.Label("DBHost", html_for="input-db-host", width=2),
            dbc.Col(
                dbc.Input(type="text", id="inputDBHost", placeholder="Enter DB Host"),
                width=10,
            )
        ], className="mb-3"),
        dbc.Row([
            dbc.Label("DBUserName", html_for="input-db-username", width=2),
            dbc.Col(
                dbc.Input(type="text", id="inputDBUserName", placeholder="Enter DB Username"),
                width=10,
            )
        ], className="mb-3"),
        dbc.Row([
            dbc.Label("DBPassword", html_for="input-db-password", width=2),
            dbc.Col(
                dbc.Input(type="password", id="inputDBPassword", placeholder="Enter DB Password"),
                width=10,
            )
        ], className="mb-3")
    ])

    save_button = dbc.Button("Save", id="save-parameters", color="success", n_clicks=0, className="mt-3")

    return dbc.Form([inputDatabaseTyp, inputSQliteParams, inputMySQLParams,
                     html.Div(id='save-button-container', children=save_button, style={'display': 'none'})])


@callback(
    [Output('sqlite', 'style'),
     Output('mysql-params', 'style'),
     Output('save-button-container', 'style')],
    [Input('inputDatabaseTyp', 'value')]
)
def toggle_params(database_typ):
    if database_typ == 'SqlLite':
        return {'display': 'block'}, {'display': 'none'}, {'display': 'block'}
    elif database_typ == 'MySQL':
        return {'display': 'none'}, {'display': 'block'}, {'display': 'block'}
    else:
        return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}


def ConfigDatabasePage():

    layout = html.Div(
        [
            html.Link(href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.9.0/font/bootstrap-icons.css",
                      rel="stylesheet"),
            dcc.Location(id='url', refresh=False),
            html.Div(id="sidebar", children=create_sidebar()),
            html.Div(id="page-content", style=CONTENT_STYLE, children=[
                dbc.Card(
                    [
                        dbc.CardHeader(html.H2("Database Configuration")),
                        dbc.CardBody(MainPage()),
                    ]
                )
            ])
        ]
    )
    return layout

layout = ConfigDatabasePage()

