# smakshjul - generate aroma / flavor wheel from CSV using matplotlib

A simple Pyhton program to generate a flavor / aroma wheel from a CSV data-set. Originally inspired by early versions of Beer Flavor wheel by Mark Dredge which categorizes flavors according to ingredient source.

The data set included is a Norwegian version with data collected from and adapted to [Norbrygg](https://norbrygg.no/) Beer guidelines, but any data set can be used.

## Prerequisites
- [Python 3](https://www.python.org/)
- [matplotlib](https://matplotlib.org/) (`pip install matplotlib`)

## Data set

The data set is a CSV-file with the following columns (from left to right)

- **Flavor descriptor**: The descriptor shown in the _outer section_ of the wheel
- **Base Ingredient**: The base ingredient the flavor originates from and displayed in the _inner section_ of the wheel
- **Ingredient subcategory**: The subcategory which is display in the _middle section_ of the wheel
- **Descriptor Type**: _Currently not in use_ - Category of descriptor (of it appears in aroma, flavor or any other element of the experience)
- **Color Index**: A zero-based index in the `matplotlib` [tab20b](https://matplotlib.org/stable/users/explain/colors/colormaps.html#qualitative) color map

**Note that the data sets must be pre-sorted**!

The first line in the file will correspond to the mid top of the circle and it will plot the labels clockwise around the wheel

## Possible improvements
Things that can be done to improve the program further:

- [x] Support command-line parameters with various options like
  - Toggle mid / inner visibility
  - Scaling
  - Font size
  - Colors
- [ ] Control the inner category color in a better way - now it just picks the first color of the category
- [ ] Merge inner and mid categories if they are identical
- [ ] Some more tweaks to better align font placement
