import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

# Load Data (Replace this with your actual dataset loading method)
df_dashboard = pd.read_csv("your_data.csv")

# Initialize Dash app
app = dash.Dash(__name__)
server = app.server

# Create a bar chart for churn risk levels
fig_risk_levels = px.histogram(df_dashboard, x='Churn_Risk_Level', 
                               title="Churn Risk Levels Distribution", 
                               color="Churn_Risk_Level",
                               labels={'Churn_Risk_Level': 'Risk Level'},
                               category_orders={"Churn_Risk_Level": ["Low", "Medium", "High"]})

# Layout
app.layout = html.Div(style={'background': '#F5F5F5', 'min-height': '100vh', 'padding': '20px'}, children=[

    # Header with Logo & Title
    html.Div([
        html.Img(src='/assets/logo.png', style={'height': '100px', 'margin-right': '20px'}),
        html.H1("Customer Churn Risk Dashboard", 
                style={'color': 'black', 'font-family': 'sans-serif', 'font-weight': '200'})
    ], style={'display': 'flex', 'align-items': 'center'}),

    # Dropdown Filter
    html.Div([
        html.Label("Filter by Churn Risk Level:", style={'font-size': '16px', 'margin-bottom': '5px', 'textAlign': 'center'}),
        dcc.Dropdown(
            id='risk-filter',
            options=[{'label': risk, 'value': risk} for risk in df_dashboard['Churn_Risk_Level'].unique()],
            value=[],
            multi=True,
            placeholder="Select risk level...",
            style={'width': '50%', 'margin': 'auto'}
        ),
    ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'margin-bottom': '20px'}),

    # Main Content Section
    html.Div([
        html.Div([dcc.Graph(id='risk-chart', figure=fig_risk_levels)], style={'width': '60%', 'padding': '20px'}),
        html.Div(id='summary-stats', style={
            'width': '40%', 'padding': '20px', 'textAlign': 'center',
            'border-left': '2px solid black'
        }),
    ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'gap': '20px'}),
])

# Callback to update graph & statistics dynamically
@app.callback(
    [Output('risk-chart', 'figure'), Output('summary-stats', 'children')],
    [Input('risk-filter', 'value')]
)
def update_dashboard(selected_risk):
    if not selected_risk:
        filtered_df = df_dashboard  # Show all data if no filter is selected
    else:
        filtered_df = df_dashboard[df_dashboard['Churn_Risk_Level'].isin(selected_risk)]

    updated_fig = px.histogram(filtered_df, x='Churn_Risk_Level', 
                               title="Churn Risk Levels Distribution", 
                               color="Churn_Risk_Level",
                               labels={'Churn_Risk_Level': 'Risk Level'},
                               category_orders={"Churn_Risk_Level": ["Low", "Medium", "High"]})

    updated_fig.update_layout(plot_bgcolor='lightgrey', paper_bgcolor='#F5F5F5', font=dict(color='black'))

    avg_age = filtered_df['Age'].mean()
    avg_support_calls = filtered_df['Support Calls'].mean()
    avg_total_spend = filtered_df['Total Spend'].mean()
    avg_usage_frequency = filtered_df['Usage Frequency'].mean()

    stats_cards = html.Div([
        html.Div([html.H3(f"{avg_age:.1f}" if not pd.isna(avg_age) else "N/A"), html.P("Average Age")]),
        html.Div([html.H3(f"{avg_support_calls:.1f}" if not pd.isna(avg_support_calls) else "N/A"), html.P("Support Calls")]),
        html.Div([html.H3(f"${avg_total_spend:.2f}" if not pd.isna(avg_total_spend) else "N/A"), html.P("Total Spend")]),
        html.Div([html.H3(f"{avg_usage_frequency:.1f}" if not pd.isna(avg_usage_frequency) else "N/A"), html.P("Usage Frequency")]),
    ], style={'display': 'flex', 'justify-content': 'space-around'})

    return updated_fig, stats_cards

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
  
