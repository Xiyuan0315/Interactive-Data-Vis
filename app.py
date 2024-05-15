import panel as pn
pn.extension('vega', template='fast')
pn.state.template.title = "Single cell visualization browser"
import pandas as pd
import altair as alt
from ipywidgets import interactive
import hvplot.pandas
import re
from vega_datasets import data
import numpy as np
import json
from pathlib import Path

folder_path = Path('/Users/xiyuanzhang/Desktop/learn/interactive_datav/final_proj/single_level')
cell_types = [file.stem for file in folder_path.glob('*')]

def load_dataset(dataset_name):
    dataset_path = folder_path / f'{dataset_name}.pkl'
    return pd.read_pickle(dataset_path)

# Define the function to visualize the dataset
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
        width=600,
        height=400
    )

    time_plot = alt.Chart(df).mark_circle(size=circle_size).encode(
        x='PC_condition',
        y='PC_Time',
        tooltip=df.columns.to_list(),
        color=time
    ).properties(
        width=600,
        height=400
    )
    combined_chart = scatter_plot.add_params(selector) | time_plot.add_params(selector)
    # Serialize to JSON string and then parse into Python dictionary
    vega_json_string = combined_chart.to_json(format="vega")
    vega_dict = json.loads(vega_json_string)  # Parse JSON string to dictionary
    return vega_dict

cell_types = cell_types  # Update with actual options

# Define 3 Panel widgets
dataset_dropdown = pn.widgets.Select(name='Cell Type', options=cell_types, value='CD4+αβTCells_naive')
circle_size = pn.widgets.FloatSlider(name="size", start=10, end=100, value=20)
opacity = pn.widgets.FloatSlider(name="opacity", start=0.1, end=1, value=0.8)

# Convert Altair/Vega JSON to a Panel compatible format
@pn.depends(dataset_dropdown.param.value, circle_size, opacity)
def update_plot(selected_dataset, circle_size, opacity):
    vega_dict = visualize_dataset(selected_dataset, circle_size, opacity)
    return pn.pane.Vega(vega_dict, sizing_mode='stretch_width')

pn.extension(template='bootstrap')
# plot_opts = dict(responsive=True, min_height=400)
pn.Column(
    pn.Row(
        pn.Column(dataset_dropdown, circle_size, opacity),
        update_plot
    )
).servable(target='main')
