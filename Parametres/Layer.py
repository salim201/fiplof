from PyQt4 import QtGui, Qt
from .UiLayer import Ui_Dialog
from Utils import Utils
import psycopg2
import psycopg2.extras

class MyLabel(QtGui.QLabel):
    def __init__(self, parent=None):
        QtGui.QLabel.__init__(self, parent)
        self.color = Qt.QColor(0, 0, 0)
        self.outlineColor = Qt.QColor(0, 0, 0)
        self.outlineWidth = 0

    def paintEvent(self, e):
        qp = QtGui.QPainter(self)
        qp.setRenderHint(Qt.QPainter.Antialiasing);
        qp.setFont(self.font())
        qp.setPen(Qt.QPen(self.color))
        qp.drawText(0, self.height() / 2, self.text())

        if self.outlineWidth > 0:
            pen = Qt.QPen(self.outlineColor)
            pen.setWidth(self.outlineWidth)
            qp.setPen(pen)
            path = QtGui.QPainterPath()
            path.addText(0, self.height() / 2, self.font(), self.text())
            qp.drawPath(path)


    def setColor(self, color):
        self.color = color
        self.repaint()

    def setOutlineColor(self, color):
        self.outlineColor = color
        self.repaint()

    def setOutlineWidth(self, width):
        self.outlineWidth = width
        self.repaint()


class Layer(QtGui.QDialog):
    def __init__(self, connection, layer_index):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.preview = MyLabel()
        self.preview.setText("Hello")
        self.ui.verticalLayout_2.addWidget(self.preview)
        self.layer_index, self.connection = layer_index, connection
        self.init_actions()
        self.init_fields()

    def init_fields(self):
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute("SELECT * FROM param_layer WHERE layer_index = %s", (self.layer_index, ))
            res = cursor.fetchone()
            if not res:
                return
            f = Qt.QFont()
            f.setFamily(res["label_font"])
            c1 = Qt.QColor(res["label_color"])
            c2 = Qt.QColor(res["stroke_color"])
            self.ui.checkBoxLabel.setChecked(res["label_size"] > 0)
            self.ui.fontComboBox.setCurrentFont(f)
            self.ui.spinBoxLabelSize.setValue(res["label_size"])
            self.ui.checkBoxMapUnit.setChecked(res["font_size_map_units"])
            self.ui.pushButtonLabelColor.setIcon(Utils.create_icon(c1))
            self.preview.setColor(c1)

            self.ui.checkBoxBuffer.setChecked(res["stroke_size"] > 0)
            self.ui.spinBoxBufferSize.setValue(res["stroke_size"])
            self.ui.pushButtonBufferColor.setIcon(Utils.create_icon(c2))
            self.preview.setOutlineColor(c2)
        except Exception as e:
            print(e)
        cursor.close()

    def init_actions(self):
        self.ui.checkBoxLabel.stateChanged.connect(self.checkBoxLabelStateChanged)
        self.ui.checkBoxBuffer.stateChanged.connect(self.checkBoxBufferStateChanged)
        self.ui.checkBoxDarkBg.stateChanged.connect(self.checkBoxDarkBgStateChanged)
        self.ui.pushButtonLabelColor.clicked.connect(self.choose_color)
        self.ui.pushButtonBufferColor.clicked.connect(self.choose_color_outline)

        self.ui.fontComboBox.currentFontChanged.connect(self.updateFont)
        self.ui.spinBoxLabelSize.valueChanged.connect(self.updateFont)
        self.ui.spinBoxBufferSize.valueChanged.connect(self.updateBuffer)

        self.ui.pushButtonCancel.clicked.connect(self.reject)
        self.ui.pushButtonOK.clicked.connect(self.okay)

    def checkBoxLabelStateChanged(self):
        self.preview.setVisible(self.ui.checkBoxLabel.isChecked())
        self.ui.fontComboBox.setEnabled(self.ui.checkBoxLabel.isChecked())
        self.ui.spinBoxLabelSize.setEnabled(self.ui.checkBoxLabel.isChecked())
        self.ui.checkBoxMapUnit.setEnabled(self.ui.checkBoxLabel.isChecked())
        self.ui.pushButtonLabelColor.setEnabled(self.ui.checkBoxLabel.isChecked())
        self.ui.spinBoxLabelSize.setValue(12 if self.ui.checkBoxLabel.isChecked() else 0)

    def checkBoxBufferStateChanged(self):
        self.ui.spinBoxBufferSize.setEnabled(self.ui.checkBoxBuffer.isChecked())
        self.ui.pushButtonBufferColor.setEnabled(self.ui.checkBoxBuffer.isChecked())
        self.ui.spinBoxBufferSize.setValue(1 if self.ui.checkBoxBuffer.isChecked() else 0)

    def checkBoxDarkBgStateChanged(self):
        if self.ui.checkBoxDarkBg.isChecked():
            self.ui.frame.setStyleSheet("background: rgb(50, 50, 50)")
        else:
            self.ui.frame.setStyleSheet("background: white")

    def updateFont(self):
        font = self.ui.fontComboBox.currentFont()
        font.setPointSize(self.ui.spinBoxLabelSize.value())
        self.preview.setFont(font)

    def updateBuffer(self):
        self.preview.setOutlineWidth(self.ui.spinBoxBufferSize.value())

    def choose_color(self):
        dialog = QtGui.QColorDialog()
        if dialog.exec_():
            self.preview.setColor(dialog.selectedColor())
            self.ui.pushButtonLabelColor.setIcon(Utils.create_icon(self.preview.color))

    def choose_color_outline(self):
        dialog = QtGui.QColorDialog()
        if dialog.exec_():
            self.preview.setOutlineColor(dialog.selectedColor())
            self.ui.pushButtonBufferColor.setIcon(Utils.create_icon(self.preview.outlineColor))

    def find_by_index(self):
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute("SELECT id FROM param_layer WHERE layer_index = %s", (self.layer_index, ))
            res = cursor.fetchone()
            return res["id"]
        except Exception as e:
            print(e)
        cursor.close()
        self.accept()

    def okay(self):
        param_id = self.find_by_index()
        cursor = self.connection.cursor()
        if param_id:
            sql = "UPDATE param_layer SET label_font = %s, label_size = %s, font_size_map_units = %s, label_color = %s"\
            ", stroke_size = %s, stroke_color = %s WHERE layer_index = %s"
        else:
            sql = "INSERT INTO param_layer(label_font, label_size, font_size_map_units, label_color, stroke_size, stroke_color, layer_index) " \
            " VALUES (%s, %s, %s, %s, %s, %s, %s)"
        try:
            print(self.preview.outlineColor.toRgb())
            cursor.execute(sql, (str(self.ui.fontComboBox.currentFont().family())
                , self.ui.spinBoxLabelSize.value()
                , self.ui.checkBoxMapUnit.isChecked()
                , str(self.preview.color.name())
                , self.ui.spinBoxBufferSize.value()
                , str(self.preview.outlineColor.name())
                , self.layer_index))
            self.connection.commit()
        except Exception as e:
            print(e)
            self.connection.rollback()
        cursor.close()
        self.accept()