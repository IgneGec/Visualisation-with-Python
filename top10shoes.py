#1.clean data and prepare for visualisation

#install libraries

import pandas as pd
#download data
df = pd.read_csv('https://query.data.world/s/rgxzfnoqy4kk35y2a4uloqq5cd4wna')
#create new dataframe just for column 'brand'
n_df = df[['brand']]
#count frequency of each brand
n1_df = n_df.merge(n_df['brand'].value_counts().to_frame(),# add new column to frame
how='left', left_on ='brand',#show where to add
right_index = True, suffixes =('','x')).rename(columns = {'brandx':'brand_count'})
#eliminate duplicates and get top 10
n2_df = n1_df.drop_duplicates(['brand','brand_count'])
final_df = n2_df.sort_values('brand_count',ascending=False).head(10)# sort out and extract top 10

#reset indexes
final_df = final_df.reset_index()
del final_df['index']

#to save dataframe as csv
final_df.to_csv('data_visual.csv', index=False)

#data for actual visual is ready to go..however, needed 
#to add manualy extra columns with each company logo

#2.Visualization
#import libraries
from bokeh.plotting import figure, output_file, show, save, ColumnDataSource
from bokeh.models.tools import HoverTool
from bokeh.transform import factor_cmap
from bokeh.palettes import Greys10
from bokeh.embed import components
output_file('index.html')

#download data
df = pd.read_csv('data_visual1.csv') # find in my repository
source = ColumnDataSource(df)

# data into list for graph
brand_list = source.data['brand'].tolist()

#add features to diagram
p = figure(
    y_range = brand_list,
    plot_width = 600,
    plot_height = 800,
    title='TOP 10 Shoe Brand',
    tools = 'pan, box_select, zoom_in, zoom_out,save, reset',
    
   )
p.hbar(
y = 'brand',
right = 'brand_count',
left = 0,
height = 0.4,
fill_color = factor_cmap('brand',
palette = Greys10,
 factors = brand_list),                     
fill_alpha = 10.0,
source = source,
legend = 'brand', 
)
p.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
p.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks
p.title.text_font_size = '14pt'
p.outline_line_color = "black"
p.background_fill_color = "beige"
p.xaxis.major_label_text_font_size = '0pt'
p.yaxis.major_label_text_font_size = '12pt'
p.legend.orientation = 'vertical'
p.legend.location = 'top_right'
p.legend.label_text_font_size = '10px'
hover = HoverTool()
hovertooltips =hover.tooltips = """
  <div>
    <h3>@brand</h3>
    <div><img src="@brand_logo" alt="" width="200" /></div>
  </div>
"""
p.add_tools(hover)
show(p)


