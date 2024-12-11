from dash import Dash
app = Dash(__name__)
server = app.server

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, State, callback_context
from dash.dependencies import Input, Output, State
import base64
import io

# Encode the logo image
logo_path = "CSP_Logo.png"  # Changed from cs_partners_logo.png to CSP_Logo.png
encoded_logo = base64.b64encode(open(logo_path, 'rb').read()).decode()

# Initialize the Dash app
app = Dash(__name__)
server = app.server

# Define color schemes
light_theme = {
    'background': '#ffffff',
    'text': '#2c3e50',
    'secondary-background': '#f8f9fa',
    'border': '#dee2e6',
    'accent': '#007bff'
}

dark_theme = {
    'background': '#1a1a1a',
    'text': '#ffffff',
    'secondary-background': '#2d2d2d',
    'border': '#404040',
    'accent': '#4dabf7'
}

# Create the layout
app.layout = html.Div([
    # Help Button
    html.Div([
        html.Button(
            '❔ Help',
            id='help-button',
            n_clicks=0,
            style={
                'backgroundColor': 'transparent',
                'border': 'none',
                'color': 'var(--accent-color)',
                'cursor': 'pointer',
                'fontSize': '16px',
                'padding': '10px',
                'marginRight': '20px'
            }
        ),
        # Replace Modal with html.Div for popup
        html.Div(
            id='help-modal',
            children=[
                html.Div([
                    html.Div([
                        html.H4('How to Use This Dashboard', style={'marginTop': '0'}),
                        html.P([
                            '1. Upload your Excel file using the drag & drop area or file selector\n',
                            '2. Select one or more school years to compare\n',
                            '3. Select one or more schools to analyze\n',
                            '4. Use the height slider to adjust the graph size'
                        ], style={'whiteSpace': 'pre-line'}),
                        
                        html.H4('Frequently Asked Questions'),
                        html.P([
                            html.Strong('Q: Why are some metrics missing from the graph?'),
                            html.Br(),
                            'A: If a metric has no data for a selected school/year, it will not appear in the graph.',
                            html.Br(),
                            html.Br(),
                            html.Strong('Q: How do I compare schools over time?'),
                            html.Br(),
                            'A: Select multiple years and schools to see their performance trends.',
                            html.Br(),
                            html.Br(),
                            html.Strong('Q: How do I reset the selections?'),
                            html.Br(),
                            'A: Click the "✕" in the dropdown menus to clear your selections.',
                            html.Br(),
                            html.Br(),
                            html.Strong('Q: Can I download the graph?'),
                            html.Br(),
                            'A: Yes! Hover over the graph and use the download button in the toolbar.'
                        ], style={'whiteSpace': 'pre-line'}),
                        html.Button(
                            '✕ Close',
                            id='close-help',
                            style={
                                'position': 'absolute',
                                'right': '10px',
                                'top': '10px',
                                'border': 'none',
                                'background': 'transparent',
                                'color': 'var(--text-color)',
                                'cursor': 'pointer',
                                'fontSize': '16px'
                            }
                        )
                    ], style={
                        'padding': '20px',
                        'lineHeight': '1.5',
                        'position': 'relative'
                    })
                ], style={
                    'backgroundColor': 'var(--secondary-bg-color)',
                    'color': 'var(--text-color)',
                    'border': '1px solid var(--border-color)',
                    'borderRadius': '8px',
                    'maxWidth': '600px',
                    'margin': '40px auto',
                    'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)'
                })
            ],
            style={
                'display': 'none',
                'position': 'fixed',
                'top': '0',
                'left': '0',
                'width': '100%',
                'height': '100%',
                'backgroundColor': 'rgba(0,0,0,0.5)',
                'zIndex': '1000'
            }
        ),
    ], style={'float': 'left', 'padding': '10px'}),
    
    # Theme Toggle
    html.Div([
        dcc.RadioItems(
            id='theme-toggle',
            options=[
                {'label': '☀️ Light', 'value': 'light'},
                {'label': '🌙 Dark', 'value': 'dark'}
            ],
            value='light',
            inline=True,
            style={'float': 'right', 'padding': '10px'}
        )
    ], style={'overflow': 'hidden'}),
    
    # Header
    html.Div([
        # Logo and Title container
        html.Div([
            # Logo
            html.Img(
                src=f'data:image/png;base64,{encoded_logo}',
                style={
                    'height': '60px',
                    'marginRight': '20px',
                    'verticalAlign': 'middle'
                }
            ),
            # Title
            html.H1('School Index Reports', 
                    style={
                        'display': 'inline-block',
                        'verticalAlign': 'middle',
                        'margin': '20px',
                        'fontFamily': 'Segoe UI, Arial, sans-serif'
                    })
        ], style={
            'textAlign': 'center',
            'margin': '20px'
        })
    ], style={'borderBottom': '2px solid var(--border-color)'}),
    
    # File Upload Component
    html.Div([
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                html.I(className='fas fa-file-upload', style={'marginRight': '10px'}),
                'Drag and Drop or ',
                html.A('Select Excel File', style={'color': 'var(--accent-color)'})
            ]),
            style={
                'width': '100%',
                'height': '80px',
                'lineHeight': '80px',
                'borderWidth': '2px',
                'borderStyle': 'dashed',
                'borderRadius': '10px',
                'textAlign': 'center',
                'margin': '20px 0',
                'transition': 'all 0.3s ease',
                'cursor': 'pointer',
            },
            multiple=False
        ),
        # Add filename display
        html.Div(id='file-name-display', style={
            'textAlign': 'center',
            'padding': '10px',
            'color': 'var(--accent-color)',
            'fontStyle': 'italic'
        }),
    ], style={'padding': '0 40px'}),
    
    # Filters Container
    html.Div([
        html.Div([
            html.Label('Select School Year(s):', style={'fontWeight': 'bold', 'marginBottom': '8px'}),
            dcc.Dropdown(
                id='year-filter',
                options=[],
                multi=True,
                style={'borderRadius': '8px'}
            )
        ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '2%'}),
        
        html.Div([
            html.Label('Select School:', style={'fontWeight': 'bold', 'marginBottom': '8px'}),
            dcc.Dropdown(
                id='school-filter',
                options=[],
                multi=True,
                style={'borderRadius': '8px'}
            )
        ], style={'width': '33%', 'display': 'inline-block', 'marginRight': '2%'}),
        
        # Add new metrics filter
        html.Div([
            html.Label('Select Metrics:', style={'fontWeight': 'bold', 'marginBottom': '8px'}),
            dcc.Dropdown(
                id='metrics-filter',
                options=[
                    {'label': 'Composite Index', 'value': 'CompositeIndex'},
                    {'label': 'Growth Index', 'value': 'GrowthIndex'},
                    {'label': 'Proficiency Index', 'value': 'ProficiencyIndex'},
                    {'label': 'School Quality Index', 'value': 'SchoolQuality Index'},
                    {'label': 'EL Progress', 'value': 'EL ProgressIndex'},
                    {'label': 'Graduation Index', 'value': 'GraduationIndex'}
                ],
                value=['CompositeIndex', 'GrowthIndex', 'ProficiencyIndex', 'SchoolQuality Index', 'EL ProgressIndex', 'GraduationIndex'],
                multi=True,
                style={'borderRadius': '8px'}
            )
        ], style={'width': '33%', 'display': 'inline-block'})
    ], style={'padding': '20px 40px', 'display': 'none', 'backgroundColor': 'var(--secondary-bg-color)', 'borderRadius': '10px', 'margin': '20px 40px'}, id='filter-container'),
    
    # Height Slider
    html.Div([
        html.Label('Adjust Graph Height:', style={'fontWeight': 'bold', 'marginBottom': '8px'}),
        dcc.Slider(
            id='height-slider',
            min=400,
            max=1200,
            step=50,
            value=600,
            marks={i: str(i) for i in range(400, 1201, 200)},
            tooltip={'placement': 'bottom', 'always_visible': True},
            className='custom-slider'
        )
    ], style={'padding': '20px 40px', 'backgroundColor': 'var(--secondary-bg-color)', 'borderRadius': '10px', 'margin': '20px 40px'}),
    
    # Graph Container
    html.Div([
        dcc.Graph(id='performance-indicators'),
        # Simple text display for missing metrics
        html.Div(
            id='missing-metrics-message',
            style={
                'textAlign': 'center',
                'padding': '10px',
                'color': 'var(--text-color)',
                'fontSize': '14px'
            }
        )
    ], style={'padding': '20px 40px'}),

], id='main-container', style={'backgroundColor': 'var(--bg-color)', 'color': 'var(--text-color)', 'minHeight': '100vh'})

