import numpy as np
import pandas as pd
import seaborn

# might need bokeh ?
import bokeh
from bokeh.models import HoverTool
from bokeh.plotting import figure, show, output_file, ColumnDataSource
from bokeh.models.glyphs import Glyph
from bokeh.plotting import gridplot

# trying folium for the heatmap
import folium
from folium import plugins

crash = pd.DataFrame.from_csv('~/Desktop/NYCcrash/NYPD_Motor_Vehicle_Collisions.csv', index_col = None)
#loc = crash['LOCATION'].tolist()
lat = crash['LATITUDE']
lon = crash['LONGITUDE']

# explore fatality
ded = crash['NUMBER OF PERSONS KILLED']
ded_fr = ded[ded !=0] ## 933 fatal accicends recorded. hmhmh

fatal = pd.DataFrame(pd.to_datetime(crash['DATE'][crash['NUMBER OF PERSONS KILLED'] != 0]))
fatal['NUM'] = crash['NUMBER OF PERSONS KILLED'][crash['NUMBER OF PERSONS KILLED'] != 0]

fatal_mon = fatal.set_index('DATE').groupby(pd.TimeGrouper(freq = 'M')).sum()
fatal_mon['date'] = fatal_mon.index.values
ym = fatal_mon['date'].apply(lambda x: x.strftime('%Y-%m')).tolist()

fatal_all = crash[crash['NUMBER OF PERSONS KILLED'] != 0]
latf = fatal_all['LATITUDE']
lonf = fatal_all['LONGITUDE']

# make a bokeh time series plot
import pandas as pd
from bokeh.charts import TimeSeries, show, output_file, vplot
from bokeh.models import (
    PanTool, WheelZoomTool, BoxSelectTool, PreviewSaveTool, ResizeTool, ResetTool, BoxZoomTool
)

data = dict(
    Date=ym,
    Deaths=fatal_mon['NUM'].tolist(),
)

tsline = TimeSeries(data,
    x='Date', y='Deaths',
    title="Traffic Deaths in NYC", ylabel='Monthly Crash Deaths', legend=True, plot_width=1000)


p = bokeh.plotting.figure(x_axis_type = "datetime",
  tools="pan,wheel_zoom,box_zoom,reset,resize,previewsave",plot_width=1000,
  name="myplot")

output_file("/Users/grad/Desktop/timeseries.html")

show(vplot(tsline))

# get the lat lons without nan values
lata = lat[lat.notnull()].tolist()
lona = lon[lon.notnull()].tolist()

locs = []
for i in range(0,len(lata)):
    locs.append([lata[i], lona[i]])

lat_fatal = latf[latf.notnull()].tolist()
lon_fatal = lonf[lonf.notnull()].tolist()

locsf = []
for i in range(0,len(lat_fatal)):
    locsf.append([lat_fatal[i], lon_fatal[i]])


#########################
# quick visulaization !! no data base will be big html file. !!
# Create a heatmap with the data.
heatmap_map = folium.Map(location=[40.75, -73.99], zoom_start=10)
heatmap_map.add_children(plugins.HeatMap(locs))
heatmap_map.save("/Users/grad/Desktop/NYCcrash/heatmap.html")

## just for fatal crashes
heatmap_map = folium.Map(location=[40.73, -73.91], zoom_start=11)
heatmap_map.add_children(plugins.HeatMap(locsf))
heatmap_map.save("/Users/grad/Desktop/NYCcrash/heatmap_fatal.html")



################################################
#choropleth of economics
unemployment = pd.read_csv('./US_Unemployment_Oct2012.csv')

