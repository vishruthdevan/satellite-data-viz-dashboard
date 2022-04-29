from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

data = pd.read_excel('data.xlsx', sheet_name='Database')
app = Dash()

if __name__ == '__main__':
    app.run_server(debug=True)