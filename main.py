import os
import sys

import dash
import dash_bootstrap_components as dbc
from dash import html

sys.path.append('/local/projekte/UX-EES-TSFW/TestPc/TestFrameWork/TestFrameWork')
sys.path.append('/local/projekte/UX-EES-TSFW/TestPc/TestFrameWork/UltraTorkWeb')
sys.path.append('/local/projekte/UX-EES-TSFW/TestPc/TestFrameWork')

import UltraTorkWebIf

from UltraTorkWebGuiIf import UltraTorkWebGuiIf
from TestFrameWorkPara import readParameter

path, filename = os.path.split(os.path.abspath(__file__))

TcStepPath = path + "/static/tcdata"
if os.path.isdir(TcStepPath):
    for filename in os.listdir(TcStepPath):
        if filename.find(".png") != -1:
            os.remove(TcStepPath + "/" + filename)

PARAMETERLIST = readParameter(path + "/UltraTorkWebConfig.json")

WebIf = UltraTorkWebIf.UltraTorkWebIf(TcStepPath,
                                      True,
                                      PARAMETERLIST["DBType"],
                                      PARAMETERLIST["DBHost"],
                                      PARAMETERLIST["DBUserName"],
                                      PARAMETERLIST["DBPassword"])

GuiDataClass = UltraTorkWebGuiIf()
GuiDataClass.setParameterList(PARAMETERLIST, WebIf)
WebIf.addTcListConfigPara(PARAMETERLIST)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN], use_pages=True, suppress_callback_exceptions=True)

app.layout = html.Div([
    dbc.Card([
        dbc.CardBody([
            dash.page_container
        ])
    ])
])



if __name__ == "__main__":
    app.run_server(port=8888, debug=True)