# Add callback for theme toggle
@app.callback(
    Output('main-container', 'style'),
    Input('theme-toggle', 'value')
)
def update_theme(theme):
    if theme == 'dark':
        return {
            'backgroundColor': dark_theme['background'],
            'color': dark_theme['text'],
            'minHeight': '100vh',
            '--bg-color': dark_theme['background'],
            '--text-color': dark_theme['text'],
            '--secondary-bg-color': dark_theme['secondary-background'],
            '--border-color': dark_theme['border'],
            '--accent-color': dark_theme['accent']
        }
    return {
        'backgroundColor': light_theme['background'],
        'color': light_theme['text'],
        'minHeight': '100vh',
        '--bg-color': light_theme['background'],
        '--text-color': light_theme['text'],
        '--secondary-bg-color': light_theme['secondary-background'],
        '--border-color': light_theme['border'],
        '--accent-color': light_theme['accent']
    }

# Update the graph callback to include theme-aware colors
@app.callback(
    [Output('performance-indicators', 'figure'),
     Output('missing-metrics-message', 'children')],
    [Input('year-filter', 'value'),
     Input('school-filter', 'value'),
     Input('metrics-filter', 'value'),
     Input('upload-data', 'contents'),
     Input('height-slider', 'value'),
     Input('theme-toggle', 'value')],
    State('upload-data', 'filename')
)
def update_graph(selected_years, selected_schools, selected_metrics, contents, height, theme, filename):
    if contents is None:
        return go.Figure(), ''
    
    df = parse_contents(contents, filename)
    
    if not isinstance(df, pd.DataFrame):
        return go.Figure(), ''
    
    # Fill NaN values with 0
    df = df.fillna(0)
    
    # Filter data based on selections
    if selected_years and selected_schools:
        filtered_df = df[
            (df['School Year'].isin(selected_years)) & 
            (df['Building Name'].isin(selected_schools))
        ]
    else:
        return go.Figure(), ''
    
    # Create the figure
    fig = go.Figure()
    
    # Use selected metrics instead of hardcoded list
    metrics = selected_metrics if selected_metrics else []
    
    # Track missing metrics
    missing_metrics = []
    
    if len(selected_years) > 1:  # Multiple years selected
        for school in selected_schools:
            school_data = filtered_df[filtered_df['Building Name'] == school]
            for metric in metrics:
                if metric in filtered_df.columns:
                    if all(school_data[metric] == 0):  # Check if all values are 0
                        if metric not in missing_metrics:
                            missing_metrics.append(metric)
                    else:
                        fig.add_trace(go.Bar(
                            name=f'{school} - {metric}',
                            x=school_data['School Year'],
                            y=school_data[metric],
                            text=school_data[metric].round(2),
                            textposition='auto',
                            marker={
                                'cornerradius': 5
                            }
                        ))
    else:  # Single year selected
        for metric in metrics:
            if metric in filtered_df.columns:
                if all(filtered_df[metric] == 0):  # Check if all values are 0
                    if metric not in missing_metrics:
                        missing_metrics.append(metric)
                else:
                    fig.add_trace(go.Bar(
                        name=metric,
                        x=filtered_df['Building Name'],
                        y=filtered_df[metric],
                        text=filtered_df[metric].round(2),
                        textposition='auto',
                        marker={
                            'cornerradius': 5
                        }
                    ))
    
    # Simplify missing metrics message
    message = ''
    if missing_metrics:
        message = f"Categories with no data: {', '.join(missing_metrics)}"
    
    # Update the layout with theme-aware colors
    layout_updates = {
        'plot_bgcolor': dark_theme['background'] if theme == 'dark' else light_theme['background'],
        'paper_bgcolor': dark_theme['background'] if theme == 'dark' else light_theme['background'],
        'font': {'color': dark_theme['text'] if theme == 'dark' else light_theme['text']},
        'title': {'font': {'size': 24, 'family': 'Segoe UI, Arial, sans-serif'}},
        'height': height,
        'xaxis': {
            'tickangle': 20 if len(selected_schools) >= 3 else 0,
            'gridcolor': dark_theme['border'] if theme == 'dark' else light_theme['border']
        },
        'yaxis': {
            'gridcolor': dark_theme['border'] if theme == 'dark' else light_theme['border']
        },
        'showlegend': True,
        'legend': {'orientation': 'h', 'yanchor': 'bottom', 'y': 1.02},
        'margin': {'b': 150}
    }
    
    fig.update_layout(**layout_updates)
    
    return fig, message

