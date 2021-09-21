import PyQt5.QtWidgets as Qtw

from widgets.general_hint import GeneralHintWidget
from widgets.graph import GraphWidget

from graph.element import GraphLayer, GraphNode, GraphLink

from graph.extractor import MonthExtractor


class PlotWidget(Qtw.QWidget):
    """
    Widget for the plot tab
    """
    def __init__(self, parent=None, models=None):
        super(PlotWidget, self).__init__(parent)

        self.extractor = MonthExtractor(models)

        self.graph = GraphWidget(self)
        self.info = GeneralHintWidget(self)

        self.graph.hovered_changed.connect(self.info.update_item)

        self.extract()

        """
        # feed test data
        l_start = GraphLayer()
        l_start.nodes.append(GraphNode(500, "#ff0000"))
        l_start.nodes.append(GraphNode(100, "#0000ff"))
        l_end = GraphLayer()
        l_end.nodes.append(GraphNode(400, "#ffff00"))
        l_end.nodes.append(GraphNode(100, "#0080ff"))
        l_end.nodes.append(GraphNode(60, "#008000"))
        l_end.nodes.append(GraphNode(40, "#909090"))
        l_store = GraphLayer()
        l_store.nodes.append(GraphNode(600, "#202020"))
        lns = []
        lns.append(GraphLink(l_start.nodes[0], l_end.nodes[0], 350))
        lns.append(GraphLink(l_start.nodes[0], l_end.nodes[1], 100))
        lns.append(GraphLink(l_start.nodes[0], l_end.nodes[2], 30))
        lns.append(GraphLink(l_start.nodes[0], l_end.nodes[3], 20))
        lns.append(GraphLink(l_start.nodes[1], l_end.nodes[0], 50))
        lns.append(GraphLink(l_start.nodes[1], l_end.nodes[2], 30))
        lns.append(GraphLink(l_start.nodes[1], l_end.nodes[3], 20))
        for N in l_end.nodes:
            lns.append(GraphLink(N, l_store.nodes[0], N.amount))
        self.graph.setData([l_start, l_end, l_store], lns)
        """
        """
        layers = [GraphLayer()]
        links = []
        layers[0].nodes.append(GraphNode(100, "#f02020"))
        for i in range(1, 10):
            newL = GraphLayer()
            newL.nodes.append(GraphNode(10, "#808080"))
            links.append(GraphLink(layers[0].nodes[0], layers[-1].nodes[0], 10))
            layers.append(newL)
        layers.append(GraphLayer())
        layers[-1].nodes.append(GraphNode(50, "#2020f0"))
        for i in range(5):
            links.append(GraphLink(layers[i+1].nodes[0], layers[-1].nodes[0], 10))
        self.graph.setData(layers, links)
        """

        # set the layout
        self.graph.setSizePolicy(Qtw.QSizePolicy.Expanding, Qtw.QSizePolicy.Expanding)
        self.info.setSizePolicy(Qtw.QSizePolicy.Fixed, Qtw.QSizePolicy.Expanding)

        layout = Qtw.QHBoxLayout()
        layout.addWidget(self.graph)
        layout.addWidget(self.info)
        self.setLayout(layout)

    def extract(self):
        self.extractor.update()
        self.graph.setData(self.extractor.layers, self.extractor.links)
