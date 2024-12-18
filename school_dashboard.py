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
        # Help modal div here
        html.Div(id='help-modal'),
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
    
    
    # Header with Logo
    html.Div([
        html.Div([
            html.Img(
                src=f'data:image/png;base64,{encoded_logo}',
                style={
                    'height': '60px',
                    'marginRight': '20px',
                    'verticalAlign': 'middle'
                }
            ),
            html.H1('School Index Reports', 
                    style={
                        'display': 'inline-block',
                        'verticalAlign': 'middle',
                        'margin': '20px',
                        'fontFamily': 'Segoe UI, Arial, sans-serif'
                    })
        ], style={'textAlign': 'center', 'margin': '20px'})
    ], style={'borderBottom': '2px solid var(--border-color)'}),
    
    # File Upload
    html.Div([
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Excel File')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            multiple=False
        ),
        html.Div(id='file-name-display')
    ], style={'margin': '20px'}),
    
    # Filters Container
    html.Div([
        # Year Filter
        html.Div([
            html.Label('Select School Year(s):', style={'fontWeight': 'bold', 'marginBottom': '10px'}),
            dcc.Dropdown(
                id='year-filter',
                multi=True,
                placeholder='Select year(s)...',
                className='dash-dropdown'
            )
        ], style={'flex': 1, 'marginRight': '20px'}),
        
        # School Filter
        html.Div([
            html.Label('Select School(s):', style={'fontWeight': 'bold', 'marginBottom': '10px'}),
            dcc.Dropdown(
                id='school-filter',
                multi=True,
                placeholder='Select school(s)...',
                className='dash-dropdown'
            )
        ], style={'flex': 1, 'marginRight': '20px'}),
        
        # Metrics Filter
        html.Div([
            html.Label('Select Metrics:', style={'fontWeight': 'bold', 'marginBottom': '10px'}),
            dcc.Dropdown(
                id='metrics-filter',
                multi=True,
                placeholder='Select metrics...',
                className='dash-dropdown'
            )
        ], style={'flex': 1})
    ], id='filter-container', style={'display': 'none', 'padding': '20px', 'display': 'flex', 'gap': '20px'}),
    
    # Graph Type Toggle Button
    html.Button(
        id='toggle-graph-type',
        children='Toggle to Line Graph',
        style={
            'backgroundColor': '#007bff',
            'color': 'white',
            'padding': '10px 20px',
            'border': 'none',
            'borderRadius': '5px',
            'cursor': 'pointer',
            'margin': '20px auto',
            'display': 'block'
        }
    ),
    
    # Height Slider
    html.Div([
        html.Label('Adjust Graph Height:', style={'fontWeight': 'bold'}),
        dcc.Slider(
            id='height-slider',
            min=400,
            max=1200,
            step=50,
            value=800,
            marks={i: str(i) for i in range(400, 1201, 200)}
        )
    ], style={'margin': '20px'}),
    
    # Custom Graph Title
    html.Div([
        html.Label('Custom Graph Title (optional):', style={'fontWeight': 'bold'}),
        dcc.Input(
            id='custom-title',
            type='text',
            placeholder='Enter custom title or leave blank for default',
            n_submit=0,
            style={
                'width': '100%',
                'padding': '8px',
                'marginTop': '5px',
                'borderRadius': '4px',
                'border': '1px solid var(--border-color)',
                'backgroundColor': 'var(--bg-color)',
                'color': 'var(--text-color)'
            }
        ),
        dcc.Checklist(
            id='show-subtitle',
            options=[{'label': 'Show "MDE School Index 2 Year Comparison" subtitle', 'value': 'show'}],
            value=['show'],  # Default to showing the subtitle
            style={'marginTop': '10px'}
        )
    ], style={'margin': '20px'}),
    
    # Graph Container
    html.Div([
        dcc.Graph(id='performance-indicators'),
        html.Div(id='missing-metrics-message')
    ], style={'margin': '20px'}),

    # Help Modal Content
    html.Div([
        html.Div([
            html.Div([
                html.H3('Help Guide', style={'marginBottom': '20px'}),
                html.Button(
                    '✕',
                    id='close-help',
                    style={
                        'position': 'absolute',
                        'right': '10px',
                        'top': '10px',
                        'backgroundColor': 'transparent',
                        'border': 'none',
                        'fontSize': '20px',
                        'cursor': 'pointer'
                    }
                ),
                html.Div([
                    html.H4('Getting Started:'),
                    html.Ol([
                        html.Li('Upload your Excel file using the drag-and-drop area or file selector.'),
                        html.Li('Select the school year(s) and school(s) you want to analyze.'),
                        html.Li('Choose the metrics you want to display on the graph.'),
                        html.Li('Use the graph type toggle to switch between bar and line graphs.'),
                        html.Li('Adjust the graph height using the slider if needed.')
                    ])
                ])
            ], style={
                'backgroundColor': 'var(--bg-color)',
                'padding': '30px',
                'borderRadius': '10px',
                'maxWidth': '600px',
                'margin': '50px auto',
                'position': 'relative',
                'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)'
            })
        ], style={
            'position': 'fixed',
            'top': '50%',
            'left': '50%',
            'transform': 'translate(-50%, -50%)',
            'zIndex': '1001'
        })
    ], id='help-modal', style={'display': 'none'}),

], id='main-container')

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

