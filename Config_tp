import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, html, callback, dcc, State
import json

from UltraTorkWebGuiIf import UltraTorkWebGuiIf

import os

GuiDataClass = UltraTorkWebGuiIf()

dash.register_page(__name__, path='/config_tp')


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

def SidebarMenu():
    offcanvas = dbc.Offcanvas(
        [
            html.Div([
                dbc.NavItem(dbc.NavLink(
                    [
                        html.I(className="bi bi-caret-right-fill me-2 "),
                        "Database Settings"
                    ],
                    href="/config_database"
                )),
                dbc.NavItem(dbc.NavLink(
                    [
                        html.I(className="bi bi-gear-fill me-2"),
                        "Testplace Configuration"
                    ],
                    href="/config_tp"
                )),
                dbc.NavItem(dbc.NavLink(
                    [
                        html.I(className="bi bi-pencil-square me-2"),
                        "Edit Testplace"
                    ],
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

def MenuConfigTp():
    TpList = GuiDataClass.getTpNameList()
    SelectedTp = GuiDataClass.getSelectedTpNameConfigPage()

    # Add an extra input field for Test Case Name (TCName) in MenuConfigTp function
    modal = html.Div(
        [
            dbc.Button(html.I(className="bi bi-funnel-fill"), id="open-centered", color="primary", outline=True,
                       style={'position': 'absolute', 'right': '10px', 'left': 'auto', 'top': '10px'}),
            dbc.Modal([
                dbc.ModalHeader(dbc.ModalTitle("Filter"), close_button=True),
                dbc.ModalBody([
                    html.Div([
                        dbc.Label("Testcases", width="auto", size="sm"),
                        dcc.Dropdown(
                            value=SelectedTp,
                            options=[{"label": i, "value": i} for i in TpList],
                            id="SelectedTpConfig"
                        ),
                    ]),
                ]),
                html.Br(),
                dbc.ModalBody([
                    html.Div([
                        dbc.Label("Create New TestCase", width="auto", size="sm"),
                        dbc.Row([
                            dbc.Col(dbc.Input(type="text", id="inputTC", placeholder="Enter Test Case Name")),
                            dbc.Col(dbc.Button("New TestCase", id="open-new-tp", color="primary", outline=True))
                        ])
                    ])

                ]),
                html.Br(),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close",
                        id="close-centered",
                        className="ms-auto",
                        n_clicks=0,
                    )
                ),
            ],
                id="modal-centered",
                centered=True,
                is_open=False,
            ),

        ],
    )

    @callback(
        Output("modal-centered", "is_open"),
        Output("inputTC", "value"),
        Output("SelectedTpConfig", "options"),
        [Input("open-centered", "n_clicks"), Input("close-centered", "n_clicks"),
         Input("open-new-tp", "n_clicks")],
        [State("modal-centered", "is_open"), State("SelectedTpConfig", "options"), State("inputTC", "value")],
    )


    def toggle_modal(n1, n2, n3, is_open, options, tc_value):
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
        if 'open-new-tp' in changed_id:
            # Clear input fields only for the new testcase, set modal to open, and add new option to dropdown menu
            new_option = {"label": tc_value or "New Testcase", "value": tc_value or "New Testcase"}
            new_options = options + [new_option]
            return True, tc_value, new_options
        elif n1 or n2:
            return not is_open, '', options
        return is_open, '', options

    return modal


def MainPage() -> html:

    newTpData = GuiDataClass.getTpConfigData()



    inputTP = dbc.Row([
        dbc.Label("Test Place Name", html_for="input-tp-row", width=2),
        dbc.Col(
            dbc.Input(type="text", id="inputTP", value=newTpData['TpName'], debounce=True),
            width=10,
        )
    ], className="mb-3")

    inputAppendix = dbc.Row([
        dbc.Label("Anlagen", html_for="input-appendix-row", width=2),
        dbc.Col(
            dbc.Input(type="text", id="inputAppendix", value=newTpData['Appendix'], debounce=True),
            width=10,
        )
    ], className="mb-3")

    inputTestdata = dbc.Row([
        dbc.Label("Testdata", html_for="input-testdata-row", width=2),
        dbc.Col(
            dbc.Input(type="text", id="inputTestdata", value=newTpData['TestData'], debounce=True),
            width=10,
        )
    ], className="mb-3")

    inputTpPath = dbc.Row([
        dbc.Label("Testplatz-Pfad", html_for="input-path-row", width=2),
        dbc.Col(
            dbc.Input(type="text", id="inputTpPath", value=newTpData['Path'], debounce=True),
            width=10,
        )
    ], className="mb-3")

    inputDbPath = dbc.Row([
        dbc.Label("Databank-Pfad", html_for="input-db-path-row", width=2),
        dbc.Col(
            dbc.Input(type="text", id="inputDbPath", value=newTpData['DBPath'], debounce=True),
            width=10,
        )
    ], className="mb-3")

    inputConfig = dbc.Row([
        dbc.Label("Konfiguration", html_for="input-configuration-row", width=2),
        dbc.Col(
            dbc.Input(type="text", id="inputConfig", value=newTpData['Config'], debounce=True),
            width=10,
        )
    ], className="mb-3")

    inputOutput = dbc.Row([
        dbc.Label("Ausgabedatei", html_for="input-output-row", width=2),
        dbc.Col(
            dbc.Input(type="text", id="inputOutput", value=newTpData['Outputfile'], debounce=True),
            width=10,
        )
    ], className="mb-3")

    inputDataPath = dbc.Row([
        dbc.Label("Daten Pfad", html_for="input-data-path-row", width=2),
        dbc.Col(
            dbc.Input(type="text", id="inputDataPath", value=newTpData['DataPath'], debounce=True),
            width=10,
        )
    ], className="mb-3")

    inputWorkspace = dbc.Row([
        dbc.Label("Arbeitsbereich", html_for="input-workspace-row", width=2),
        dbc.Col(
            dbc.Input(type="text", id="inputWorkspace", value=newTpData['Workspace'], debounce=True),
            width=10,
        )
    ], className="mb-3")

    inputXMLOutput = dbc.Row([
        dbc.Label("XML Output Pfad", html_for="input-xml-output-row", width=2),
        dbc.Col(
            dbc.Input(type="text", id="inputXMLOutput", value=newTpData['XmlOutputPath'], debounce=True),
            width=10,
        )
    ], className="mb-3")

    submit = dbc.Row([
        dbc.Col(
            dbc.Button('Submit', color='primary', id='button-submit', n_clicks=0),
            id='div-button',
            width=2,
        ),
        dbc.Col(width=10)
    ], className="mb-3")

    tab1_content = [
        inputTP,
        inputAppendix,
        inputTestdata,
        inputTpPath,
        inputDbPath,
        inputConfig,
        inputOutput,
        inputDataPath,
        inputWorkspace,
        inputXMLOutput,
        submit
    ]

    tab2_content = [
        html.Thead([
            html.Tr([
                html.Th(
                    dbc.InputGroup([
                        dbc.Button("Verbose", id="input-save-actor", n_clicks=0),
                        dcc.Dropdown(['false', 'true'], 'false', id='demo-verbose', style={'width': '100%'})
                    ]), style={'width': '20%'}
                ),
                html.Th(
                    dbc.InputGroup([
                        dbc.Button("BatchMode", id="input-save-batch", n_clicks=0),
                        dcc.Dropdown(['false', 'true'], 'false', id='demo-batch', style={'width': '100%'})
                    ]), style={'width': '20%'}
                ),
                html.Th(
                    dbc.InputGroup([
                        dbc.Button("TPApache2", id="input-save-apache", n_clicks=0),
                        dcc.Dropdown(['false', 'true'], 'false', id='demo-dropdown', style={'width': '100%'})
                    ]), style={'width': '20%'}
                ),
                html.Th(
                    dbc.InputGroup([
                        dbc.Button("Abortlevel", id="input-save-abort", n_clicks=0),
                        dcc.Dropdown(['1', '2', '3', '4', '5'], '3', id='demo-abort', style={'width': '100%'})
                    ]), style={'width': '20%'}
                ),
            ]),
            html.Tr([
                html.Th(
                    dbc.InputGroup([
                        dbc.Button("State", id="input-save-state", n_clicks=0),
                        dcc.Dropdown(
                            options=[{'label': i, 'value': i} for i in ['implemented', 'reviewed', 'tested']],
                            value='implemented', id='demo-state', style={'width': '100%'}
                        )
                    ]), style={'width': '25%'}
                ),
                html.Th(
                    dbc.InputGroup([
                        dbc.Button("Debug", id="input-save-verbose", n_clicks=0),
                        dcc.Dropdown(
                            options=[{'label': str(i), 'value': str(i)} for i in range(1, 6)],
                            value='3', id='demo-debug', style={'width': '100%'}
                        )
                    ]), style={'width': '15%'}
                ),
                html.Th(
                    dbc.InputGroup([
                        dbc.Button("ActorTable", id="input-save-actor", n_clicks=0),
                        dcc.Dropdown(
                            options=[{'label': i, 'value': i} for i in ['Default', 'Param1', 'Param2']],
                            value='Default', id='demo-actor', style={'width': '100%'}
                        )
                    ]), style={'width': '25%'}
                ),
            ], style={'margin-top': '30px'}),
            html.Tr([
                html.Th(
                    dbc.Button("Save ", id="save-parameters", color="success", n_clicks=0, className="mt-3"),
                    colSpan=4, style={'text-align': 'center'}
                )
            ])
        ])
    ]

    tabs = dbc.Tabs([
        dbc.Tab(label="TP Input", tab_id="tab1", children=[
            dbc.Table(striped=True, bordered=True, hover=True, children=[
                html.Tbody(tab1_content)
            ]),
        ]),
        dbc.Tab(label="TP Parameter", tab_id="tab2", children=[
            dbc.Table(striped=True, bordered=True, hover=True, children=tab2_content),
        ]),
    ], active_tab="tab1")

    # Build the layout
    layout = dbc.Form([
        tabs
    ])

    return dbc.CardBody(layout)


def ConfigTpPage():
    layout = html.Div([
        # Include Bootstrap Icons CDN link
        html.Link(href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.9.0/font/bootstrap-icons.css",
                  rel="stylesheet"),

        # Sidebar
        html.Div(id="sidebar", style=SIDEBAR_STYLE, children=[
            dbc.Row(
                [
                    dbc.Col(html.Img(src="/static/images/ultratronikLogoU.png", height="30px"), width="auto"),
                    dbc.Col(dbc.NavbarBrand("UltraTorkWeb", className="ms-2")),
                    dbc.Col(html.Hr(), width="100%"),  # Horizontal line
                ],
                align="center",
                className="g-0"
            ),
            SidebarMenu()  # Include Sidebar content
        ]),

    ])

    page = dbc.Card([
        dbc.CardHeader([
            html.H2("Testplace configuration"),
        ]),
        dbc.CardBody(
            MenuConfigTp()
        ),
        dbc.CardBody(
            MainPage()
        ),

    ])

    grid = html.Div([
        dbc.Row([
            dbc.Col([(layout)], width=3),
            dbc.Col(page),
        ]),
    ])

    return grid


layout = html.Div(ConfigTpPage(), id="TpConfigSettings")


@callback(
    [Output('TpConfigSettings', 'children'),
     Output('SelectedTpConfig', 'value')],  # Add Output for resetting dropdown
    Input('SelectedTpConfig', 'value')
)
def render_page_content(TpName):

    GuiDataClass.setSelectedTpNameConfigPage(TpName)

    return ConfigTpPage(), None

@callback(
    Output('div-button', 'children'),
    Input('button-submit', 'n_clicks'),
    State('inputTP', 'value'),
    State('inputAppendix', 'value'),
    State('inputTestdata', 'value'),
    State('inputTpPath', 'value'),
    State('inputDbPath', 'value'),
    State('inputConfig', 'value'),
    State('inputOutput', 'value'),
    State('inputDataPath', 'value'),
    State('inputWorkspace', 'value'),
    State('inputXMLOutput', 'value'),
    State('inputTC', 'value')  # Add State for the new test case name input field
)
def write_tp_name_value(n, TpName, Appendix, Testdata, TpPath, DbPath, Config, Output, DataPath, Workspace, XMLOutput, TCName):

    if n:
        # Create dictionary with all the data
        testcase_data = {
            "TpName": TpName,
            "Appendix": Appendix,
            "Testdata": Testdata,
            "TpPath": TpPath,
            "DbPath": DbPath,
            "Config": Config,
            "Output": Output,
            "DataPath": DataPath,
            "Workspace": Workspace,
            "XMLOutput": XMLOutput
        }

        # Load existing test cases from JSON file or create an empty dictionary if the file doesn't exist or is empty
        try:
            with open('UltraTorkWebConfig.json', 'r') as json_file:
                testcases = json.load(json_file)
        except (FileNotFoundError, json.JSONDecodeError):
            testcases = {}

        # Check if the test case already exists
        if TpName not in testcases:
            # Add the new test case with the specified name
            testcases[TCName] = testcase_data

            # Save updated test cases to JSON file
            with open('UltraTorkWebConfig.json', 'w') as json_file:
                json.dump(testcases, json_file, indent=4)

            # Provide feedback to the user
            return [html.Div("New test case '{}' added and saved to UltraTorkWebConfig".format(TCName))]
        else:
            # Test case already exists, provide feedback to the user
            return [html.Div("Test case '{}' already exists in UltraTorkWebConfig".format(TpName))]

    return [dbc.Button('Submit', color='primary', id='button-submit', n_clicks=0)]


