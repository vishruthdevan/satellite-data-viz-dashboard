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


data['Date of Launch'] = pd.to_datetime(
    data['Date of Launch'], errors='coerce').dt.strftime('%d-%m-%Y')
data['Date of Launch'] = data['Date of Launch'].map(lambda x: str(x)[-4:])
data_contractors = data['Contractor'].value_counts().reset_index(name='Counts')
data_contractors.columns = ['Contractor', 'Counts']
data_contractors.sort_values(by='Counts', ascending=False, inplace=True,)
top_contractors = data_contractors['Contractor'].head(6).to_list()
data_contractors_date = data[[
    'Date of Launch', 'Contractor']].value_counts().reset_index(name='Counts')
data_contractors_date.sort_values(by='Date of Launch', inplace=True,)
data_contractors_date = data_contractors_date[data_contractors_date['Contractor'].isin(
    top_contractors)]
fig3 = px.line(
    data_contractors_date,
    x="Date of Launch",
    y="Counts",
    color='Contractor',
    markers=True,
    title="Trends in number of satellites launched by each contractor")
fig3.update_layout(
    margin=dict(l=10, r=10, t=50, b=10),
    paper_bgcolor="papayawhip",
    title=dict(x=0.5))

data_orbit = data['Type of Orbit']
data_orbit = data_orbit.value_counts().reset_index(name='Count')
data_orbit.columns = ['Type of Orbit', 'Count']
descriptions = [r"A non-inclined orbit is an orbit coplanar with a plane of reference. <br>The orbital inclination is 0?? for prograde orbits, and ?? (180??) for retrograde ones.<br> If the plane of reference is a massive spheroid body's equatorial plane, <br>these orbits are called equatorial; if the plane of reference <br>is the ecliptic plane, they are called ecliptic. ",
                r"A Sun-synchronous orbit (SSO), also called a heliosynchronous orbit, <br> is a nearly polar orbit around a planet, in which the satellite passes over any <br>given point of the planet's surface at the same local mean solar time.",
                r"A polar orbit is one in which a satellite passes above or nearly above<br> both poles of the body being orbited (usually a planet such as the Earth, but possibly<br> another body such as the Moon or Sun) on each revolution. It has an <br>inclination of about 60 - 90 degrees to the body's equator.[1] A <br>satellite in a polar orbit will pass over the equator at a different longitude <br>on each of its orbits. ",
                r"A near-equatorial orbit is an orbit that lies close to the equatorial <br>plane of the object orbited. Such an orbit has an inclination near 0??. On Earth, such <br>orbits lie on the celestial equator, the great circle of the imaginary <br>celestial sphere on the same plane as the equator of Earth",
                r"A Molniya orbit is a type of satellite orbit designed to provide communications <br>and remote sensing coverage over high latitudes. It is a highly elliptical <br>orbit with an inclination of 63.4 degrees, an argument of perigee of 270 <br>degrees, and an orbital period of approximately half a sidereal <br>day.",
                r"A deep highly eccentric orbit (HEO) is an elliptic orbit with high eccentricity, <br>usually referring to one around Earth. Examples of inclined HEO orbits <br>include Molniya orbits, named after the Molniya Soviet communication satellites<br> which used them, and Tundra orbits. ",
                r"In astrodynamics or celestial mechanics, an elliptic orbit or elliptical orbit <br>is a Kepler orbit with an eccentricity of less than 1; this includes the <br>special case of a circular orbit, with eccentricity equal to 0. In a stricter <br>sense, it is a Kepler orbit with the eccentricity greater than 0 <br>and less than 1 (thus excluding the circular orbit). In a wider sense, it is <br>a Kepler's orbit with negative energy. This includes the radial elliptic orbit, with eccentricity equal to 1. ",
                r"A synchronous orbit is an orbit in which an orbiting body (usually a satellite) <br>has a period equal to the average rotational period of the body being orbited<br> (usually a planet), and in the same direction of rotation as that body.[1] ",
                r"Cislunar is Latin for 'on this side of the moon' and generally refers to the <br>volume between Earth and the moon. Cislunar space includes LEO, Medium Earth <br>Orbit, GEO, as well as other orbits, such as Low Lunar Orbit and NRHO, the <br>intended orbit for the Gateway.28"]

