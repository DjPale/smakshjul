import matplotlib.pyplot as plt
import numpy as np
import math
import csv 


def read_data(fname):
    with open(fname, encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)

        data = []

        skipped = False
        for row in reader:
            if not skipped:
                skipped = True
            else:
                data.append(row)

    return data

def fetch_category_data(vals, data_idx: int, color_idx: int):
    # didn't find another easy way to re-combine arrays
    cols = np.column_stack((vals[:,data_idx], vals[:,color_idx]))
    # fetch colors
    idx = np.unique(cols[:,1], return_index=True)[1]
    # sort them since they were sorted on the way out
    #idx = idx.argsort()[::-1]
    idx.sort()
    # refetch the indexes in the correct order and convert to int
    o_colors = cols[idx][:,1].astype(int)[::-1]

    # fetch category data with counts
    idx, counts = np.unique(cols[:,0], return_index=True, return_counts=True)[1:]
    # construct a new array combined with counts to be able to sort them
    sub_tot = np.column_stack((idx, counts))
    # mind-blowing way to return sorted indixes based on first column
    # also note that this is inverted since the data direction is different from the labeling direction
    o_data = sub_tot[sub_tot[:,0].argsort()[::-1]] 

    return (o_colors, o_data[:,1])


data = read_data('smakshjul-data-small.csv')

fig, ax = plt.subplots(figsize=(13,12))

outer_radius = 1.6
outer_size = 0.63
mid_size = 0.4
mid_radius = outer_radius - outer_size
inner_radius = mid_radius - mid_size
text_margin = 0.02

vals = np.array(data)

o_colors, o_data = fetch_category_data(vals, 2, 4)
i_colors, i_data = fetch_category_data(vals, 1, 4)

cmap = plt.colormaps["tab20b"]
outer_colors = cmap(o_colors)
mid_colors = cmap(o_colors)
inner_colors = cmap(i_colors)

angle_step = 360.0 / len(data)

angle = 90
angle_ofs = 0
ha = 'left'

start_angle = angle + angle_step / 2

ax.pie(o_data, radius=outer_radius, colors=outer_colors,
       startangle=start_angle,
       wedgeprops=dict(width=outer_size, edgecolor='w'))

ax.pie(o_data, radius=mid_radius, colors=mid_colors,
       startangle=start_angle,
       wedgeprops=dict(width=mid_size, edgecolor='w'))

ax.pie(i_data, radius=inner_radius, colors=inner_colors,
       startangle=start_angle,
       wedgeprops=dict(edgecolor='w'))

ax.set(aspect="equal")

for line in data:
    r_a = math.radians(angle)

    o_pos = (mid_radius + text_margin)
    m_pos = (inner_radius + text_margin)
    i_pos = (0.2 + text_margin)

    x = o_pos * math.cos(r_a)
    y = o_pos * math.sin(r_a)

    # outer text
    tx = ax.text(x, y, str.upper(line[0]),
                            size=10, rotation=angle + angle_ofs,
                            horizontalalignment=ha, verticalalignment='center',
                            rotation_mode='anchor',
                            transform=ax.transData)
    
    x = m_pos * math.cos(r_a)
    y = m_pos * math.sin(r_a)

    tx = ax.text(x, y, str.upper(line[2]),
                            size=10, rotation=angle + angle_ofs,
                            horizontalalignment=ha, verticalalignment='center',
                            rotation_mode='anchor',
                            transform=ax.transData)
    

    x = i_pos * math.cos(r_a)
    y = i_pos * math.sin(r_a)

    # tx = ax.text(x, y, str.upper(line[1]),
    #                         size=10, rotation=angle + angle_ofs,
    #                         horizontalalignment=ha, verticalalignment='center',
    #                         rotation_mode='anchor',
    #                         transform=ax.transData)

    angle -= angle_step

    if angle < -90:
        ha = 'right'
        angle_ofs = 180


plt.show()