import panel as pn
pn.extension('vega')
import pandas as pd
import altair as alt
import numpy as np
import json
from pathlib import Path

# Set the paths for the data
folder_path = Path('/Users/xiyuanzhang/Desktop/learn/interactive_datav/final_proj/single_level')
heatmap_folder_path = Path('/Users/xiyuanzhang/Desktop/learn/interactive_datav/final_proj/heatmap')

# Initialize cell types from the dataset
cell_types = [file.stem for file in folder_path.glob('*') if not file.name.startswith('.')]

# Load heatmap data to get gene names
data = pd.read_pickle('test.pkl')
genes = data.columns.tolist()

# Panel widgets
dataset_dropdown = pn.widgets.Select(name='Cell Type', options=cell_types, value='γδTCells')
circle_size = pn.widgets.FloatSlider(name="Size", start=10, end=100, value=20)
opacity = pn.widgets.FloatSlider(name="Opacity", start=0.1, end=1, value=0.8)
gene_slider = pn.widgets.IntSlider(name='Number of Genes', start=1, end=50, value=20)
single_gene = pn.widgets.AutocompleteInput(
    name='Selected Gene', options=genes,
    case_sensitive=False, search_strategy='includes',
)
injury_pane = pn.pane.Image('./injury.png', width=300)

# Markdown instructions
instruction = pn.pane.Markdown("""
This dashboard visualizes single-cell data from a traumatic brain injury patient across three different conditions: healthy, mild, and severe. 
Additionally, data is collected at three different time points: day 1, day 3, and day 7 after hospitalization. 
The goal of this visualization is to provide an overview of cellular behavior under different conditions and time points, and to identify potential genes that play crucial roles in disease development.
""")

# Disable row limits for Altair
alt.data_transformers.disable_max_rows()

# Define custom theme for Altair charts
def custom_theme():
    return {
        'config': {
            'background': 'transparent',
            'title': {
                'font': 'Arial',
                'fontSize': 20,
                'fontWeight': 'bold',
                'color': 'black'
            },
            'axis': {
                'labelFont': 'Arial',
                'labelFontSize': 15,
                'titleFont': 'Arial',
                'titleFontSize': 18,
                'titleFontWeight': 'bold',
                'titleColor': 'black'
            },
            'legend': {
                'labelFont': 'Arial',
                'labelFontSize': 15,
                'titleFont': 'Arial',
                'titleFontSize': 18,
                'titleFontWeight': 'bold',
                'titleColor': 'black'
            }
        }
    }

# Register and enable the custom theme
alt.themes.register('custom_theme', custom_theme)
alt.themes.enable('custom_theme')

# Load dataset
def load_dataset(dataset_name):
    dataset_path = folder_path / f'{dataset_name}.pkl'
    return pd.read_pickle(dataset_path)

# Load heatmap data
def load_heatmap(dataset_name):
    dataset_path = heatmap_folder_path / f'{dataset_name}.pkl'
    return pd.read_pickle(dataset_path)

# Visualize dataset
def visualize_dataset(dataset_name, circle_size=20, opacity=0.8):
    df = load_dataset(dataset_name)
    selector = alt.selection_point(fields=['Condition'])
    condition = alt.condition(selector, 'Condition', alt.value('lightgrey'))
    opacity_cond = alt.condition(selector, alt.value(opacity), alt.value(0.2))
    time = alt.condition(selector, 'Time', alt.value('transparent'))

    scatter_plot = alt.Chart(df).mark_circle(size=circle_size).encode(
        x='PC_condition',
        y='PC_Time',
        color=condition,
        opacity=opacity_cond,
        tooltip=df.columns.to_list()
    ).properties(
        width=800,
        height=500
    )

    time_plot = alt.Chart(df).mark_circle(size=circle_size).encode(
        x='PC_condition',
        y='PC_Time',
        tooltip=df.columns.to_list(),
        color=time
    ).properties(
        width=800,
        height=500
    )

    combined_chart = alt.hconcat(scatter_plot, time_plot).resolve_scale().configure_concat(
        spacing=250
    ).add_params(selector)

    vega_dict = combined_chart.to_dict()
    return vega_dict

