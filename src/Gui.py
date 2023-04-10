from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
import AStar, Input, UCS
import os
import folium

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.map_widget = self.ui.map_widget

        # create a Folium map centered on a specific location
        location = [-6.891166851249083, 107.61068223565846]  # New York City
        m = folium.Map(location=location, zoom_start=20)

        folium.ClickForMarker().add_to(m)

        # convert the map to HTML
        map_html = m._repr_html_()

        # create a QWebEngineView to display the map
        self.webview = QWebEngineView()
        self.webview.setHtml(map_html)
        self.map_widget.setLayout(QVBoxLayout())
        self.map_widget.layout().addWidget(self.webview)
        self.ui.pushButton.clicked.connect(self.openFileNameDialog)
        self.ui.search_botton.clicked.connect(self.searchPath)

    def openFileNameDialog(self):
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Choose map file", os.getcwd(), 
                                                            "Text Files (*.txt)", options=options)
        if fileName:
            name = fileName.split("/")[-1]
            print(fileName)
            self.ui.lineEdit.setText(name)
            self.ui.graph = Input.Graph()
            self.ui.input_check = True
            try:
                if self.ui.type_map.currentText() == "with coords":
                    self.ui.graph.read_input_coords(fileName)
                else:
                    self.ui.graph.read_input(fileName)
            except Exception as e:
                self.ui.warning("Invalid map type")
                self.ui.lineEdit.setText("")
                self.ui.input_check = False
                return
            self.update_map()
            self.ui.add_nodes()
    
    def update_map(self):
        nodes = self.ui.graph.get_nodes()
        adj_matrix = self.ui.graph.get_adj()
        coord = self.ui.graph.get_coords()
        coord_tuples = []
        for i in range(len(adj_matrix)):
            to_float = (float(coord[i][0]), float(coord[i][1]))
            coord_tuples.append(to_float)
        # initialize the sums
        sum_lat = 0
        sum_lon = 0

        # iterate over the coordinates and sum up the values
        for lat, lon in coord_tuples:
            sum_lat += lat
            sum_lon += lon

        # calculate the averages
        avg_lat = sum_lat / len(coord_tuples)
        avg_lon = sum_lon / len(coord_tuples)

        self.m = folium.Map(location=[avg_lat, avg_lon], zoom_start=15)

        for i in range(len(nodes)):
            tooltip = folium.Tooltip(nodes[i])
            temp_marker = folium.Marker(location=[coord_tuples[i][0], coord_tuples[i][1]], tooltip=tooltip)
            temp_marker.add_to(self.m);

        for i in range(len(adj_matrix)):
            for j in range(i):
                if adj_matrix[i][j] != 0:
                    line = folium.PolyLine(locations=[[coord_tuples[i][0], coord_tuples[i][1]], [coord_tuples[j][0], coord_tuples[j][1]]], color='red')
                    line.add_to(self.m)

        # convert the updated map to HTML
        self.map_html = self.m._repr_html_()
        # update the QWebEngineView to display the updated map
        self.webview.setHtml(self.map_html)

    def searchPath(self):
        if not self.ui.input_check:
            self.ui.warning("Please choose a file")
            return
        self.ui.clear_result()
        source = self.ui.soure_nodes.findText(self.ui.soure_nodes.currentText())
        dest = self.ui.dest_nodes.findText(self.ui.dest_nodes.currentText())
        algo = self.ui.search_alg.currentText()
        self.ui.graph.calculate_weighted()
        weighted = self.ui.graph.get_weighted()
        coords = self.ui.graph.get_coords()
        nodes = self.ui.graph.get_nodes()
        print(weighted)
        if algo == "UCS":
            self.ui.result = UCS.ucs(weighted, source, dest)
        else:
            self.ui.result = AStar.a_star(weighted, coords, source, dest)
        path = ""
        for i in range(len(self.ui.result[0])):
            idx = self.ui.result[0][i]
            path += str(self.ui.graph.get_nodes()[idx])
            if i != len(self.ui.result[0]) - 1:
                path += " -> "
        distance = str(round(self.ui.result[1], 4))
        for i in range(len(self.ui.result[0]) - 1):
            from_coor = self.ui.result[0][i]
            to_coor = self.ui.result[0][i + 1]
            line = folium.PolyLine(locations=[[float(coords[from_coor][0]), float(coords[from_coor][1])], [float(coords[to_coor][0]), float(coords[to_coor][1])]], color='cyan')
            line.add_to(self.m)
        # convert the updated map to HTML
        self.map_html = self.m._repr_html_()
        # update the QWebEngineView to display the updated map
        self.webview.setHtml(self.map_html)
        self.ui.path_result.setText(path)
        self.ui.dist_result.setText(distance)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(932, 590)
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        MainWindow.setAnimated(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.map_widget = QWidget(self.centralwidget)
        self.map_widget.setGeometry(350, 50, 481, 341)
        self.map_widget.setObjectName("map_widget")
        self.search_botton = QtWidgets.QPushButton(self.centralwidget)
        self.search_botton.setGeometry(QtCore.QRect(110, 370, 81, 31))
        self.search_botton.setObjectName("search_botton")
        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(340, 0, 211, 51))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.title.setFont(font)
        self.title.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.title.setFrameShadow(QtWidgets.QFrame.Plain)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setObjectName("title")
        self.algo_frame = QtWidgets.QFrame(self.centralwidget)
        self.algo_frame.setGeometry(QtCore.QRect(80, 270, 151, 80))
        self.algo_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.algo_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.algo_frame.setObjectName("algo_frame")
        self.algo_title = QtWidgets.QLabel(self.algo_frame)
        self.algo_title.setGeometry(QtCore.QRect(30, 0, 91, 41))
        self.algo_title.setObjectName("algo_title")
        self.search_alg = QtWidgets.QComboBox(self.algo_frame)
        self.search_alg.setGeometry(QtCore.QRect(40, 40, 71, 31))
        self.search_alg.setObjectName("search_alg")
        self.search_alg.addItem("")
        self.search_alg.addItem("")
        self.path_frame = QtWidgets.QFrame(self.centralwidget)
        self.path_frame.setGeometry(QtCore.QRect(320, 410, 591, 121))
        self.path_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.path_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.path_frame.setObjectName("path_frame")
        self.path_title = QtWidgets.QLabel(self.path_frame)
        self.path_title.setGeometry(QtCore.QRect(10, 10, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.path_title.setFont(font)
        self.path_title.setObjectName("path_title")
        self.path_result = QtWidgets.QLabel(self.path_frame)
        self.path_result.setGeometry(QtCore.QRect(10, 40, 561, 81))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.path_result.setFont(font)
        self.path_result.setText("")
        self.path_result.setObjectName("path_result")
        self.dist_frame = QtWidgets.QFrame(self.centralwidget)
        self.dist_frame.setGeometry(QtCore.QRect(10, 410, 221, 121))
        self.dist_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.dist_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.dist_frame.setObjectName("dist_frame")
        self.distance_title = QtWidgets.QLabel(self.dist_frame)
        self.distance_title.setGeometry(QtCore.QRect(10, 10, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.distance_title.setFont(font)
        self.distance_title.setObjectName("distance_title")
        self.dist_result = QtWidgets.QLabel(self.dist_frame)
        self.dist_result.setGeometry(QtCore.QRect(10, 40, 151, 71))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.dist_result.setFont(font)
        self.dist_result.setText("")
        self.dist_result.setObjectName("dist_result")
        self.file_frame = QtWidgets.QFrame(self.centralwidget)
        self.file_frame.setGeometry(QtCore.QRect(40, 90, 231, 91))
        self.file_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.file_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.file_frame.setObjectName("file_frame")
        self.file_title = QtWidgets.QLabel(self.file_frame)
        self.file_title.setGeometry(QtCore.QRect(60, 0, 101, 31))
        self.file_title.setAlignment(QtCore.Qt.AlignCenter)
        self.file_title.setObjectName("file_title")
        self.pushButton = QtWidgets.QPushButton(self.file_frame)
        self.pushButton.setGeometry(QtCore.QRect(140, 50, 91, 21))
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(self.file_frame)
        self.lineEdit.setGeometry(QtCore.QRect(0, 50, 113, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.nodes_frame = QtWidgets.QFrame(self.centralwidget)
        self.nodes_frame.setGeometry(QtCore.QRect(50, 190, 221, 80))
        self.nodes_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.nodes_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.nodes_frame.setObjectName("nodes_frame")
        self.soure_nodes = QtWidgets.QComboBox(self.nodes_frame)
        self.soure_nodes.setGeometry(QtCore.QRect(10, 40, 71, 31))
        self.soure_nodes.setObjectName("soure_nodes")
        self.nodes_title = QtWidgets.QLabel(self.nodes_frame)
        self.nodes_title.setGeometry(QtCore.QRect(70, 0, 81, 31))
        self.nodes_title.setObjectName("nodes_title")
        self.dest_nodes = QtWidgets.QComboBox(self.nodes_frame)
        self.dest_nodes.setGeometry(QtCore.QRect(140, 40, 71, 31))
        self.dest_nodes.setObjectName("dest_nodes")
        self.type_map = QtWidgets.QComboBox(self.centralwidget)
        self.type_map.setGeometry(QtCore.QRect(90, 50, 131, 22))
        self.type_map.setObjectName("type_map")
        self.type_map.addItem("with coords")
        self.type_map.addItem("without coords")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 932, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.lineEdit.setReadOnly(True)
        # self.pushButton.clicked.connect(self.openFileNameDialog)

        # self.search_botton.clicked.connect(self.searchPath)

        self.input_check = False

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.search_botton.setText(_translate("MainWindow", "Search"))
        self.title.setText(_translate("MainWindow", "Path Finder"))
        self.algo_title.setText(_translate("MainWindow", "Choose Algorithm"))
        self.search_alg.setItemText(0, _translate("MainWindow", "UCS"))
        self.search_alg.setItemText(1, _translate("MainWindow", "A*"))
        self.path_title.setText(_translate("MainWindow", "Path"))
        self.distance_title.setText(_translate("MainWindow", "Distance"))
        self.file_title.setText(_translate("MainWindow", "Choose File"))
        self.pushButton.setText(_translate("MainWindow", "Open File"))
        self.nodes_title.setText(_translate("MainWindow", "Choose Nodes"))

    def add_nodes(self):
        self.clear_nodes()
        nodes = self.graph.get_nodes()
        for i in range(len(nodes)):
            self.soure_nodes.addItem(nodes[i])
            self.dest_nodes.addItem(nodes[i])
        self.soure_nodes.setCurrentIndex(0)
        self.dest_nodes.setCurrentIndex(1)

    def clear_nodes(self):
        self.soure_nodes.clear()
        self.dest_nodes.clear()

    def clear_result(self):
        self.path_result.setText("")
        self.dist_result.setText("")
    
    def warning(self, message):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setText(message)
        msg.setWindowTitle("Warning")
        msg.exec_()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MyMainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MyMainWindow)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
