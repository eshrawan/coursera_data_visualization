"""
Project for Week 2 of "Python Data Visualization".
Read World Bank GDP data and create some basic XY plots.

author: @eshrawan
"""

import csv
import pygal


def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      keyfield  - field to use as key for rows
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    table = {}
    with open(filename, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            rowid = row[keyfield]
            table[rowid] = row
    return table


def build_plot_values(gdpinfo, gdpdata):
    """
    Inputs:
      gdpinfo - GDP data information dictionary
      gdpdata - A single country's GDP stored in a dictionary whose
                keys are strings indicating a year and whose values
                are strings indicating the country's corresponding GDP
                for that year.

    Output:
      Returns a list of tuples of the form (year, GDP) for the years
      between "min_year" and "max_year", inclusive, from gdpinfo that
      exist in gdpdata.  The year will be an integer and the GDP will
      be a float.
    """
    list_ex = []
    for key, value in gdpdata.items():
        try:
            if (value != ""):
                if (int(key) <= gdpinfo["max_year"]) and (int(key)  >= gdpinfo["min_year"]):
                    list_ex.append((int(key), float(value)))
        except ValueError:
            pass

    list_ex.sort(key = lambda pair: pair[0])
    return list_ex


def build_plot_dict(gdpinfo, country_list):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names

    Output:
      Returns a dictionary whose keys are the country names in
      country_list and whose values are lists of XY plot values
      computed from the CSV file described by gdpinfo.

      Countries from country_list that do not appear in the
      CSV file should still be in the output dictionary, but
      with an empty XY plot value list.
    """
    plot_dict = {}
    plot_data = read_csv_as_nested_dict(gdpinfo["gdpfile"],
                                       gdpinfo["country_name"],
                                       gdpinfo["separator"], gdpinfo["quote"])
    for country in country_list:
        plot_dict[country] = []
        for key, value in plot_data.items():
            if key == country:
                tuple_x = build_plot_values(gdpinfo, value)
                plot_dict[country] = tuple_x

    return plot_dict


def render_xy_plot(gdpinfo, country_list, plot_file):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names
      plot_file    - String that is the output plot file name

    Output:
      Returns None.

    Action:
      Creates an SVG image of an XY plot for the GDP data
      specified by gdpinfo for the countries in country_list.
      The image will be stored in a file named by plot_file.
    """
    plot = build_plot_dict(gdpinfo, country_list)
    line_chart = pygal.XY(xrange=(1960, 2016))
    line_chart.title = 'Plot of GDP for countries spanning 1960 to 2015'
    line_chart.x_title = 'Year'
    line_chart.y_title = 'GDP in current value of USD'

    for country in country_list:
        for key,item in plot.items():
            try:
                if (key != ""):
                    if key == country:
                        line_chart.add(key, item)
            except ValueError:
                pass
    line_chart.render_to_file(plot_file)