data_orbit['Description'] = descriptions
fig4 = px.treemap(data_orbit, path=['Type of Orbit'],
                  values='Count',
                  color='Count',
                  color_continuous_scale='sunset',
                  title='Distribution of Type of Orbit',
                  hover_data=['Description']
                  )
fig4.update_layout(
    margin=dict(l=10, r=10, t=50, b=10),
    paper_bgcolor="aliceblue",
    title=dict(x=0.5))

countries = {}
for country in pycountry.countries:
    countries[country.name] = country.alpha_3


data_country = data['Country of Operator/Owner'].value_counts().reset_index(name='Count')
data_country.columns = ['Country of Operator/Owner', 'Count']

codes = [countries.get(country, country)
         for country in data_country['Country of Operator/Owner']]
data_country['iso_codes'] = codes
data_country['iso_codes'] = data_country['iso_codes'].replace(
    ['Russia', 'South Korea', 'Bolivia', 'Venezuela', 'Czech Republic', 'Laos', 'China/Sri Lanka'], ['RUS', 'KOR', 'BOL', 'VEN', 'CZE', 'LAO', 'LKA'])
data_country['percentile'] = data_country['Count'].rank(
    method='max').apply(lambda x: 100.0*(x-1)/(len(data_country)-1))


world_map1 = px.choropleth(data_country, locations="iso_codes",
                           color="Count",
                           color_continuous_scale="deep",
                           hover_data=['Country of Operator/Owner', 'Count'],
                           title="Number of satellites registered by each country",
                           height=600,
                           width=1500)

world_map1.update_layout(
    margin=dict(l=10, r=10, t=50, b=10),
    title=dict(x=0.5))


world_map2 = px.choropleth(data_country, locations="iso_codes",
                           color="percentile",
                           color_continuous_scale="deep",
                           range_color=(0, 100),
                           hover_data=['Country of Operator/Owner', 'Count'],
                           title="Number of satellites registered by each country (percentile)",
                           height=600,
                           width=1500)

world_map2.update_layout(
    margin=dict(l=10, r=10, t=50, b=10),
    title=dict(x=0.5))


@app.callback(
    Output('fig2', 'figure'),
    Input('bar-slider', 'value'))
def update_bar(value):
    fig2_ = px.bar(data_purpose[:value], x='Purpose', y="Counts",
                   color="Counts", title="Purpose of satellites")
    fig2_.update_layout(
        margin=dict(l=10, r=10, t=50, b=10),
        paper_bgcolor="#D6EAF8",
        title=dict(x=0.5))
    return fig2_


@app.callback(
    Output('world_map2', 'figure'),
    Input('world-map-toggle', 'value'))
def update_world(value):
    if value == False:
        return world_map2
    else:
        return world_map1


app.layout = html.Div(children=[
    html.H1(children='Satellite Data Dashboard', style={
            'textAlign': 'center', "font-family": "Arial"}),
    html.Div([
        html.Div([
            dcc.Graph(id='fig2', figure=fig2, style={
                'display': 'inline-block'}),
        ], style={'width': "100%"}),
        html.Div([
            dcc.Slider(min=3, max=9, step=3, value=3, id="bar-slider")
        ], style={'width': "80%"})
    ],
        style={'width': "50%", 'display': 'inline-block', "padding": "2rem 2rem"}
    ),
    dcc.Graph(id='fig1', figure=fig1, style={'display': 'inline-block'}),
    html.P(),
    html.Div([
        dcc.Graph(id='fig3', figure=fig3)]),
    html.P(),
    dcc.Graph(id='world_map2', figure=world_map2, style={
              "width": "1300px", "margin": "0 auto", "padding": "1rem 0rem"}),
    daq.ToggleSwitch(
        id='world-map-toggle',
        label='Percentile/Count',
        value=False,
        color="magenta",
    ),
    html.Div([
        dcc.Graph(id='fig4', figure=fig4)], style={"padding": "5rem 0rem"}),
])


if __name__ == '__main__':
    app.run_server(debug=True)
