from decouple import config
import plotly.express as px
import pandas as pd

# mapbox_token = config("MAPBOX_SECRET")
# mapbox_style = config("MAPBOX_STYLE")

# px.set_mapbox_access_token(mapbox_token)


def MapIndia(data=None):
    df = data
    color_scale = [
        "#fadc8f", "#f9d67a", "#f8d066", "#f8c952", "#f7c33d", "#f6bd29",
        "#f5b614", "#F4B000", "#eaa900", "#e0a200", "#dc9e00", "#FFA07A"]
    
    fig = px.scatter_mapbox(
        df,
        title='map',
        lat="latitude",
        lon="longitude",
        color="Profit",
        size="Sales",
        size_max=50,
        hover_name="City",
        hover_data=["City", "Profit", "Sales"],
        color_continuous_scale=color_scale,
    )

    fig.layout.update(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=700,
        # width=700,
        # This takes away the color bar on the right hand side of the plot if it is set to False
        coloraxis_showscale=False,
        mapbox_style='stamen-toner',
        mapbox=dict(center=dict(lat=23.5937, lon=81.9629), zoom=4),
    )

    fig.data[0].update(
        hovertemplate="Sales: ₹%{customdata[2]} <br>Profit: ₹%{customdata[1]}<br>City: %{customdata[0]}"
    )
    return fig
