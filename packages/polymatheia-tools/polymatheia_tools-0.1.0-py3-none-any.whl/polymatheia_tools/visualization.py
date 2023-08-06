# !/usr/bin/python
# -*- coding: utf-8 -*-

"""This module provides a class for visualizing PICA field distributions."""

import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class FieldVisualization:
    """The :class:`~polymatheia_tools.visualization.FieldVisualization` provides a PICA field visualization.

    After creating a new :class:`~polymatheia_tools.visualization.FieldVisualization` the
    visualization can be started by calling the ``start`` function.
    """

    INFILE = "input_dict_visualization.json"
    OUTFILE = "input_dict_visualized.png"
    _ENCODING = "utf-8"

    @staticmethod
    def start(i, o):
        """Start the visualization.

        :param i: Path to input JSON file
        :type i: ``str``
        :param o: Path to output image file
        :type o: ``str``
        """
        # Load data
        with open(i, 'r', encoding=FieldVisualization._ENCODING) as f:
            data = json.load(f)

        # Get values needed for visualization
        values = []
        for key in data.keys():
            df = pd.DataFrame(data[key])
            values.append((key, df.iloc[0]['in_X_records']))
        values.sort(key=lambda a: a[1], reverse=True)

        # Plotting
        key, frequency = zip(*values)
        indices = np.arange(len(values))
        bars = plt.bar(indices, frequency, color='orange')
        plt.xticks(indices, key, rotation=0)
        for rect in bars:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2.0, height, '%d' % int(height), ha='center', va='bottom')
        plt.xlabel('PICA-Feld')
        plt.ylabel('Anzahl an Datensätzen')
        plt.tight_layout()
        plt.savefig(o)
        plt.show()
