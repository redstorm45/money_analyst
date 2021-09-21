import PyQt5.QtWidgets as Qtw
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui


class GraphWidget(Qtw.QWidget):
    """
    Widget containing the graph part of the plot tab
    """
    hovered_changed = QtCore.pyqtSignal(list)

    def __init__(self, parent):
        super(GraphWidget, self).__init__(parent)
        self.__spacing = 20
        self.__border = 20
        self.__node_width = 20
        self.__bezier_offset = 0.5

        self.layers = []
        self.links = []
        self.hovered_item = None

        self.setMouseTracking(True)
        self.setMinimumSize(300, 200)

    def setData(self, layers, links):
        # raw data
        print("set data:", layers)
        self.layers = layers
        self.links = sorted(links, key=lambda l:(-l.node_start.amount, -l.node_end.amount))

        for layer in self.layers:
            layer.sort()

        # scale
        self.data_width = len(layers)
        max_nodes = max(len(layer.nodes) for layer in layers)
        self.max_spacing = (max_nodes-1)*self.__spacing

        self.calculate_positions()

    def calculate_positions(self):
        """
        Function to update all the positions of nodes and links
        """
        if len(self.layers) == 0:
            return

        if self.layers[0].total() == 0:
            return

        scr_width = self.width()
        scr_height = self.height()
        x_spacing = (scr_width - 2*self.__border - self.__node_width*self.data_width) // (self.data_width-1)
        y_scale = (scr_height - self.max_spacing - 2*self.__border) / self.layers[0].total()

        # position all node rects
        for i, layer in enumerate(self.layers):
            x_pos = self.__border + i*(self.__node_width + x_spacing)
            y_pos = self.__border + (self.max_spacing - (len(layer.nodes)-1)*self.__spacing)//2
            layer.set_position(x_pos, y_pos, self.__node_width, self.__spacing, y_scale)
            print("set pos of", layer)

        # make all paths for links
        node_offsets_start = {}
        node_offsets_end = {}
        for link in self.links:
            # get the offset of start/end and update them
            id_start = id(link.node_start)
            if id_start not in node_offsets_start:
                node_offsets_start[id_start] = 0
            link_start_offset = node_offsets_start[id_start]
            node_offsets_start[id_start] += link.amount * y_scale

            id_end = id(link.node_end)
            if id_end not in node_offsets_end:
                node_offsets_end[id_end] = 0
            link_end_offset = node_offsets_end[id_end]
            node_offsets_end[id_end] += link.amount * y_scale

            # calculate positions for paths
            start_x = link.node_start.rect.x()+self.__node_width
            start_x_dir = link.node_start.rect.x() + self.__node_width + x_spacing*self.__bezier_offset
            start_y1 = link.node_start.rect.y()+link_start_offset
            start_y2 = link.node_start.rect.y()+link_start_offset+link.amount * y_scale
            end_x = link.node_end.rect.x()
            end_x_dir = link.node_end.rect.x() - x_spacing*self.__bezier_offset
            end_y1 = link.node_end.rect.y()+link_end_offset
            end_y2 = link.node_end.rect.y()+link_end_offset+link.amount * y_scale

            # make the path from the positions
            path = QtGui.QPainterPath()
            path.moveTo(start_x, start_y1)
            path.cubicTo(start_x_dir, start_y1, end_x_dir, end_y1, end_x, end_y1)
            path.lineTo(end_x, end_y2)
            path.cubicTo(end_x_dir, end_y2, start_x_dir, start_y2, start_x, start_y2)
            path.lineTo(start_x, start_y1)
            link.path = path

    def paintEvent(self, event):
        # create the painter
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setPen(QtGui.QColor("#000000"))
        painter.setRenderHints(painter.Antialiasing)

        # render all the links
        for link in self.links:
            gradient = QtGui.QLinearGradient(link.node_start.rect.right(), 0, link.node_end.rect.left(), 0)
            c1 = QtGui.QColor(link.node_start.color)
            # color = QtGui.QColor(link.node_start.color)
            # color.setAlphaF(0.5)
            # painter.fillPath(link.path, color)
            # use a gradient
            c1.setAlphaF(0.5)
            gradient.setColorAt(0.6, c1)
            c2 = QtGui.QColor(link.node_end.color)
            c2.setAlphaF(0.5)
            gradient.setColorAt(0.8, c2)
            painter.fillPath(link.path, gradient)

        # render the nodes
        print(self.layers)
        for layer in self.layers:
            for node in layer.nodes:
                if not node.selected:
                    painter.fillRect(node.rect, QtGui.QColor(node.color))
                else:
                    painter.setBrush(QtGui.QColor(node.color))
                    painter.drawRect(node.rect)

        # draw selection of the links
        for link in self.links:
            if link.selected:
                painter.strokePath(link.path, QtGui.QColor("#000000"))
        painter.end()

    def resizeEvent(self, event):
        self.calculate_positions()

    def mouseMoveEvent(self, event):
        new_hovered_item = None
        # try to find hovered in the nodes
        for layer in self.layers:
            for node in layer.nodes:
                if node.rect.contains(event.pos()):
                    new_hovered_item = node
        if new_hovered_item is None:
            # try again to find, in the links
            for link in self.links:
                if link.path.contains(event.pos()):
                    new_hovered_item = link
        if self.hovered_item != new_hovered_item:
            # update
            if self.hovered_item is not None:
                self.hovered_item.selected = False
            self.hovered_item = new_hovered_item
            if self.hovered_item is not None:
                self.hovered_item.selected = True
            self.hovered_changed.emit([self.hovered_item])
            self.update()

    def sizeHint(self):
        return QtCore.QSize(500, 400)
