'''
    Contains the functions to set up the map visualization.

'''

import plotly.graph_objects as go
import hover_template


def add_choro_trace(fig, montreal_data, locations, z_vals, colorscale):
    '''
        Adds the choropleth trace, representing Montreal's neighborhoods.

        Note: The z values and colorscale provided ensure every neighborhood
        will be grey in color. Although the trace is defined using Plotly's
        choropleth features, we are simply defining our base map.

        Args:
            fig: The figure to add the choropleth trace to
            montreal_data: The data used for the trace
            locations: The locations (neighborhoods) to show on the trace
            z_vals: The table to use for the choropleth's z values
            colorscale: The table to use for the choropleth's color scale
        Returns:
            fig: The updated figure with the choropleth trace

    '''
    fig = go.Figure(
        go.Choroplethmapbox(
            geojson=montreal_data,
            featureidkey="properties.NOM",
            locations=locations["NOM"],
            z=z_vals,
            colorscale=colorscale,
            hovertemplate=hover_template.map_base_hover_template()
        ),
    )
    fig.update_traces(showscale=False)

    return fig


def add_scatter_traces(fig, street_df):
    '''
        Adds the scatter trace, representing Montreal's pedestrian paths.

        Args:
            fig: The figure to add the scatter trace to
            street_df: The dataframe containing the information on the
                pedestrian paths to display
        Returns:
            The figure now containing the scatter trace

    '''
    for trace in street_df.groupby(['TYPE_SITE_INTERVENTION']).groups.keys():
        data = street_df.loc[street_df['TYPE_SITE_INTERVENTION'] == trace]

        fig.add_scattermapbox(
            lon=data["LONGITUDE"],
            lat=data["LATITUDE"],
            text=data["TYPE_SITE_INTERVENTION"],
            mode="markers",
            marker=go.scattermapbox.Marker(size=9, opacity=0.7),
            showlegend=True,
            name=trace,
            hovertemplate=hover_template.map_marker_hover_template(trace),
            customdata=[data['MODE_IMPLANTATION'], data['NOM_PROJET'], data['OBJECTIF_THEMATIQUE']]
        )

    return fig