def safe_float_convert(val):
    try:
        return float(val)
    except (ValueError, TypeError):
        return 0.0

# Update the graph callback to include theme-aware colors
@app.callback(
    [Output('performance-indicators', 'figure'),
     Output('missing-metrics-message', 'children'),
     Output('toggle-graph-type', 'children')],
    [Input('year-filter', 'value'),
     Input('school-filter', 'value'),
     Input('metrics-filter', 'value'),
     Input('upload-data', 'contents'),
     Input('height-slider', 'value'),
     Input('theme-toggle', 'value'),
     Input('toggle-graph-type', 'n_clicks'),
     Input('custom-title', 'value'),
     Input('show-subtitle', 'value')],
    [State('toggle-graph-type', 'children'),
     State('upload-data', 'filename')]
)
def update_graph(selected_years, selected_schools, selected_metrics, contents, height, theme, n_clicks, custom_title, show_subtitle, current_text, filename):
    # Initialize n_clicks if None
    n_clicks = 0 if n_clicks is None else n_clicks
    
    # Determine graph type based on number of clicks
    graph_type = 'line' if n_clicks % 2 == 1 else 'bar'
    
    # Toggle button text
    new_button_text = 'Toggle to Bar Graph' if graph_type == 'line' else 'Toggle to Line Graph'
    
    if contents is None:
        return go.Figure(), '', new_button_text
    
    df = parse_contents(contents, filename)
    
    if not isinstance(df, pd.DataFrame):
        return go.Figure(), '', new_button_text
    
    # Fill NaN values with 0
    df = df.fillna(0)
    
    # Filter data based on selections
    if selected_years and selected_schools:
        filtered_df = df[
            (df['School Year'].isin(selected_years)) & 
            (df['Building Name'].isin(selected_schools))
        ]
    else:
        return go.Figure(), '', new_button_text
    
    # Create the figure
    fig = go.Figure()
    
    # Add the logo image
    fig.add_layout_image(
        dict(
            source=f'data:image/png;base64,{encoded_logo}',
            xref="paper",
            yref="paper",
            x=1,  # Right side
            y=1.1,  # Above the plot
            sizex=0.15,  # Width of the image
            sizey=0.15,  # Height of the image
            xanchor="right",
            yanchor="top"
        )
    )
    
    # Use selected metrics instead of hardcoded list
    metrics = selected_metrics if selected_metrics else []
    
    # Track missing metrics
    missing_metrics = []
    
    if len(selected_years) > 1:  # Multiple years selected
        for school in selected_schools:
            school_data = filtered_df[filtered_df['Building Name'] == school]
            for metric in metrics:
                if metric in filtered_df.columns:
                    if all(school_data[metric] == 0):
                        if metric not in missing_metrics:
                            missing_metrics.append(metric)
                    else:
                        if graph_type == 'bar':
                            fig.add_trace(go.Bar(
                                name=f'{school} - {metric}',
                                x=school_data['School Year'],
                                y=school_data[metric],
                                text=[f"{safe_float_convert(val):.1f}<br><b>{metric}</b>" for val in school_data[metric]],
                                textposition='outside',
                                textfont=dict(
                                    size=12,
                                    family='Segoe UI, Arial, sans-serif'
                                ),
                                cliponaxis=False,
                                marker={
                                    'cornerradius': 5
                                }
                            ))
                        else:  # line graph
                            fig.add_trace(go.Scatter(
                                name=f'{school} - {metric}',
                                x=school_data['School Year'],
                                y=school_data[metric],
                                text=[f"{metric}: {safe_float_convert(val):.2f}" for val in school_data[metric]],
                                textposition='top center',
                                mode='lines+markers+text',
                                marker={'size': 8}
                            ))
    else:  # Single year selected
        for metric in metrics:
            if metric in filtered_df.columns:
                if all(filtered_df[metric] == 0):
                    if metric not in missing_metrics:
                        missing_metrics.append(metric)
                else:
                    if graph_type == 'bar':
                        fig.add_trace(go.Bar(
                            name=metric,
                            x=filtered_df['Building Name'],
                            y=filtered_df[metric],
                            text=[f"{safe_float_convert(val):.1f}<br><b>{metric}</b>" for val in filtered_df[metric]],
                            textposition='outside',
                            textfont=dict(
                                size=12,
                                family='Segoe UI, Arial, sans-serif'
                            ),
                            cliponaxis=False,
                            marker={
                                'cornerradius': 5
                            }
                        ))
                    else:  # line graph
                        fig.add_trace(go.Scatter(
                            name=metric,
                            x=filtered_df['Building Name'],
                            y=filtered_df[metric],
                            text=[f"{metric}: {safe_float_convert(val):.2f}" for val in filtered_df[metric]],
                            textposition='top center',
                            mode='lines+markers+text',
                            marker={'size': 8}
                        ))
    
    # Simplify missing metrics message
    message = ''
    if missing_metrics:
        message = f"Categories with no data: {', '.join(missing_metrics)}"
    
    # Modify the title creation logic
    if custom_title:
        title = custom_title
    else:
        if len(selected_schools) == 1:
            # Extract school name (everything before the "/")
            school_name = selected_schools[0].split('/')[0].strip()
            title = school_name
            if show_subtitle and 'show' in show_subtitle:
                title += "<br>MDE School Index 2 Year Comparison"
        else:
            title = "School Performance Comparison"
            if show_subtitle and 'show' in show_subtitle:
                title += "<br>MDE School Index 2 Year Comparison"

    # Update the layout with theme-aware colors and improved styling
    layout_updates = {
        'plot_bgcolor': dark_theme['background'] if theme == 'dark' else light_theme['background'],
        'paper_bgcolor': dark_theme['background'] if theme == 'dark' else light_theme['background'],
        'font': {
            'color': dark_theme['text'] if theme == 'dark' else light_theme['text'],
            'family': 'Segoe UI, Arial, sans-serif'
        },
        'title': {
            'text': title,
            'font': {
                'size': 24,
                'family': 'Segoe UI, Arial, sans-serif',
                'color': dark_theme['text'] if theme == 'dark' else light_theme['text']
            },
            'y': 0.95,  # Position the title higher to make room for the logo
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        'height': height,
        'xaxis': {
            'tickangle': 20 if len(selected_schools) >= 3 else 0,
            'gridcolor': dark_theme['border'] if theme == 'dark' else light_theme['border'],
            'title': {
                'text': 'School Year' if len(selected_years) > 1 else 'Schools',
                'font': {'size': 14}
            }
        },
        'yaxis': {
            'gridcolor': dark_theme['border'] if theme == 'dark' else light_theme['border'],
            'title': {
                'text': 'Index Value',
                'font': {'size': 14}
            },
            'range': [0, max([max(trace.y) for trace in fig.data]) * 1.2]
        },
        'showlegend': True,
        'legend': {
            'orientation': 'h',
            'yanchor': 'bottom',
            'y': -0.3,  # Move legend below the graph
            'xanchor': 'center',
            'x': 0.5,
            'bgcolor': 'rgba(0,0,0,0)'  # Transparent background
        },
        'margin': {
            't': 120,  # Top margin for title and logo
            'b': 150,  # Bottom margin for legend
            'l': 80,
            'r': 80,
            'pad': 10
        }
    }
    
    fig.update_layout(**layout_updates)
    
    # Update bar/line styles for better visibility
    if graph_type == 'bar':
        fig.update_traces(
            marker_line_color=dark_theme['border'] if theme == 'dark' else light_theme['border'],
            marker_line_width=1,
            opacity=0.8
        )
    else:  # line graph
        fig.update_traces(
            line_width=3,
            marker_size=8
        )
    
    return fig, message, new_button_text

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
            
            # Convert '--' to 0 or NaN
            for column in df.columns:
                if df[column].dtype == object:  # Only process non-numeric columns
                    df[column] = df[column].replace('--', 0)
                    
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
     Output('school-filter', 'options'),
     Output('metrics-filter', 'options'),
     Output('metrics-filter', 'value')],
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def update_filters(contents, filename):
    if contents is None:
        return {'display': 'none'}, [], None, [], [], None
    
    df = parse_contents(contents, filename)
    
    if isinstance(df, pd.DataFrame):
        year_options = [{'label': str(year), 'value': year} 
                       for year in sorted(df['School Year'].unique())]
        school_options = [{'label': school, 'value': school} 
                         for school in sorted(df['Building Name'].unique())]
        
        # Get all available metrics
        exclude_columns = ['School Year', 'Building Name']
        all_metrics = [col for col in df.columns if col not in exclude_columns]
        metric_options = [{'label': metric, 'value': metric} for metric in sorted(all_metrics)]
        
        # Define the default metrics to be selected
        default_metrics = [
            "SchoolQuality Index",
            "CompositeIndex",
            "GraduationIndex",
            "GrowthIndex",
            "EL ProgressIndex",
            "ProficiencyIndex"
        ]
        
        # Filter to only include metrics that exist in the dataframe
        selected_metrics = [metric for metric in default_metrics if metric in df.columns]
        
        return {
            'padding': '20px',
            'display': 'block'
        }, year_options, [], school_options, metric_options, selected_metrics
    
    return {'display': 'none'}, [], None, [], [], None

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

# Add this new callback to handle Enter key presses
@app.callback(
    Output('custom-title', 'value'),
    [Input('custom-title', 'n_submit'),
     Input('custom-title', 'value')],
    [State('custom-title', 'value')]
)
def handle_enter(n_submit, current_value, prev_value):
    ctx = callback_context
    if not ctx.triggered:
        return current_value or ''
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if trigger_id == 'custom-title' and ctx.triggered[0]['prop_id'].endswith('n_submit'):
        # Only add <br> when Enter is pressed
        return current_value + '<br>'
    
    return current_value or ''

if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=True)