import PyQt5.QtCore as QtCore


class GraphElement:
    """
    A base class for the elements drawn in the graph widget
    """
    def __init__(self):
        self.info = None


class GraphNode(GraphElement):
    """
    Class containing data for a node in the graph tab
    """
    def __init__(self, amount, color, info=None):
        self.amount = amount
        self.color = color
        self.info = info

        self.selected = False
        self.rect = None

    def __repr__(self):
        return "<Node rect="+str(self.rect)+">"

class GraphLink(GraphElement):
    """
    Class containing data for a link in the graph tab
    """
    def __init__(self, node_start, node_end, amount, info=None):
        self.node_start = node_start
        self.node_end = node_end
        self.amount = amount
        self.info = info

        self.selected = False
        self.path = None


class GraphLayer:
    """
    Class containing data for a layer in the graph tab
    """
    def __init__(self):
        self.nodes = []

    def sort(self):
        self.nodes = sorted(self.nodes, key=lambda n:-n.amount)

    def total(self):
        return sum(n.amount for n in self.nodes)

    def set_position(self, x_off, y_off, width, y_spacing, y_scale):
        for node in self.nodes:
            node_height = int(y_scale*node.amount)
            node.rect = QtCore.QRect(x_off, y_off, width, node_height)
            y_off += node_height + y_spacing

    def __repr__(self):
        return "<Layer nodes="+str(self.nodes)+">"