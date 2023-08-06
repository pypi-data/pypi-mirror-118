# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.

import unittest
import numpy as np
from shapelets.model.view_match import View

from shapelets.dsl.data_app_panel import (
    GridPanel,
    HorizontalFlowPanel,
    VerticalFlowPanel, TabsFlowPanel
)
from shapelets.dsl.data_app_widgets import (
    Button,
    DonutChart,
    Label,
    LineChart,
    Markdown,
    MetadataField,
    MetadataFilter,
    MultiSequenceSelector,
    Number,
    PieChart,
    PolarArea,
    RadarArea,
    ScatterPlot,
    SequenceSelector, Date, Text, Table
)
from shapelets.model import (
    Collection,
    MetadataType,
    NDArray,
    Sequence,
    SequenceBaseTypeEnum,
    SequenceDensityEnum, Dataframe)

categories_str = ["1", "2", "3", "4", "5"]
x_axis_int = [1, 2, 3, 4, 5]
y_axis_int = [1, 2, 3, 4, 5]
data_int = [10, 9, 8, 7, 6]


class WidgetDataAppTest(unittest.TestCase):

    def test_number(self):
        number = Number(widget_id="widget_id_1",
                        name="number_1",
                        default_value=3,
                        value_type=int)
        expected_result = {
            'id': 'widget_id_1',
            'name': 'number_1',
            'draggable': False,
            'resizable': False,
            'disabled': False,
            'type': 'Number',
            'properties': {
                'value': 3,
                'type': 'INTEGER'
            }
        }
        self.assertEqual(number.to_dict_widget(), expected_result)

    def test_date(self):
        date = Date(title="Date title", date=1627292707575, min_date=1627292507575, max_date=1627292907575)
        date_dict = date.to_dict_widget()
        self.assertEqual(date_dict["name"], "Date")
        self.assertEqual(date_dict["properties"]["title"], "Date title")
        self.assertEqual(date_dict["properties"]["date"], 1627292707575)
        self.assertEqual(date_dict["properties"]["minDate"], 1627292507575)
        self.assertEqual(date_dict["properties"]["maxDate"], 1627292907575)

    def test_text(self):
        text = Text(title="Text title", text="Hello world")
        text_dict = text.to_dict_widget()
        self.assertEqual(text_dict["name"], "Text")
        self.assertEqual(text_dict["properties"]["title"], "Text title")
        self.assertEqual(text_dict["properties"]["text"], "Hello world")

    def test_button(self):
        button = Button(widget_id="widget_id_4",
                        widget_name="button1",
                        text_button="Click para sumar x + y")
        expected_result = {'id': 'widget_id_4',
                           'name': 'button1',
                           'draggable': False,
                           'resizable': False,
                           'disabled': False,
                           'type': 'Button',
                           'properties':
                               {'text': 'Click para sumar x + y',
                                'events': []
                                }
                           }

        self.assertEqual(button.to_dict_widget(), expected_result)

    def test_metadata_filter(self):
        collection = Collection("Merceditas")
        metadata_1 = MetadataField("INDUSTRY", MetadataType.STRING, collection)
        metadata_2 = MetadataField("DATA_QUALITY_INDEX", MetadataType.DOUBLE, collection)
        metadata_3 = MetadataField("LAT_LNG_COORDINATES", MetadataType.GEOHASH, collection)
        metadata_filter = MetadataFilter(metadata_elements=[metadata_1, metadata_2, metadata_3],
                                         widget_id="widget_id_2",
                                         name="metadata_filter",
                                         title="Metadata Filter")
        expected_result = {
            'id': 'widget_id_2',
            'name': 'metadata_filter',
            'draggable': False,
            'resizable': False,
            'disabled': False,
            'type': 'MetadataFilter',
            'properties': {'metadataFields':
                [
                    ['INDUSTRY', 'String'],
                    ['DATA_QUALITY_INDEX', 'Double'],
                    ['LAT_LNG_COORDINATES', 'Coordinates']
                ],
                'title': 'Metadata Filter'
            }
        }
        self.assertEqual(metadata_filter.to_dict_widget(), expected_result)

    def test_horizontal_panel(self):
        horizontal_panel = HorizontalFlowPanel(panel_title="Operands",
                                               panel_id="Horizontal_Panel_Id")
        expected_result = {
            'id': 'Horizontal_Panel_Id',
            'name': 'Horizontal_Panel_Id',
            'draggable': False,
            'resizable': False,
            'disabled': False,
            'type': 'HorizontalFlowPanel',
            'properties': {
                "title": "Operands",
                "placements": [],
                'widgets': []
            }
        }
        self.assertEqual(horizontal_panel.to_dict_widget(), expected_result)

    def test_horizontal_panel_with_widget(self):
        horizontal_panel = HorizontalFlowPanel(panel_title="Operands",
                                               panel_id="Horizontal_Panel_Id")
        number = Number(widget_id="widget_id_5",
                        name="number_1",
                        default_value=3,
                        value_type=int)
        horizontal_panel.place(number)
        expected_result = {
            'disabled': False,
            'draggable': False,
            'id': 'Horizontal_Panel_Id',
            'name': 'Horizontal_Panel_Id',
            'resizable': False,
            'type': 'HorizontalFlowPanel',
            'properties': {
                'placements': [
                    {
                        'offset': 0,
                        'widgetRef': 'widget_id_5',
                        'width': 1
                    }
                ],
                'title': 'Operands',
                'widgets': [
                    {
                        'disabled': False,
                        'draggable': False,
                        'id': 'widget_id_5',
                        'name': 'number_1',
                        'properties': {'type': 'INTEGER', 'value': 3},
                        'resizable': False,
                        'type': 'Number'
                    }
                ]
            }
        }
        self.assertEqual(horizontal_panel.to_dict_widget(), expected_result)

    def test_vertical_panel_with_widget(self):
        vertical_panel = VerticalFlowPanel(panel_title="Operands",
                                           panel_id="Vertical_Panel_Id")
        number = Number(widget_id="widget_id_5",
                        name="number_1",
                        default_value=3,
                        value_type=int)
        vertical_panel.place(number)
        expected_result = {
            'disabled': False,
            'draggable': False,
            'id': 'Vertical_Panel_Id',
            'name': 'Vertical_Panel_Id',
            'properties': {
                'title': 'Operands',
                'widgets': [
                    {
                        'disabled': False,
                        'draggable': False,
                        'id': 'widget_id_5',
                        'name': 'number_1',
                        'properties': {'type': 'INTEGER', 'value': 3},
                        'resizable': False,
                        'type': 'Number'
                    }
                ]
            },
            'resizable': False,
            'type': 'VerticalFlowPanel'
        }
        self.assertEqual(vertical_panel.to_dict_widget(), expected_result)

    def test_grid_panel_with_widget(self):
        grid_panel = GridPanel(num_rows=5,
                               num_cols=5,
                               panel_title="Operands",
                               panel_id="Grid_Panel_Id")
        number = Number(widget_id="widget_id_5",
                        name="number_1",
                        default_value=3,
                        value_type=int)
        grid_panel.place(widget=number, row=1, col=1, row_span=3, col_span=2)
        expected_result = {
            'disabled': False,
            'draggable': False,
            'id': 'Grid_Panel_Id',
            'name': 'Grid_Panel_Id',
            'resizable': False,
            'type': 'GridPanel',
            'properties': {
                'numCols': 5,
                'numRows': 5,
                'placements': [{'col': 1,
                                'colSpan': 2,
                                'row': 1,
                                'rowSpan': 3,
                                'widgetRef': 'widget_id_5'}],
                'title': 'Operands',
                'widgets': [
                    {
                        'disabled': False,
                        'draggable': False,
                        'id': 'widget_id_5',
                        'name': 'number_1',
                        'properties': {'type': 'INTEGER', 'value': 3},
                        'resizable': False,
                        'type': 'Number'
                    }
                ]
            }
        }
        self.assertEqual(grid_panel.to_dict_widget(), expected_result)

    def test_grid_panel_with_widget_out_of_bounds(self):
        grid_panel = GridPanel(num_rows=5,
                               num_cols=5,
                               panel_title="Operands",
                               panel_id="Grid_Panel_Id")
        number = Number(widget_id="widget_id_5",
                        name="number_1",
                        default_value=3,
                        value_type=int)
        with self.assertRaises(IndexError):
            grid_panel.place(widget=number, row=4, col=1, row_span=3, col_span=2)

    def test_tabs_flow_panel(self):
        tabs_flow_panel = TabsFlowPanel(panel_title="Panel_title", panel_id="Panel_id")
        number = Number(widget_id="number_1", name="number_1", default_value=1, value_type=int)
        number2 = Number(widget_id="number_2", name="number_2", default_value=2, value_type=int)
        tabs_flow_panel.place(number, "Tab 1")
        tabs_flow_panel.place(number2, "Tab 2")

        expected_result = {
            'disabled': False,
            'draggable': False,
            'id': 'Panel_id',
            'name': 'Panel_id',
            'resizable': False,
            'type': 'TabsFlowPanel',
            'properties': {
                'tabs': [
                    {
                        'title': 'Tab 1',
                    },
                    {
                        'title': 'Tab 2',
                    }
                ],
                'title': 'Panel_title',
                'widgets': [
                    {
                        'disabled': False,
                        'draggable': False,
                        'id': 'number_1',
                        'name': 'number_1',
                        'properties': {'type': 'INTEGER', 'value': 1},
                        'resizable': False,
                        'type': 'Number'
                    },
                    {
                        'disabled': False,
                        'draggable': False,
                        'id': 'number_2',
                        'name': 'number_2',
                        'properties': {'type': 'INTEGER', 'value': 2},
                        'resizable': False,
                        'type': 'Number'
                    }
                ]
            }
        }
        self.assertEqual(tabs_flow_panel.to_dict_widget(), expected_result)

    def test_line_chart_with_sequence(self):
        seq = Sequence(
            "sequence_id_1",
            "sequence_1", None, 0, 0, None,
            SequenceDensityEnum.DENSE,
            SequenceBaseTypeEnum.NUMERICAL)
        line_chart_with_seq = LineChart(sequence=seq,
                                        title="Third Sequence",
                                        widget_id="widget_id_6")
        expected_result = {
            'id': 'widget_id_6',
            'name': 'LineChart',
            'draggable': False,
            'resizable': False,
            'disabled': False,
            'type': 'LineChart:Sequence',
            'properties': {
                'sequenceId': 'sequence_id_1',
                'title': 'Third Sequence'
            }
        }
        self.assertEqual(line_chart_with_seq.to_dict_widget(), expected_result)

    def test_line_chart_with_nd_array(self):
        x_axis = NDArray(nd_array_id="x_axis_nd_array_id",
                         name="x-axis",
                         description="x-axis description",
                         dtype=np.dtype("int"),
                         dims=(100,))
        y_axis = NDArray(nd_array_id="y_axis_nd_array_id",
                         name="y-axis",
                         description="y-axis description",
                         dtype=np.dtype("float64"),
                         dims=(100,))
        line_chart_with_nd_array = LineChart(x_axis=x_axis,
                                             y_axis=y_axis,
                                             title="Third Sequence",
                                             widget_id="line_chart_with_nd_array_id")
        expected_result = {
            'id': 'line_chart_with_nd_array_id',
            'name': 'LineChart',
            'type': 'LineChart:NDArray',
            'draggable': False,
            'resizable': False,
            'disabled': False,
            'properties': {
                'title': 'Third Sequence',
                'xAxis': 'x_axis_nd_array_id',
                'yAxis': 'y_axis_nd_array_id'
            }
        }
        self.assertEqual(line_chart_with_nd_array.to_dict_widget(), expected_result)

    def test_line_chart_data(self):
        line_chart_with_data = LineChart(x_axis=x_axis_int,
                                         y_axis=y_axis_int,
                                         title="Linechart with data",
                                         widget_id="line_chart_with_data")
        expected_result = {
            'id': 'line_chart_with_data',
            'name': 'LineChart',
            'type': 'LineChart',
            'draggable': False,
            'resizable': False,
            'disabled': False,
            'properties': {
                'title': 'Linechart with data',
                'xAxis': x_axis_int,
                'yAxis': y_axis_int
            }
        }
        self.assertEqual(line_chart_with_data.to_dict_widget(), expected_result)

    def test_sequence_selector(self):
        seq1 = Sequence(
            "sequence_id_1",
            "sequence_1", None, 0, 0, None,
            SequenceDensityEnum.DENSE,
            SequenceBaseTypeEnum.NUMERICAL)
        seq2 = Sequence(
            "sequence_id_2",
            "sequence_2", None, 0, 0, None,
            SequenceDensityEnum.DENSE,
            SequenceBaseTypeEnum.NUMERICAL)
        sequence_selector = SequenceSelector(sequences=[seq1, seq2],
                                             default_sequence=seq1,
                                             title="Sequence Selector",
                                             name="SequenceSelector",
                                             widget_id="widget_id_8")
        expected_result = {
            'id': 'widget_id_8',
            'name': 'SequenceSelector',
            'draggable': False,
            'resizable': False,
            'disabled': False,
            'type': 'SequenceSelector',
            'properties': {
                'sequenceIds': ['sequence_id_1', 'sequence_id_2'],
                'title': 'Sequence Selector',
                'default': 'sequence_id_1'
            }
        }
        self.assertEqual(sequence_selector.to_dict_widget(), expected_result)

    def test_multi_sequence_selector(self):
        seq1 = Sequence(
            "sequence_id_1",
            "sequence_1", None, 0, 0, None,
            SequenceDensityEnum.DENSE,
            SequenceBaseTypeEnum.NUMERICAL)
        seq2 = Sequence(
            "sequence_id_2",
            "sequence_2", None, 0, 0, None,
            SequenceDensityEnum.DENSE,
            SequenceBaseTypeEnum.NUMERICAL)
        seq3 = Sequence(
            "sequence_id_3",
            "sequence_3", None, 0, 0, None,
            SequenceDensityEnum.DENSE,
            SequenceBaseTypeEnum.NUMERICAL)
        sequence_selector = MultiSequenceSelector(sequences=[seq1, seq2, seq3],
                                                  default_sequence=[seq1, seq3],
                                                  title="Sequence Selector",
                                                  name="SequenceSelector",
                                                  widget_id="widget_id_8")
        expected_result = {
            'id': 'widget_id_8',
            'name': 'SequenceSelector',
            'draggable': False,
            'resizable': False,
            'disabled': False,
            'type': 'MultiSequenceSelector',
            'properties': {
                'sequenceIds': ['sequence_id_1', 'sequence_id_2', 'sequence_id_3'],
                'title': 'Sequence Selector',
                'default': ['sequence_id_1', 'sequence_id_3']
            }
        }
        self.assertEqual(sequence_selector.to_dict_widget(), expected_result)

    def test_multi_sequence_selector_without_default(self):
        seq1 = Sequence(
            "sequence_id_1",
            "sequence_1", None, 0, 0, None,
            SequenceDensityEnum.DENSE,
            SequenceBaseTypeEnum.NUMERICAL)
        seq2 = Sequence(
            "sequence_id_2",
            "sequence_2", None, 0, 0, None,
            SequenceDensityEnum.DENSE,
            SequenceBaseTypeEnum.NUMERICAL)
        sequence_selector = MultiSequenceSelector(sequences=[seq1, seq2],
                                                  title="Sequence Selector",
                                                  name="SequenceSelector",
                                                  widget_id="widget_id_8")
        expected_result = {
            'id': 'widget_id_8',
            'name': 'SequenceSelector',
            'draggable': False,
            'resizable': False,
            'disabled': False,
            'type': 'MultiSequenceSelector',
            'properties': {
                'sequenceIds': ['sequence_id_1', 'sequence_id_2'],
                'title': 'Sequence Selector'
            }
        }
        self.assertEqual(sequence_selector.to_dict_widget(), expected_result)

    def test_label(self):
        label = Label(text="My First Label",
                      widget_id="widget_id_9")
        expected_result = {
            'id': 'widget_id_9',
            'name': 'Label',
            'draggable': False,
            'resizable': False,
            'disabled': False,
            'type': 'Label',
            'properties': {
                'text': 'My First Label'
            }
        }
        self.assertEqual(label.to_dict_widget(), expected_result)

    def test_table(self):
        dataframe = Dataframe(dataframe_id="1234", name="Dataframe", description="Dataframe", n_cols=2, n_rows=3,
                              col_names=["Col1", "Col2"], col_types=["float64", "float64"], has_index=True,
                              index_type="float64")
        table = Table(dataframe)
        expected_properties = {
            "data": "1234"
        }
        self.assertEqual(table.to_dict_widget()["properties"], expected_properties)

    def test_markdown(self):
        text = "My text for a markdown"
        markdown = Markdown(text=text,
                            widget_id="widget_id_10")
        expected_result = {
            'id': 'widget_id_10',
            'name': 'Label',
            'draggable': False,
            'resizable': False,
            'disabled': False,
            'type': 'Markdown',
            'properties': {
                'text': 'My text for a markdown'
            }
        }
        self.assertEqual(markdown.to_dict_widget(), expected_result)

    def test_pie_chart(self):
        categories = NDArray(nd_array_id="categories_nd_array_id",
                             name="categories",
                             description="categories description",
                             dtype=np.dtype("float64"),
                             dims=(3, 5))
        data = NDArray(nd_array_id="data_nd_array_id",
                       name="data",
                       description="data description",
                       dtype=np.dtype("float64"),
                       dims=(3, 5))

        pie_chart = PieChart(categories=categories,
                             data=data,
                             name="Pie Chart",
                             title="Pie Chart Title",
                             widget_id="pie_area_id")

        expected_result = {
            'id': 'pie_area_id',
            'name': 'Pie Chart',
            'type': 'PieChart',
            'draggable': False,
            'resizable': False,
            'disabled': False,
            'properties': {
                'categories': 'categories_nd_array_id',
                'data': 'data_nd_array_id',
                'title': 'Pie Chart Title'
            }
        }

        self.assertEqual(pie_chart.to_dict_widget(), expected_result)

    def test_pie_chart_data(self):
        pie_chart_int = PieChart(categories=categories_str,
                                 data=data_int,
                                 name="Pie Chart",
                                 title="Pie Chart Title",
                                 widget_id="pie_area_id")

        expected_result = {
            'id': 'pie_area_id',
            'name': 'Pie Chart',
            'type': 'PieChart',
            'draggable': False,
            'resizable': False,
            'disabled': False,
            'properties': {
                'categories': categories_str,
                'data': data_int,
                'title': 'Pie Chart Title'
            }
        }
        self.assertEqual(pie_chart_int.to_dict_widget(), expected_result)

    def test_scatter_plot(self):
        x_axis = NDArray(nd_array_id="x_axis_nd_array_id",
                         name="fluffiness",
                         description="fluffiness description",
                         dtype=np.dtype("float64"),
                         dims=(0.1, 0.2, 0.3, 0.4, 0.5))

        y_axis = NDArray(nd_array_id="y_axis_nd_array_id",
                         name="iq",
                         description="iq description",
                         dtype=np.dtype("float64"),
                         dims=(10, 20, 30, 60, 120))

        scatter_plot = ScatterPlot(x_axis=x_axis,
                                   y_axis=y_axis,
                                   name="ScatterPlot chart",
                                   title="ScatterPlot title",
                                   widget_id="scatterplot_id")

        expected_result_simple = {
            'id': 'scatterplot_id',
            'name': 'ScatterPlot chart',
            'type': 'ScatterPlot',
            'draggable': False,
            'resizable': False,
            'disabled': False,
            'properties': {
                'xAxis': 'x_axis_nd_array_id',
                'yAxis': 'y_axis_nd_array_id',
                'trendLine': False,
                'title': 'ScatterPlot title'
            }
        }
        self.assertEqual(scatter_plot.to_dict_widget(), expected_result_simple)

    def test_scatter_plot_size(self):
        x_axis = NDArray(nd_array_id="x_axis_nd_array_id",
                         name="fluffiness",
                         description="fluffiness description",
                         dtype=np.dtype("float64"),
                         dims=(0.1, 0.2, 0.3, 0.4, 0.5))

        y_axis = NDArray(nd_array_id="y_axis_nd_array_id",
                         name="iq",
                         description="iq description",
                         dtype=np.dtype("float64"),
                         dims=(10, 20, 30, 60, 120))

        size = NDArray(nd_array_id="size_nd_array_id",
                       name="count",
                       description="count description",
                       dtype=np.dtype("float64"),
                       dims=(1, 3, 1, 5, 2))

        scatter_size = ScatterPlot(x_axis=x_axis,
                                   y_axis=y_axis,
                                   size=size,
                                   name="ScatterPlot chart with size",
                                   title="ScatterPlot chart with size title",
                                   widget_id="scatterplot_id_2")
        expected_result_size = {
            'id': 'scatterplot_id_2',
            'name': 'ScatterPlot chart with size',
            'type': 'ScatterPlot',
            'draggable': False,
            'resizable': False,
            'disabled': False,
            'properties': {
                'xAxis': 'x_axis_nd_array_id',
                'yAxis': 'y_axis_nd_array_id',
                'trendLine': False,
                'size': 'size_nd_array_id',
                'title': 'ScatterPlot chart with size title'
            }
        }
        self.assertEqual(scatter_size.to_dict_widget(), expected_result_size)

    def test_scatter_plot_color(self):
        x_axis = NDArray(nd_array_id="x_axis_nd_array_id",
                         name="fluffiness",
                         description="fluffiness description",
                         dtype=np.dtype("float64"),
                         dims=(0.1, 0.2, 0.3, 0.4, 0.5))

        y_axis = NDArray(nd_array_id="y_axis_nd_array_id",
                         name="iq",
                         description="iq description",
                         dtype=np.dtype("float64"),
                         dims=(10, 20, 30, 60, 120))

        color = NDArray(nd_array_id="color_nd_array_id",
                        name="score",
                        description="score description",
                        dtype=np.dtype("float64"),
                        dims=(1, 3, 8, 6, 3.5))

        scatter_color = ScatterPlot(x_axis=x_axis,
                                    y_axis=y_axis,
                                    color=color,
                                    name="ScatterPlot chart with color",
                                    title="ScatterPlot chart with color title",
                                    widget_id="scatterplot_id_3")
        expected_result_color = {
            'id': 'scatterplot_id_3',
            'name': 'ScatterPlot chart with color',
            'type': 'ScatterPlot',
            'draggable': False,
            'resizable': False,
            'disabled': False,
            'properties': {
                'xAxis': 'x_axis_nd_array_id',
                'yAxis': 'y_axis_nd_array_id',
                'trendLine': False,
                'color': 'color_nd_array_id',
                'title': 'ScatterPlot chart with color title'
            }
        }
        self.assertEqual(scatter_color.to_dict_widget(), expected_result_color)

    def test_scatter_plot_both(self):
        x_axis = NDArray(nd_array_id="x_axis_nd_array_id",
                         name="fluffiness",
                         description="fluffiness description",
                         dtype=np.dtype("float64"),
                         dims=(0.1, 0.2, 0.3, 0.4, 0.5))

        y_axis = NDArray(nd_array_id="y_axis_nd_array_id",
                         name="iq",
                         description="iq description",
                         dtype=np.dtype("float64"),
                         dims=(10, 20, 30, 60, 120))

        size = NDArray(nd_array_id="size_nd_array_id",
                       name="count",
                       description="count description",
                       dtype=np.dtype("float64"),
                       dims=(1, 3, 1, 5, 2))

        color = NDArray(nd_array_id="color_nd_array_id",
                        name="score",
                        description="score description",
                        dtype=np.dtype("float64"),
                        dims=(1, 3, 8, 6, 3.5))

        scatter_both = ScatterPlot(x_axis=x_axis,
                                   y_axis=y_axis,
                                   color=color,
                                   size=size,
                                   name="ScatterPlot chart with both",
                                   title="ScatterPlot chart with both title",
                                   widget_id="scatterplot_id_4")
        expected_result_both = {
            'id': 'scatterplot_id_4',
            'name': 'ScatterPlot chart with both',
            'type': 'ScatterPlot',
            'draggable': False,
            'resizable': False,
            'disabled': False,
            'properties': {
                'xAxis': 'x_axis_nd_array_id',
                'yAxis': 'y_axis_nd_array_id',
                'trendLine': False,
                'color': 'color_nd_array_id',
                'size': 'size_nd_array_id',
                'title': 'ScatterPlot chart with both title'
            }
        }
        self.assertEqual(scatter_both.to_dict_widget(), expected_result_both)

    def test_scatter_plot_data(self):
        scatter_with_data = ScatterPlot(x_axis=x_axis_int,
                                        y_axis=y_axis_int,
                                        name="ScatterPlot chart with data",
                                        title="ScatterPlot chart with data title",
                                        widget_id="scatterplot_id_5")
        expected_with_data = {
            'id': 'scatterplot_id_5',
            'name': 'ScatterPlot chart with data',
            'type': 'ScatterPlot',
            'draggable': False,
            'resizable': False,
            'disabled': False,
            'properties': {
                'xAxis': x_axis_int,
                'yAxis': y_axis_int,
                'trendLine': False,
                'title': 'ScatterPlot chart with data title'
            }
        }
        self.assertEqual(scatter_with_data.to_dict_widget(), expected_with_data)

    def test_donut_chart(self):
        categories = NDArray(nd_array_id="categories_nd_array_id",
                             name="categories",
                             description="categories description",
                             dtype=np.dtype("float64"),
                             dims=(3, 5))

        data = NDArray(nd_array_id="data_nd_array_id",
                       name="data",
                       description="data description",
                       dtype=np.dtype("float64"),
                       dims=(3, 5))

        donut_chart = DonutChart(categories=categories,
                                 data=data,
                                 name="Donut Chart",
                                 title="Donut Chart Title",
                                 widget_id="donut_id")
        expected_result = {
            'id': 'donut_id',
            'name': 'Donut Chart',
            'type': 'DonutChart',
            'draggable': False,
            'resizable': False,
            'disabled': False,
            'properties': {
                'categories': 'categories_nd_array_id',
                'data': 'data_nd_array_id',
                'title': 'Donut Chart Title'
            }
        }
        self.assertEqual(donut_chart.to_dict_widget(), expected_result)

    def test_donut_chart_data(self):
        donut_chart_with_data = DonutChart(categories=categories_str,
                                           data=data_int,
                                           name="Donut Chart with data",
                                           title="Donut Chart with data Title",
                                           widget_id="donut_id_data")
        expected_result = {
            'id': 'donut_id_data',
            'name': 'Donut Chart with data',
            'type': 'DonutChart',
            'draggable': False,
            'resizable': False,
            'disabled': False,
            'properties': {
                'categories': categories_str,
                'data': data_int,
                'title': 'Donut Chart with data Title'
            }
        }
        self.assertEqual(donut_chart_with_data.to_dict_widget(), expected_result)

    def test_polar_area(self):
        categories = NDArray(nd_array_id="categories_nd_array_id",
                             name="categories",
                             description="categories description",
                             dtype=np.dtype("float64"),
                             dims=(3, 5))
        data = NDArray(nd_array_id="data_nd_array_id",
                       name="data",
                       description="data description",
                       dtype=np.dtype("float64"),
                       dims=(3, 5))

        polar_area = PolarArea(categories=categories,
                               data=data,
                               name="Polar Area",
                               title="Polar Area Title",
                               widget_id="polar_area_id")
        expected_result = {
            'id': 'polar_area_id',
            'name': 'Polar Area',
            'type': 'PolarArea',
            'draggable': False,
            'resizable': False,
            'disabled': False,
            'properties': {
                'categories': 'categories_nd_array_id',
                'data': 'data_nd_array_id',
                'title': 'Polar Area Title'
            }
        }
        self.assertEqual(polar_area.to_dict_widget(), expected_result)

    def test_polar_area_data(self):
        polar_area_with_data = PolarArea(categories=categories_str,
                                         data=data_int,
                                         name="Polar Area with data",
                                         title="Polar Area with data Title",
                                         widget_id="polar_area_id_data")
        expected_result = {
            'id': 'polar_area_id_data',
            'name': 'Polar Area with data',
            'type': 'PolarArea',
            'draggable': False,
            'resizable': False,
            'disabled': False,
            'properties': {
                'categories': categories_str,
                'data': data_int,
                'title': 'Polar Area with data Title'
            }
        }
        self.assertEqual(polar_area_with_data.to_dict_widget(), expected_result)

    def test_radar_area(self):
        categories = NDArray(nd_array_id="categories_nd_array_id",
                             name="categories",
                             description="categories description",
                             dtype=np.dtype("float64"),
                             dims=(3, 5))
        data = NDArray(nd_array_id="data_nd_array_id",
                       name="data",
                       description="data description",
                       dtype=np.dtype("float64"),
                       dims=(3, 5))

        groups = NDArray(nd_array_id="groups_nd_array_id",
                         name="groups",
                         description="groups description",
                         dtype=np.dtype("float64"),
                         dims=(3, 5))

        radar_area = RadarArea(categories=categories,
                               data=data,
                               groups=groups,
                               name="Radar Area",
                               title="Radar Area Title",
                               widget_id="radar_area_id")

        radar_area_with_data = RadarArea(categories=categories_str,
                                         data=data_int,
                                         groups=data_int,
                                         name="Radar Area with data",
                                         title="Radar Area with data Title",
                                         widget_id="radar_area_id_data")
        expected_result = {
            'id': 'radar_area_id',
            'name': 'Radar Area',
            'type': 'RadarArea',
            'draggable': False,
            'resizable': False,
            'disabled': False,
            'properties': {
                'categories': 'categories_nd_array_id',
                'data': 'data_nd_array_id',
                'groups': 'groups_nd_array_id',
                'title': 'Radar Area Title'
            }
        }
        expected_result_with_data = {
            'id': 'radar_area_id_data',
            'name': 'Radar Area with data',
            'type': 'RadarArea',
            'draggable': False,
            'resizable': False,
            'disabled': False,
            'properties': {
                'categories': categories_str,
                'data': data_int,
                'groups': data_int,
                'title': 'Radar Area with data Title'
            }
        }
        self.assertEqual(radar_area.to_dict_widget(), expected_result)
        self.assertEqual(radar_area_with_data.to_dict_widget(), expected_result_with_data)

    def test_radar_area_data(self):
        radar_area_with_data = RadarArea(categories=categories_str,
                                         data=data_int,
                                         groups=data_int,
                                         name="Radar Area with data",
                                         title="Radar Area with data Title",
                                         widget_id="radar_area_id_data")
        expected_result = {
            'id': 'radar_area_id_data',
            'name': 'Radar Area with data',
            'type': 'RadarArea',
            'draggable': False,
            'resizable': False,
            'disabled': False,
            'properties': {
                'categories': categories_str,
                'data': data_int,
                'groups': data_int,
                'title': 'Radar Area with data Title'
            }
        }
        self.assertEqual(radar_area_with_data.to_dict_widget(), expected_result)
