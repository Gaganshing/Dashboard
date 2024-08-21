import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, html, callback, dcc, State
import plotly.express as px
import plotly.graph_objects as go
from datetime import date

from UltraTorkWebGuiIf import UltraTorkWebGuiIf

# Initialize the data interface class
GuiDataClass = UltraTorkWebGuiIf()

# Register the page for Dash
dash.register_page(__name__, path='/')

# Define styles for the sidebar and main content
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


def create_sidebar():
    """Create the sidebar layout with improved styling."""
    offcanvas = dbc.Offcanvas(
        [
            dbc.NavItem(dbc.NavLink(
                [html.I(className="bi bi-caret-right-fill me-2"), "Database Settings"],
                href="/config_database",
                id="database-settings-link"
            )),
            dbc.Tooltip("Configure database settings", target="database-settings-link"),

            dbc.NavItem(dbc.NavLink(
                [html.I(className="bi bi-gear-fill me-2"), "Testplace Configuration"],
                href="/config_tp",
                id="testplace-config-link"
            )),
            dbc.Tooltip("Configure testplaces", target="testplace-config-link"),

            dbc.NavItem(dbc.NavLink(
                [html.I(className="bi bi-pencil-square me-2"), "Edit Testplace"],
                href="/impl",
                id="edit-testplace-link"
            )),
            dbc.Tooltip("Edit testplaces", target="edit-testplace-link"),
        ],
        id="offcanvas",
        title="Testing Menu",
        is_open=False,
        style={"background-color": "#343a40", "color": "#ffffff"}  # Darker offcanvas
    )

    TpList = GuiDataClass.getTpNameList()
    TpListData = dcc.Dropdown(
        options=[{"label": i, "value": i} for i in TpList],
        id="graph-tp-name-dropdown",
        multi=True,
        placeholder="Select Testplaces",
        style={"border-radius": "15px", "padding": "5px", "background-color": "#f0f0f0",
               "color": "#333333"}  # Slightly off-white for better visibility
    )

    sidebar = html.Div(
        [
            html.Img(src="/static/images/ultratronikLogoU.png", height="60px", style={"margin-bottom": "20px"}),
            dbc.NavbarBrand("UltraTorkWeb", className="ms-2", style={"font-size": "21px", "font-weight": "bold"}),
            dbc.Nav(
                [
                    dbc.NavLink("Dashboard", href="/", className="bi bi-house", id="dashboard-link"),
                    dbc.Tooltip("Go to the dashboard", target="dashboard-link"),

                    dbc.NavLink("Testing Menu", href="/", id="open-offcanvas", className="bi bi-geo-alt", active=True),
                    dbc.Tooltip("Open testing menu", target="open-offcanvas"),

                    dbc.NavLink("Documentation", href="/documentation", className="bi bi-pen", id="documentation-link"),
                    dbc.Tooltip("View documentation", target="documentation-link"),
                ],
                vertical=True,
                pills=True,
            ),
            offcanvas,
            html.Div(
                [
                    dbc.Label("Select Testplaces"),
                    TpListData,
                    dbc.Button("Update Graph", id="update-graph-button", color="primary", className="mt-2",
                               style={"border-radius": "20px"}),
                    dbc.Tooltip("Update the graphs with selected testplaces", target="update-graph-button"),

                    dbc.Button("Clear Selection", id="clear-selection-button", color="dark", className="mt-2",
                               style={"border-radius": "20px"}),
                    dbc.Tooltip("Clear the selected testplaces", target="clear-selection-button")
                ],
                className="mt-4"
            )
        ],
        style=SIDEBAR_STYLE,
    )

    return sidebar


def create_graph_page():
    """Create the graph page layout."""
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Loading(dcc.Graph(id="combined-bar-graph")),
                            dcc.Loading(dcc.Graph(id="combined-pie-chart")),
                            dcc.Loading(dcc.Graph(id="line-graph"))  # New line graph
                        ],
                        width=9
                    )
                ]
            )
        ]
    )


def create_status_cards(pass_count, fail_count, error_count, tc_count, app_count, sop_count):
    """Create status cards to show pass, fail, and error counts."""
    return dbc.Row(
        [
            create_status_card("Total Pass", pass_count, "success"),
            create_status_card("Total Fail", fail_count, "danger"),
            create_status_card("Total Errors", error_count, "warning"),
            create_status_card("Total TC-Errors", tc_count, "info"),
            create_status_card("Total App-Errors", app_count, "warning"),
            create_status_card("Total SOP-Errors", sop_count, "dark")
        ]
    )


def create_status_card(title, count, color):
    """Helper function to create individual status card."""
    return dbc.Col(
        dbc.Card(
            dbc.CardBody(
                [html.H4(title, className="card-title"), html.P(f"{count}", className="card-text")],
            ),
            color=color,
            inverse=True
        ),
        width=4
    )


@callback(
    Output("offcanvas", "is_open"),
    [Input("open-offcanvas", "n_clicks")],
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n, is_open):
    return not is_open if n else is_open


@callback(
    Output('graph-tp-name-dropdown', 'value'),
    [Input('clear-selection-button', 'n_clicks')]
)
def clear_dropdown(n_clicks):
    return [] if n_clicks else dash.no_update


