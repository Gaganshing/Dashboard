import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State, callback, ALL
from UltraTorkWebGuiIf import UltraTorkWebGuiIf
from datetime import date, datetime

# Initialize the GUI data interface
GuiDataClass = UltraTorkWebGuiIf()

# Register the page for Dash
dash.register_page(__name__, path='/impl')

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

# Function to create the filter modal
def create_filter_modal():
    tp_list = GuiDataClass.getTpNameList()
    selected_tp = GuiDataClass.getTpSelectedTp()

    tp_dropdown = dcc.Dropdown(
        value=selected_tp,
        options=[{"label": i, "value": i} for i in tp_list],
        id="inlineFormTpName",
    )

    result_filter_dropdown = dcc.Dropdown(
        id='result-filter',
        options=[
            {'label': 'ALL', 'value': 'ALL'},
            {'label': 'PASS', 'value': 'PASS'},
            {'label': 'FAIL', 'value': 'FAIL'},
            {'label': 'OTHER', 'value': 'OTHER'}
        ],
        value='ALL'
    )
    date_picker = dcc.DatePickerRange(
        id='date-picker-range',
        start_date=date(2024, 7, 21).strftime('%Y-%m-%d'),  # Default start date
        end_date=date(2024, 7, 25).strftime('%Y-%m-%d'),  # Default end date
        display_format='YYYY-MM-DD'  # Format to display the dates
    )

    modal = html.Div(
        [
            dbc.Button(html.I(className="bi bi-funnel-fill"), id="open-centered", color="primary", outline=True,
                       style={'position': 'absolute', 'right': '10px', 'top': '10px'}),
            dbc.Modal([
                dbc.ModalHeader(dbc.ModalTitle("Filter"), close_button=True),
                dbc.ModalBody([
                    html.Div([
                        dbc.Label("Testcases Name", width="auto", size="sm"),
                        tp_dropdown,
                        dbc.Label("Result Filter", width="auto", size="sm"),
                        result_filter_dropdown,
                        dbc.Label("Date Range", width="auto", size="sm"),
                        date_picker
                    ]),
                ]),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close-centered", className="ms-auto", n_clicks=0)
                ),
            ],
                id="modal",
                is_open=False,
            ),
        ],
    )

    @callback(
        Output("modal", "is_open"),
        [Input("open-centered", "n_clicks"), Input("close-centered", "n_clicks")],
        [State("modal", "is_open")],
    )
    def toggle_modal(open_clicks, close_clicks, is_open):
        if open_clicks or close_clicks:
            return not is_open
        return is_open

    return modal

# Function to create the content for the main page
def create_main_page_content(ResultTcList):
    # Initialize counts
    pass_count = 0
    fail_count = 0
    other_count = 0

    table1_row = []
    table2_row = []

    for ResultTc in ResultTcList:
        for i, result in enumerate(ResultTc[1]):
            result_type = result[7]
            if result_type == "PASS":
                pass_count += 1
            elif result_type == "FAIL":
                fail_count += 1
            else:
                other_count += 1

            button_color = 'success' if result_type == "PASS" else 'danger' if result_type == "FAIL" else 'warning'
            button_label = result_type

            row1 = html.Tr([
                html.Td(str(i)),
                html.Td(result[2]),
                html.Td(result[3]),
                html.Td(result[6]),
                html.Td(result[8]),
                dbc.Button(button_label, color=button_color, size="sm", id={'type': 'result-button', 'index': i})
            ])
            table1_row.append(row1)

            row2 = html.Tr([
                html.Td(str(i)),
                html.Td(result[2]),
                html.Td(result[4]),
                html.Td(result[5]),
                html.Td(result[6]),
                html.Td(result[8]),
                dbc.Button(button_label, color=button_color, size="sm", id={'type': 'result-button', 'index': i})
            ])
            table2_row.append(row2)

    status_bar = dbc.Alert(
        f"Total: {pass_count + fail_count + other_count} | Pass: {pass_count} | Fail: {fail_count} | Other: {other_count}",
        color="info"
    )

    table1_header = [
        html.Thead(html.Tr([
            html.Th("Nr.", style={'width': '2%'}),
            html.Th("Name", style={'width': '60%'}),
            html.Th("SW Version", style={'width': '10%'}),
            html.Th("Runtime", style={'width': '10%'}),
            html.Th("Try", style={'width': '8%'}),
            html.Th("Result", style={'width': '10%'}),
        ]))
    ]

    tab1_layout = dbc.Table(table1_header + [html.Tbody(table1_row)], striped=True, bordered=True, hover=True)

    tab1_content = dbc.Card(
        dbc.CardBody([
            status_bar,
            tab1_layout
        ]),
        className="mt-3",
    )

    table2_header = [
        html.Thead(html.Tr([
            html.Th("Nr.", style={'width': '2%'}),
            html.Th("Name", style={'width': '50%'}),
            html.Th("Start", style={'width': '10%'}),
            html.Th("End", style={'width': '10%'}),
            html.Th("Runtime", style={'width': '7%'}),
            html.Th("Try", style={'width': '7%'}),
            html.Th("Result", style={'width': '4%'}),
        ]))
    ]

    tab2_layout = dbc.Table(table2_header + [html.Tbody(table2_row)], striped=True, bordered=True, hover=True)

    tab2_content = dbc.Card(
        dbc.CardBody([
            status_bar,
            tab2_layout
        ]),
        className="mt-3",
    )

    tabs = dbc.Tabs([
        dbc.Tab(tab1_content, label="Testplace List", tab_id="tab1"),
        dbc.Tab(tab2_content, label="Testplace Time", tab_id="tab2"),
    ], active_tab="tab1")

    detailed_info_tab = dbc.Tab(
        html.Div(id='detailed-info'), label="Detailed Info", tab_id="tab-detailed-info"
    )

    main_tabs = dbc.Tabs([
        dbc.Tab(tabs, label="Tables", tab_id="tab-tables"),
        detailed_info_tab
    ], id="main-tabs", active_tab="tab-tables")

    layout = dbc.Form([
        main_tabs
    ])

    return dbc.CardBody(layout)

