# Import required libraries
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
# Read the airline  csv data file and converting it into pandas dataframe
# importing as a csv file from a local directory
spacexdata = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_1.csv")
                                   
# Create a dash application
app = dash.Dash()

app.layout = html.Div(children=[html.H1('SpaceX Launch Record Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
                                        dcc.Dropdown(id = 'site-dropdown',
                                                     options = [{'label': 'All Sites', 'value': 'ALL'},
                                                               {'label': 'CCAFS SLC 40', 'value': 'CCAFS SLC 40'},
                                                               {'label': 'VAFB SLC 4E', 'value': 'VAFB SLC 4E'},
                                                               {'label': 'KSC LC 39A', 'value': 'KSC LC 39A'}],
                                                                value='ALL',
                                                                placeholder="Select any LaunchSite",
                                                                searchable=True),
                                html.Br(),
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,max=10000,step=1000,
                                                value=[spacexdata['PayloadMass'].min(),spacexdata['PayloadMass'].max()],
                                                marks={0: '0', 2500:'2500',5000:'5000',
                                                7500:'7500', 10000: '10000'}),
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacexdata
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Success Count for launch sites')
        return fig
    else:
        filtered_df=spacexdata[spacexdata['Launch Site']== entered_site]
        filtered_df=filtered_df.groupby(['Launch Site','class']).size().reset_index(name='class count')
        fig=px.pie(filtered_df,values='class count',names='class',title=f"Total Success Launches for site {entered_site}")
        return fig
        # return the outcomes piechart for a selected site

@app.callback(Output(component_id='success-payload-scatter-chart',component_property='figure'),
                [Input(component_id='site-dropdown',component_property='value'),
                Input(component_id='payload-slider',component_property='value')])
def scatter(entered_site,payload):
    filtered_df = spacexdata[spacexdata['PayloadMass'].between(payload[0],payload[1])]
    # thought reusing filtered_df may cause issues, but tried it out of curiosity and it seems to be working fine
    
    if entered_site=='ALL':
        fig=px.scatter(filtered_df,x='PayloadMass',y='class',color='Booster Version Category',title='Success count on Payload mass for all sites')
        return fig
    else:
        fig=px.scatter(filtered_df[filtered_df['Launch Site']==entered_site],x='Payload Mass (kg)',y='class',color='Booster Version Category',title=f"Success count on Payload mass for site {entered_site}")
        return fig

# Run the app
app.run_server()