@callback(
    [Output('combined-bar-graph', 'figure'),
     Output('combined-pie-chart', 'figure'),
     Output('line-graph', 'figure'),  # Output for line graph
     Output('status-cards', 'children')],
    [Input('update-graph-button', 'n_clicks')],
    [State('graph-tp-name-dropdown', 'value')]
)
def update_combined_graphs(n_clicks, selected_tp_names):
    if not selected_tp_names:
        empty_fig = px.pie(names=['No Data'], values=[1], title="No Testplaces Selected")
        return empty_fig, empty_fig, empty_fig, create_status_cards(0, 0, 0, 0, 0, 0)

    data = {'Date': [], 'Result Type': [], 'Count': [], 'Testplace': []}
    aggregate_data = {'Result Type': ['PASS', 'FAIL', 'ERROR', 'TC-Error', 'App-Error', 'Sop-Error'],
                      'Count': [0, 0, 0, 0, 0, 0]}

    line_data = {'Date': [], 'Count': [], 'Testplace': []}  # Data for the line graph

    try:
        for tp_name in selected_tp_names:
            GuiDataClass.setResultDataFilterTpName(tp_name)
            ResultTcList = GuiDataClass.getTcResultList()

            daily_counts = {}
            for ResultTc in ResultTcList:
                date_str = ResultTc[0].split(" ")[0]
                if date_str not in daily_counts:
                    daily_counts[date_str] = {'PASS': 0, 'FAIL': 0, 'ERROR': 0, 'TC-Error': 0, 'App-Error': 0,
                                              'Sop-Error': 0}

                for result in ResultTc[1]:
                    result_type = result[7]
                    if result_type == "PASS":
                        daily_counts[date_str]['PASS'] += 1
                    elif result_type == "FAIL":
                        daily_counts[date_str]['FAIL'] += 1
                    elif result_type == "TC_FAIL":
                        daily_counts[date_str]['TC-Error'] += 1
                    elif result_type == "APP_ERROR":
                        daily_counts[date_str]['App-Error'] += 1
                    elif result_type == "SPORADIC_BEHAVIOR":
                        daily_counts[date_str]['Sop-Error'] += 1
                    else:
                        daily_counts[date_str]['ERROR'] += 1

            for date, counts in daily_counts.items():
                data['Date'].extend([date] * 6)
                data['Result Type'].extend(['PASS', 'FAIL', 'ERROR', 'TC-Error', 'App-Error', 'Sop-Error'])
                data['Count'].extend(
                    [counts['PASS'], counts['FAIL'], counts['ERROR'], counts['TC-Error'], counts['App-Error'],
                     counts['Sop-Error']])
                data['Testplace'].extend([tp_name] * 6)

                aggregate_data['Count'][0] += counts['PASS']
                aggregate_data['Count'][1] += counts['FAIL']
                aggregate_data['Count'][2] += counts['ERROR']
                aggregate_data['Count'][3] += counts['TC-Error']
                aggregate_data['Count'][4] += counts['App-Error']
                aggregate_data['Count'][5] += counts['Sop-Error']

                # Prepare data for the line graph
                for result_type in ['PASS', 'FAIL', 'ERROR', 'TC-Error', 'App-Error', 'Sop-Error']:
                    line_data['Date'].extend([date] * len(selected_tp_names))
                    line_data['Count'].extend([counts[result_type]] * len(selected_tp_names))
                    line_data['Testplace'].extend([tp_name] * len(selected_tp_names))

    except Exception as e:
        print(f"An error occurred: {e}")
        return px.bar(title="Error"), px.pie(title="Error"), px.line(title="Error"), create_status_cards(0, 0, 0, 0, 0,
                                                                                                         0)

    combined_bar_fig = px.bar(
        data_frame=data,
        x='Date',
        y='Count',
        color='Result Type',
        barmode='group',
        title="Combined Testplace Results by Date",
        text='Testplace'
    )

    combined_bar_fig.update_layout(
        yaxis_title='Count',
        xaxis_title='Date',
        legend_title_text='Result Type',
        xaxis=dict(tickmode='linear'),
        barmode='group',
        plot_bgcolor='#f4f4f4',  # Light background
        paper_bgcolor='#ffffff'  # White background
    )

    combined_pie_fig = px.pie(
        data_frame=aggregate_data,
        names='Result Type',
        values='Count',
        title="Aggregate Results"
    )

    # Line graph to show trends over time
    line_fig = px.line(
        data_frame=line_data,
        x='Date',
        y='Count',
        color='Testplace',
        title="Trend of Results Over Time",
        markers=True
    )

    line_fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Count',
        plot_bgcolor='#f4f4f4',  # Light background
        paper_bgcolor='#ffffff'  # White background
    )

    status_cards = create_status_cards(
        aggregate_data['Count'][0],
        aggregate_data['Count'][1],
        aggregate_data['Count'][2],
        aggregate_data['Count'][3],
        aggregate_data['Count'][4],
        aggregate_data['Count'][5]
    )

    return combined_bar_fig, combined_pie_fig, line_fig, status_cards


def create_index_page():
    """Create the main index page layout."""
    return html.Div(
        [
            html.Link(href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.9.0/font/bootstrap-icons.css",
                      rel="stylesheet"),
            html.Div(id="sidebar", children=create_sidebar()),
            html.Div(id="page-content", style=CONTENT_STYLE, children=[
                dbc.Card(
                    [
                        dbc.CardHeader(html.H2("Overview of the Project")),
                        dbc.CardBody(
                            [
                                html.Div(id='status-cards'),
                                create_graph_page()
                            ]
                        )
                    ]
                )
            ])
        ]
    )


# Define the main layout of the app
layout = create_index_page()