# Update headings and plots based on the selected dataset
@pn.depends(dataset_dropdown.param.value)
def update_headings(selected_dataset):
    content = f'# General property of {selected_dataset}'
    return pn.pane.Markdown(content)

@pn.depends(dataset_dropdown.param.value, circle_size, opacity)
def update_plot(selected_dataset, circle_size, opacity):
    vega_dict = visualize_dataset(selected_dataset, circle_size, opacity)
    return pn.pane.Vega(vega_dict, sizing_mode='stretch_width', align='center')

@pn.depends(gene_slider.param.value, dataset_dropdown.param.value)
def create_heatmap(num_genes, dataset_name):
    result_df = load_heatmap(dataset_name)
    selected_genes = result_df.columns[-num_genes:].tolist()[::-1]
    df_selected = result_df[selected_genes].reset_index().melt(id_vars='condition')
    df_selected.columns = ['Condition', 'Gene', 'Expression']

    heatmap = alt.Chart(df_selected).mark_rect().encode(
        x=alt.X('Gene:O', sort=alt.EncodingSortField(field='Gene', order='ascending'),
                scale=alt.Scale(domain=selected_genes)),
        y=alt.Y('Condition:O', sort=alt.EncodingSortField(field='Condition', order='ascending')),
        color=alt.Color('Expression:Q', scale=alt.Scale(scheme='lightgreyred')),
        tooltip=['Condition', 'Gene', 'Expression']
    ).properties(
        width=600,
        height=400,
        title='Heatmap of Gene Expression'
    )

    vega_dict = heatmap.to_dict()
    return pn.pane.Vega(vega_dict, sizing_mode='stretch_width')

# Filtered table based on selection
df = pd.read_pickle('./test.pkl')

def filtered_table(selection,selected_gene):
    domain = ['day0', "day1", "day3", 'day7']
    range_ = ['#93c4c1', '#77b472', '#f4d15b', '#c094b5']
    if not selection:
        return "## No selection"
    query = ' & '.join(
        f'{values[0]} <= `{col}` <= {values[1]}'
        if pd.api.types.is_numeric_dtype(df[col])
        else f'`{col}` in {values}' 
        for col, values in selection.items()
    )
    updated_df = df.query(query)
    
    return alt.Chart(updated_df).mark_tick().encode(
    x=alt.X(f'{selected_gene}:Q', scale=alt.Scale(zero=False)),
    y='time:N',
    color=alt.Color('time').scale(domain=domain, range=range_)
    ).properties(
        width=600,
        height=100
    )
    

@pn.depends(single_gene.param.value)
def update_vega_pane(selected_gene):
    brush = alt.selection_interval(name='brush')
    chart = alt.Chart(df).mark_tick().encode(
        x=alt.X(f'{selected_gene}:Q', scale=alt.Scale(zero=False)),
        y='condition:N',
        color=alt.condition(brush, 'condition:N', alt.value('lightgray'))
    ).add_params(
        brush
    ).properties(
        width=600,
        height=100
    )
    vega_pane = pn.pane.Vega(chart, debounce=10)
    time_plot = pn.bind(filtered_table, vega_pane.selection.param.brush,selected_gene)

    return pn.Column(vega_pane,time_plot)



layout = pn.template.FastListTemplate(
    header_background="#f2505d",
    title="Visualizing Single-Cell Data in Traumatic Brain Injury",
    sidebar=[
        injury_pane,
        instruction,
        dataset_dropdown,
        circle_size,
        opacity,
        gene_slider
    ],
    main=[
        pn.Column(
            update_headings,
            pn.Row(update_plot, align='center', sizing_mode='stretch_width')
        ),
        pn.Column(
            pn.pane.Markdown("# Gene expression exploration"),
            pn.Row(create_heatmap, pn.Column(single_gene, update_vega_pane))
        )
    ]
)

layout.servable()