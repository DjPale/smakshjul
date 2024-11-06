import matplotlib.pyplot as plt
import numpy as np
import math
import csv 
import argparse
from label_plotter import LabelPlotter

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
    # fetch unique categories - the index they "switch" to a new value will determine which color to use
    idx = np.unique(cols[:,0], return_index=True)[1]
    # sort them since they were sorted in the unique-function
    idx.sort()
    # refetch the indexes in the correct order (reversed) and convert to int
    o_colors = cols[idx][:,1].astype(int)[::-1]

    # fetch category data with counts
    idx, counts = np.unique(cols[:,0], return_index=True, return_counts=True)[1:]
    # construct a new array combined with counts to be able to sort them by one column
    sub_tot = np.column_stack((idx, counts))
    # mind-blowing way to return sorted indices based on first column
    # also note that this is inverted since the data direction is different from the text print direction
    o_data = sub_tot[sub_tot[:,0].argsort()[::-1]] 

    return (o_colors, o_data[:,1])

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', default='data/smakshjul-data.csv', help='Specify input CSV file instead of default "data/smakshjul-data.csv"')
    parser.add_argument('-o', '--output', help='Specify file output - extension must be supported by matplotlib, error is thrown if it is not')
    parser.add_argument('-c', '--colormap', default='tab20b', help='Specify matplotlib colormap name instead of default "tab20b"')
    parser.add_argument('--width', type=int, default=13, help='Width of plot in matplotlib units (default=13)')
    parser.add_argument('--height', type=int, default=12, help='Height of plot in matplotlib units (default=12)')
    parser.add_argument('--font-size', type=int, default=10, help='Set default label font size (default=10)')
    parser.add_argument('--no-inner', action='store_true', help='Disable inner plot circle')
    parser.add_argument('--no-middle', action='store_true', help='Disable middle plot circle')
    parser.add_argument('--print-colormaps', action='store_true', help='Print available colormaps and exit')
    return parser.parse_args()

##### Program Start

args = parse_arguments()

if args.print_colormaps:
    print(plt.colormaps())
    exit()

data = read_data(args.file)

fig, ax = plt.subplots(figsize=(args.width, args.height))

outer_radius = 1.6
outer_size = 0.63
mid_size = 0.4
mid_r = outer_radius - outer_size
inner_radius = mid_r - mid_size
text_margin = 0.02

vals = np.array(data)

o_colors, o_data = fetch_category_data(vals, 2, 4)
i_colors, i_data = fetch_category_data(vals, 1, 4)

cmap = plt.colormaps[args.colormap]
outer_colors = cmap(o_colors)
mid_colors = cmap(o_colors)
inner_colors = cmap(i_colors)

angle = 90
angle_step = 360.0 / len(data)
start_angle = angle + angle_step / 2

ax.pie(o_data, radius=outer_radius, colors=outer_colors,
       startangle=start_angle,
       wedgeprops=dict(width=outer_size, edgecolor='w'))

if not args.no_middle:
    ax.pie(o_data, radius=mid_r, colors=mid_colors,
        startangle=start_angle,
        wedgeprops=dict(width=mid_size, edgecolor='w'))

if not args.no_inner:
    ax.pie(i_data, radius=inner_radius, colors=inner_colors,
        startangle=start_angle,
        wedgeprops=dict(edgecolor='w'))

ax.set(aspect="equal")

angle_ofs = 0
horiz_align = 'left'

outer_r = (mid_r + text_margin)
mid_r = (inner_radius + text_margin)
inner_r = (0.2 + text_margin)

outer_labels = LabelPlotter(outer_r, angle_step, start_angle = start_angle, font_size = args.font_size)

if not args.no_middle:
    mid_labels = LabelPlotter(mid_r, angle_step, start_angle = start_angle, font_size = args.font_size)

if not args.no_inner:
    inner_labels = LabelPlotter(inner_r, angle_step, start_angle = start_angle, font_size = args.font_size)

for line in data:
    outer_labels.label_plot(ax, str.upper(line[0]), angle, angle_ofs, horiz_align)

    if not args.no_middle:
        mid_labels.eval_label_plot(ax, str.upper(line[2]), angle, angle_ofs, horiz_align)

    if not args.no_inner:
        inner_labels.eval_label_plot(ax, str.upper(line[1]), angle, angle_ofs, horiz_align)

    angle -= angle_step

    if angle < -90:
        horiz_align = 'right'
        angle_ofs = 180

if not args.no_middle:
    mid_labels.final_label_plot(ax, angle, angle_ofs, horiz_align)
    
if not args.no_inner:
    inner_labels.final_label_plot(ax, angle, angle_ofs, horiz_align)

if args.output:
    plt.savefig(args.output)
else:
    plt.show()
