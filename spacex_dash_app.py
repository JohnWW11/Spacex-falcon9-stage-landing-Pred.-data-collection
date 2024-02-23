# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into a pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a Dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # TASK 1: Add a dropdown list to enable Launch Site selection
    # The default select value is for ALL sites
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
        ],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    
    html.Br(),
    # Rest of your layout components...
])
                               

# TASK 2: Add a pie chart to show the total successful launches count for all sites
# If a specific launch site was selected, show the Success vs. Failed counts for the site
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        counts = filtered_df.groupby('Launch Site')['class'].sum().reset_index()
        fig = px.pie(counts, values='class', names='Launch Site', title='Total Success Launches by Site')
        return fig
    else:
        data = filtered_df.loc[filtered_df['Launch Site'] == entered_site, ['Launch Site', 'class']]
        counts = data['class'].value_counts(normalize=True)
        fig = px.pie(counts, values=counts.values, names=counts.index, title=f"Total Success Launches for site {entered_site}")
        return fig

                             
# TASK 3: Add a slider to select payload range
#dcc.RangeSlider(id='payload-slider',...)
dcc.RangeSlider(
    id='id',
    min=0,
    max=10000,
    step=1000,
    marks={0: '0', 100: '100'},
    value=[min_payload, max_payload]
)



# TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")]
)
def get_scatter_chart(entered_site, payload_range):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        data = filtered_df[['Payload Mass (kg)', 'class', 'Booster Version Category']].copy()
        data1 = data[(data['Payload Mass (kg)'] >= payload_range[0]) & (data['Payload Mass (kg)'] <= payload_range[1])]
        fig = px.scatter(data1, x="Payload Mass (kg)", y="class", color="Booster Version Category")
        return fig
    else:
        data = filtered_df.loc[filtered_df['Launch Site'] == entered_site, ['Payload Mass (kg)', 'class', 'Booster Version Category']]
        data1 = data[(data['Payload Mass (kg)'] >= payload_range[0]) & (data['Payload Mass (kg)'] <= payload_range[1])]
        fig = px.scatter(data1, x="Payload Mass (kg)", y="class", color="Booster Version Category")
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
