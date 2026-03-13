# Import required libraries
import pandas as pd
import dash
import plotly.graph_objects as go
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px



# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

launch_site_list = spacex_df['Launch Site'].unique()

launch_site_options =[{'label': 'All Sites', 'value': 'ALL'},{'label': launch_site_list[0], 'value': launch_site_list[0]},\
{'label': launch_site_list[1], 'value': launch_site_list[1]}, {'label': launch_site_list[2], 'value': launch_site_list[2]},\
{'label': launch_site_list[3], 'value': launch_site_list[3]}]

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                                options = launch_site_options,
                                                value = 'ALL',
                                                placeholder = "All Sites",
                                                searchable = True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min = 0,
                                                max = 10000,
                                                step = 1000,
                                                marks = {0:'0',
                                                         2000: '2000', 4000: '4000',
                                                         6000: '6000', 8000: '8000',
                                                         10000: '10000'},
                                                value = [min_payload, max_payload]),
                                html.Div(id = 'output-container-range-slider'),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])




def get_launch_site_success_data(data_frame):

    CCAFSLC40 = spacex_df[(spacex_df['Launch Site'] == launch_site_list[0])]
    CCAFSLC40 = CCAFSLC40[['Launch Site', 'class']]
    CCAFSLC40 = CCAFSLC40.groupby('class')['Launch Site'].value_counts().reset_index()
    CCAFSLC40.columns = ['class','Launch Site', 'count']

    VAFBSLC4E = spacex_df[(spacex_df['Launch Site'] == launch_site_list[1])]
    VAFBSLC4E = VAFBSLC4E[['Launch Site', 'class']]
    VAFBSLC4E = VAFBSLC4E.groupby('class')['Launch Site'].value_counts().reset_index()
    VAFBSLC4E.columns = ['class','Launch Site', 'count']

    KSCLC39A = spacex_df[(spacex_df['Launch Site'] == launch_site_list[2])]
    KSCLC39A = KSCLC39A[['Launch Site', 'class']]
    KSCLC39A = KSCLC39A.groupby('class')['Launch Site'].value_counts().reset_index()
    KSCLC39A.columns = ['class','Launch Site', 'count']

    CCAFSSLC40 = spacex_df[(spacex_df['Launch Site'] == launch_site_list[3])]
    CCAFSSLC40 = CCAFSSLC40[['Launch Site', 'class']]
    CCAFSSLC40 = CCAFSSLC40.groupby('class')['Launch Site'].value_counts().reset_index()
    CCAFSSLC40.columns = ['class','Launch Site', 'count']

    return CCAFSLC40, VAFBSLC4E, KSCLC39A, CCAFSSLC40


CCAFSLC40, VAFBSLC4E, KSCLC39A, CCAFSSLC40 = get_launch_site_success_data(spacex_df)

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id = 'success-pie-chart', component_property = 'figure'),
    Input(component_id = 'site-dropdown', component_property = 'value'))

def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values = 'class',
        names = 'Launch Site',
        title = 'Percentage of Successful Launches by Site')
        return fig
    elif entered_site == 'CCAFS LC-40':
        fig = px.pie(CCAFSLC40, values = 'count',  
        names = 'class', 
        title = 'Percentage of Successful Launches at site: CCAFS LC-40')
        return fig 
    elif entered_site == 'VAFB SLC-4E':
        fig = px.pie(VAFBSLC4E, values = 'count',  
        names = 'class', 
        title = 'Percentage of Successful Launches at site: VAFB SLC-4E')
        return fig
    elif entered_site == 'KSC LC-39A':
        fig = px.pie(KSCLC39A, values = 'count',  
        names = 'class', 
        title = 'Percentage of Successful Launches at site: KSC LC-39A')
        return fig
    elif entered_site == 'CCAFS SLC-40':
        fig = px.pie(CCAFSSLC40, values = 'count',  
        names = 'class', 
        title = 'Percentage of Successful Launches at site: CCAFS SLC-40 ')
        return fig
    else:
        return None

#https://dash.plotly.com/dash-core-components/rangeslider
@app.callback(
    Output('output-container-range-slider', 'children'),
    Input('payload-slider', 'value'))
def update_output(value):
    return 'You have selected "{}"'.format(value)

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id = 'success-payload-scatter-chart', component_property = 'figure'),
    [Input(component_id = 'site-dropdown', component_property = 'value'),
     Input(component_id = "payload-slider", component_property = "value")])

def get_scatter_plot(entered_site, payload_range):
    if entered_site == 'ALL':
        # https://plotly.com/python/setting-graph-size/
        fig = px.scatter(spacex_df, x = 'Payload Mass (kg)', 
                         y = 'class', 
                         color = 'Booster Version Category',
                         title = 'Correlation between Payload Mass (kg) and Success for All Sites',
                         range_x = payload_range,
                         width = 1500,
                         height = 500)
        return fig
    elif entered_site == 'CCAFS LC-40':
        CCAFSLC40_df = spacex_df[(spacex_df['Launch Site'] == 'CCAFS LC-40')]
        fig = px.scatter(CCAFSLC40_df, x = 'Payload Mass (kg)', 
                         y = 'class', 
                         color = 'Booster Version Category',
                         title = 'Correlation between Payload Mass (kg) and Success at site: CCAFS LC-40',
                         range_x = payload_range,
                         width = 1500,
                         height = 500)
        return fig 
    elif entered_site == 'VAFB SLC-4E':
        VAFBSLC4E_df = spacex_df[(spacex_df['Launch Site'] == 'VAFB SLC-4E')]
        fig = px.scatter(VAFBSLC4E_df, x = 'Payload Mass (kg)', 
                         y = 'class', 
                         color = 'Booster Version Category',
                         title = 'Correlation between Payload Mass (kg) and Success at site: VAFB SLC-4E',
                         range_x = payload_range,
                         width = 1500,
                         height = 500)
        return fig
    elif entered_site == 'KSC LC-39A':
        KSCLC39A_df = spacex_df[(spacex_df['Launch Site'] == 'KSC LC-39A')]
        fig = px.scatter(KSCLC39A_df, x = 'Payload Mass (kg)', 
                         y = 'class', 
                         color = 'Booster Version Category',
                         title = 'Correlation between Payload Mass (kg) and Success at site: KSC LC-39A',
                         range_x = payload_range,
                         width = 1500,
                         height = 500)
        return fig
    elif entered_site == 'CCAFS SLC-40':
        CCAFSSLC40_df = spacex_df[(spacex_df['Launch Site'] == 'CCAFS SLC-40')]
        fig = px.scatter(CCAFSSLC40_df, x = 'Payload Mass (kg)', 
                         y = 'class', 
                         color = 'Booster Version Category',
                         title = 'Correlation between Payload Mass (kg) and Success at site: CCAFS SLC-40',
                         range_x = payload_range,
                         width = 1500,
                         height = 500)
        return fig
    else:
        return None


# Run the app
if __name__ == '__main__':
    app.run()