# Function to create the base layout of the page
def create_impl_base_page(ResultTcList):
    layout = html.Div(
        [
            html.Link(href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.9.0/font/bootstrap-icons.css", rel="stylesheet"),
            html.Div(id="sidebar", style=SIDEBAR_STYLE, children=create_sidebar()),
            html.Div(id="page-content", style=CONTENT_STYLE, children=[
                dbc.Card(
                    [
                        dbc.CardHeader(html.H2("Edit Testplace")),
                        dbc.CardBody(create_filter_modal()),
                        dbc.CardBody(create_main_page_content(ResultTcList))
                    ]
                )
            ])
        ]
    )
    return layout

# Define the layout for the page
layout = html.Div(create_impl_base_page([]), id="TcImplementationListChanged")

# Callback to update the page content based on the selected test place and result filter
@callback(
    Output('TcImplementationListChanged', 'children'),
    [Input('inlineFormTpName', 'value'), Input('result-filter', 'value'),
     Input('date-picker-range', 'start_date'), Input('date-picker-range', 'end_date')]
)
def update_page_content(tp_name, result_filter, start_date, end_date):
    GuiDataClass.setResultDataFilterTpName(tp_name)
    ResultTcList = GuiDataClass.getTcResultList()

    if not start_date or not end_date:
        start_date = datetime.min.strftime('%Y-%m-%d')
        end_date = datetime.max.strftime('%Y-%m-%d')

    filtered_results = []
    for ResultTc in ResultTcList:
        test_date_str = ResultTc[0]
        test_date = datetime.strptime(test_date_str, "%Y-%m-%d %H:%M:%S,%f").date()

        if not (start_date <= test_date_str[:10] <= end_date):
            continue

        results = ResultTc[1]
        if result_filter and result_filter != 'ALL':
            results = [r for r in results if r[7] == result_filter.upper()]
        filtered_results.append([ResultTc[0], results])

    return create_impl_base_page(filtered_results)

# Callback to display detailed information based on the clicked result button
@callback(
    [Output('main-tabs', 'active_tab'), Output('detailed-info', 'children')],
    [Input({'type': 'result-button', 'index': ALL}, 'n_clicks')],
    [State({'type': 'result-button', 'index': ALL}, 'id')]
)
def display_detailed_info(n_clicks, ids):
    ctx = dash.callback_context

    if not ctx.triggered:
        return dash.no_update, dash.no_update

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    button_index = eval(button_id)['index']

    ResultTcList = GuiDataClass.getTcResultList()
    result_details = None
    count = 0
    for ResultTc in ResultTcList:
        result = ResultTcList[0]

    for ResultTc in ResultTcList:
        if count + len(ResultTc[1]) > button_index:
            result_details = ResultTc[1][button_index - count]
            break
        count += len(ResultTc[1])

    detailed_info = html.Div([
        html.H4(f"Details for Test Case: {result_details[2]}"),
        html.P(f"Date: {result[0]}"),
        html.P(f"Runtime: {result_details[6]}"),
        html.P(f"Result: {result_details[7]}"),
    ])
    return 'tab-detailed-info', detailed_info