# Add custom CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" rel="stylesheet">
        <style>
            /* Custom CSS for modern look */
            body {
                margin: 0;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            .custom-slider .rc-slider-track {
                background-color: var(--accent-color);
            }
            
            .custom-slider .rc-slider-handle {
                border-color: var(--accent-color);
            }
            
            .dash-dropdown .Select-control {
                border-color: var(--border-color);
                background-color: var(--bg-color);
            }
            
            .dash-dropdown .Select-menu-outer {
                background-color: var(--bg-color);
                border-color: var(--border-color);
            }
            
            .dash-dropdown .Select-value-label {
                color: var(--text-color) !important;
            }
            
            .custom-tooltip {
                background-color: var(--secondary-bg-color) !important;
                color: var(--text-color) !important;
                border: 1px solid var(--border-color) !important;
                border-radius: 8px !important;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
            }
            
            .dash-tooltip {
                opacity: 1 !important;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    
    try:
        if 'xlsx' in filename:
            # Read Excel file
            df = pd.read_excel(io.BytesIO(decoded))
            return df
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

@app.callback(
    [Output('filter-container', 'style'),
     Output('year-filter', 'options'),
     Output('year-filter', 'value'),
     Output('school-filter', 'options')],
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def update_filters(contents, filename):
    if contents is None:
        return {'display': 'none'}, [], None, []
    
    df = parse_contents(contents, filename)
    
    if isinstance(df, pd.DataFrame):
        year_options = [{'label': str(year), 'value': year} 
                       for year in sorted(df['School Year'].unique())]
        school_options = [{'label': school, 'value': school} 
                         for school in sorted(df['Building Name'].unique())]
        
        return {'padding': '20px', 'display': 'block'}, year_options, [], school_options
    
    return {'display': 'none'}, [], None, []

# Add a new callback to update the filename display
@app.callback(
    Output('file-name-display', 'children'),
    Input('upload-data', 'filename')
)
def update_filename(filename):
    if filename:
        return f'📄 Uploaded: {filename}'
    return ''

# Update the callback for the modal
@app.callback(
    Output('help-modal', 'style'),
    [Input('help-button', 'n_clicks'),
     Input('close-help', 'n_clicks')],
    State('help-modal', 'style')
)
def toggle_modal(help_clicks, close_clicks, current_style):
    ctx = callback_context
    if not ctx.triggered:
        return {'display': 'none'}
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == 'help-button':
        return {
            'display': 'block',
            'position': 'fixed',
            'top': '0',
            'left': '0',
            'width': '100%',
            'height': '100%',
            'backgroundColor': 'rgba(0,0,0,0.5)',
            'zIndex': '1000'
        }
    elif button_id == 'close-help':
        return {'display': 'none'}
    
    return current_style

if __name__ == '__main__':
    app.run_server(debug=True)