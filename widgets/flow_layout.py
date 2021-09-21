import PyQt5.QtWidgets as Qtw
import PyQt5.QtCore as QtCore
from PyQt5.QtCore import Qt


class FlowLayout(Qtw.QLayout):
    """
    A flow layout, taken from the Qt examples
    """
    def __init__(self, parent, margin=-1, v_spacing=1, h_spacing=-1):
        super(FlowLayout, self).__init__(parent)
        self.h_spacing = h_spacing
        self.v_spacing = v_spacing
        self.item_list = list()

        self.setContentsMargins(margin, margin, margin, margin)

    def addItem(self, item):
        self.item_list.append(item)

    def horizontalSpacing(self):
        if self.h_spacing >= 0:
            return self.h_spacing
        return self.smartSpacing(Qtw.QStyle.PM_LayoutHorizontalSpacing)

    def verticalSpacing(self):
        if self.v_spacing >= 0:
            return self.v_spacing
        return self.smartSpacing(Qtw.QStyle.PM_LayoutVerticalSpacing)

    def expandingDirections(self):
        return Qt.Vertical

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        return self.doLayout(QtCore.QRect(0, 0, width, 0), True)

    def count(self):
        return len(self.item_list)

    def itemAt(self, index):
        if 0 <= index < len(self.item_list):
            return self.item_list[index]
        return None

    def minimumSize(self):
        size = QtCore.QSize()
        for item in self.item_list:
            size.expandedTo(item.minimumSize())
        left, top, right, bottom = self.getContentsMargins()
        size += QtCore.QSize(left+right, top+bottom)
        return size

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def takeAt(self, index):
        if 0 <= index < len(self.item_list):
            return self.item_list.pop(index)

    def doLayout(self, rect, testOnly):
        left, top, right, bottom = self.getContentsMargins()
        effectiveRect = rect.adjusted(left, top, -right, -bottom)
        x = effectiveRect.x()
        y = effectiveRect.y()
        lineHeight = 0

        for item in self.item_list:
            wid = item.widget()
            spaceX = self.horizontalSpacing()
            if spaceX == -1:
                spaceX = wid.style().layoutSpacing(Qtw.QSizePolicy.PushButton, Qtw.QSizePolicy.PushButton, Qt.Horizontal)
            spaceY = self.verticalSpacing()
            if spaceY == -1:
                spaceY = wid.style().layoutSpacing(Qtw.QSizePolicy.PushButton, Qtw.QSizePolicy.PushButton, Qt.Vertical)

            nextX = x + item.sizeHint().width() + spaceX
            if nextX - spaceX > effectiveRect.right() and lineHeight > 0:
                x = effectiveRect.x()
                y = y + lineHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                lineHeight = 0

            if not testOnly:
                item.setGeometry(QtCore.QRect(QtCore.QPoint(x, y), item.sizeHint()))

            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())
        return y + lineHeight - rect.y() + bottom

    def smartSpacing(self, pixelmetric):
        parent = self.parent()
        if parent is None:
            return -1
        elif parent.isWidgetType():
            return parent.style().pixelMetric(pixelmetric, None, parent)
        else:
            return parent.spacing()
