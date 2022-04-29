from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

data = pd.read_excel('data.xlsx', sheet_name='Database')
app = Dash()

data_users = data['Users'].value_counts().reset_index(name='Counts')
data_users.columns = ['Users', 'Counts']
fig1 = px.pie(
   data_users, 
   names='Users', 
   values="Counts", 
   color="Counts",
   title="Distribution of Users")


if __name__ == '__main__':
    app.run_server(debug=True)