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


data = read_data('smakshjul-data.csv')

fig, ax = plt.subplots(figsize=(13,12))

outer_radius = 1.6
outer_size = 0.63
mid_size = 0.4
mid_radius = outer_radius - outer_size
inner_radius = mid_radius - mid_size
text_margin = 0.02

vals = np.array([[60., 32.], [37., 40.], [29., 10.]])

cmap = plt.colormaps["tab20c"]
outer_colors = cmap([1, 2, 5, 6, 9, 10])
mid_colors = cmap(np.arange(3)*4)
inner_colors = cmap([2, 6, 10])

ax.pie(vals.sum(axis=1), radius=outer_radius, colors=outer_colors,
       wedgeprops=dict(width=outer_size, edgecolor='w'))

ax.pie(vals.flatten(), radius=mid_radius, colors=mid_colors,
       wedgeprops=dict(width=mid_size, edgecolor='w'))

ax.pie(vals.flatten(), radius=inner_radius, colors=inner_colors,
       wedgeprops=dict(edgecolor='w'))

ax.set(aspect="equal")

angle_step = 360.0 / len(data)

angle = 90
angle_ofs = 0
ha = 'left'


for line in data:
    r_a = math.radians(angle)
    x = (mid_radius + text_margin) * math.cos(r_a)
    y = (mid_radius + text_margin) * math.sin(r_a)

    tx = ax.text(x, y, str.upper(line[0]),
                            size=10, rotation=angle + angle_ofs,
                            horizontalalignment=ha, verticalalignment='center',
                            rotation_mode='anchor',
                            transform=ax.transData)
    angle -= angle_step

    if angle < -90:
        ha = 'right'
        angle_ofs = 180


plt.show()