from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import pycountry
import dash_daq as daq

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
fig1.update_traces(textposition='inside')
fig1.update_layout(
   uniformtext_minsize=12, 
   uniformtext_mode='hide',
   margin=dict(l=10, r=10, t=50, b=10),
   paper_bgcolor="mintcream",
   title=dict(x=0.5))

data_purpose = data['Purpose'].value_counts().reset_index(name='Counts')
data_purpose.columns = ['Purpose', 'Counts']
fig2 = px.bar(
   data_purpose[:5], 
   x='Purpose', 
   y="Counts", 
   color="Counts", 
   title="Purpose of satellites")
fig2.update_layout(
   margin=dict(l=10, r=10, t=50, b=10),
   paper_bgcolor="#D6EAF8",
   title=dict(x=0.5))


if __name__ == '__main__':
    app.run_server(debug=True)