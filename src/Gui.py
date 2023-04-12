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
        self.location = [-6.891166851249083, 107.61068223565846] 
        self.m = folium.Map(location=self.location, zoom_start=20)
        map_html = self.m._repr_html_()
        self.webview = QWebEngineView()
        self.webview.setHtml(map_html)
        self.map_widget.setLayout(QVBoxLayout())
        self.map_widget.layout().addWidget(self.webview)

        self.ui.pushButton.clicked.connect(self.openFileNameDialog)
        self.ui.search_botton.clicked.connect(self.searchPath)
        self.ui.clear_map_button.clicked.connect(self.reset_map)
        self.ui.input_mode.stateChanged.connect(lambda: self.input_change())
        self.ui.show_graph.clicked.connect(lambda: self.folium_graph())
        

    def openFileNameDialog(self):
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Choose map file", os.getcwd(), 
                                                            "Text Files (*.txt)", options=options)
        if fileName:
            self.ui.clear_input()
            name = fileName.split("/")[-1]
            self.ui.graph = Input.Graph()
            try:
                self.ui.graph.read_input_coords(fileName)
            except Exception as e:
                self.ui.input_check = False
                self.ui.warning("Invalid input file")
                return
            if len(self.ui.graph.get_nodes()) < 8:
                self.ui.input_check = False
                self.ui.warning("Nodes must be more than 8")
                return
            self.ui.input_check = True
            self.ui.file_name.setText(name)
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
        self.m.fit_bounds(coord_tuples)

        for i in range(len(nodes)):
            tooltip = folium.Tooltip(nodes[i])
            temp_marker = folium.Marker(location=[coord_tuples[i][0], coord_tuples[i][1]], tooltip=tooltip)
            temp_marker.add_to(self.m)

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
            self.ui.warning("No input detected")
            return
        self.ui.clear_result()
        self.update_map()
        source = self.ui.soure_nodes.findText(self.ui.soure_nodes.currentText())
        dest = self.ui.dest_nodes.findText(self.ui.dest_nodes.currentText())
        algo = self.ui.search_alg.currentText()
        self.ui.graph.calculate_weighted()
        weighted = self.ui.graph.get_weighted()
        coords = self.ui.graph.get_coords()
        if algo == "UCS":
            self.ui.result = UCS.ucs(weighted, source, dest)
        else:
            self.ui.result = AStar.a_star(weighted, coords, source, dest)
        if self.ui.result == None:
            self.ui.path_result.setText("No path found")
            self.ui.dist_result.setText("No path found")
            return
        path = ""
        for i in range(len(self.ui.result[0])):
            idx = self.ui.result[0][i]
            path += str(self.ui.graph.get_nodes()[idx])
            if i != len(self.ui.result[0]) - 1:
                path += " -> "
        distance = str(round(self.ui.result[1], 4)) + " km"
        for i in range(len(self.ui.result[0]) - 1):
            from_coor = self.ui.result[0][i]
            to_coor = self.ui.result[0][i + 1]
            line = folium.PolyLine(locations=[[float(coords[from_coor][0]), float(coords[from_coor][1])], [float(coords[to_coor][0]), float(coords[to_coor][1])]], color='cyan')
            line.add_to(self.m)
        # convert the updated map to HTML
        self.m
        self.map_html = self.m._repr_html_()
        # update the QWebEngineView to display the updated map
        self.webview.setHtml(self.map_html)
        self.ui.path_result.setText(path)
        self.ui.dist_result.setText(distance)
    
    def reset_map(self):
        # reset folium map
        self.m = folium.Map(location=self.location, zoom_start=20)
        self.input_change()
        map_html = self.m._repr_html_()
        self.webview.setHtml(map_html)

    def input_change(self):
        location = self.m
        self.m = folium.Map(location=self.location, zoom_start=20)
        if self.ui.input_mode.isChecked():
            folium.ClickForMarker().add_to(self.m)
            self.ui.pushButton.setDisabled(True)
        else:
            self.ui.pushButton.setDisabled(False)
    
    def folium_graph(self):
        # create graph from markers in folium map
        self.ui.graph = Input.Graph()
        coords = []
        
        # self.ui.input_check = True
        

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(932, 611)
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        MainWindow.setAnimated(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayout = QtWidgets.QFormLayout(self.centralwidget)
        self.formLayout.setObjectName("formLayout")
        self.frame_input = QtWidgets.QFrame(self.centralwidget)
        self.frame_input.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_input.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_input.setObjectName("frame_input")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_input)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.type_fram = QtWidgets.QFrame(self.frame_input)
        self.type_fram.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.type_fram.setFrameShadow(QtWidgets.QFrame.Raised)
        self.type_fram.setObjectName("type_fram")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.type_fram)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.input_mode = QtWidgets.QCheckBox(self.type_fram)
        self.input_mode.setObjectName("input_mode")
        self.verticalLayout_2.addWidget(self.input_mode)
        self.verticalLayout_5.addWidget(self.type_fram)
        self.file_frame = QtWidgets.QFrame(self.frame_input)
        self.file_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.file_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.file_frame.setObjectName("file_frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.file_frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.file_title = QtWidgets.QLabel(self.file_frame)
        self.file_title.setAlignment(QtCore.Qt.AlignCenter)
        self.file_title.setObjectName("file_title")
        self.verticalLayout.addWidget(self.file_title)
        self.file_name = QtWidgets.QLineEdit(self.file_frame)
        self.file_name.setObjectName("file_name")
        self.verticalLayout.addWidget(self.file_name)
        self.pushButton = QtWidgets.QPushButton(self.file_frame)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.verticalLayout_5.addWidget(self.file_frame)
        self.nodes_frame = QtWidgets.QFrame(self.frame_input)
        self.nodes_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.nodes_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.nodes_frame.setObjectName("nodes_frame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.nodes_frame)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.nodes_title = QtWidgets.QLabel(self.nodes_frame)
        self.nodes_title.setObjectName("nodes_title")
        self.verticalLayout_3.addWidget(self.nodes_title)
        self.nodes_title_s = QtWidgets.QLabel(self.nodes_frame)
        self.nodes_title_s.setObjectName("nodes_title_s")
        self.verticalLayout_3.addWidget(self.nodes_title_s)
        self.soure_nodes = QtWidgets.QComboBox(self.nodes_frame)
        self.soure_nodes.setObjectName("soure_nodes")
        self.verticalLayout_3.addWidget(self.soure_nodes)
        self.nodes_title_d = QtWidgets.QLabel(self.nodes_frame)
        self.nodes_title_d.setObjectName("nodes_title_d")
        self.verticalLayout_3.addWidget(self.nodes_title_d)
        self.dest_nodes = QtWidgets.QComboBox(self.nodes_frame)
        self.dest_nodes.setObjectName("dest_nodes")
        self.verticalLayout_3.addWidget(self.dest_nodes)
        self.verticalLayout_5.addWidget(self.nodes_frame)
        self.algo_frame = QtWidgets.QFrame(self.frame_input)
        self.algo_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.algo_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.algo_frame.setObjectName("algo_frame")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.algo_frame)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.algo_title = QtWidgets.QLabel(self.algo_frame)
        self.algo_title.setObjectName("algo_title")
        self.verticalLayout_4.addWidget(self.algo_title)
        self.search_alg = QtWidgets.QComboBox(self.algo_frame)
        self.search_alg.setObjectName("search_alg")
        self.search_alg.addItem("")
        self.search_alg.addItem("")
        self.verticalLayout_4.addWidget(self.search_alg)
        self.verticalLayout_5.addWidget(self.algo_frame)
        self.search_botton = QtWidgets.QPushButton(self.frame_input)
        self.search_botton.setObjectName("search_botton")
        self.verticalLayout_5.addWidget(self.search_botton)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.frame_input)
        self.frame_map = QtWidgets.QFrame(self.centralwidget)
        self.frame_map.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_map.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_map.setObjectName("frame_map")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_map)
        self.gridLayout.setObjectName("gridLayout")
        self.show_graph = QtWidgets.QPushButton(self.frame_map)
        self.show_graph.setObjectName("show_graph")
        self.gridLayout.addWidget(self.show_graph, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)
        self.clear_map_button = QtWidgets.QPushButton(self.frame_map)
        self.clear_map_button.setObjectName("clear_map_button")
        self.gridLayout.addWidget(self.clear_map_button, 1, 2, 1, 1)
        self.map_widget = QtWidgets.QGraphicsView(self.frame_map)
        self.map_widget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.map_widget.setObjectName("map_widget")
        self.gridLayout.addWidget(self.map_widget, 0, 0, 1, 3)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.frame_map)
        self.frame_result = QtWidgets.QFrame(self.centralwidget)
        self.frame_result.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_result.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_result.setObjectName("frame_result")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_result)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.dist_frame = QtWidgets.QFrame(self.frame_result)
        self.dist_frame.setMaximumSize(QtCore.QSize(175, 2000))
        self.dist_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.dist_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.dist_frame.setObjectName("dist_frame")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.dist_frame)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.distance_title = QtWidgets.QLabel(self.dist_frame)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.distance_title.setFont(font)
        self.distance_title.setObjectName("distance_title")
        self.verticalLayout_6.addWidget(self.distance_title)
        self.dist_result = QtWidgets.QLabel(self.dist_frame)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.dist_result.setFont(font)
        self.dist_result.setText("")
        self.dist_result.setObjectName("dist_result")
        self.verticalLayout_6.addWidget(self.dist_result)
        self.horizontalLayout.addWidget(self.dist_frame)
        self.path_frame = QtWidgets.QFrame(self.frame_result)
        self.path_frame.setMinimumSize(QtCore.QSize(100, 100))
        self.path_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.path_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.path_frame.setObjectName("path_frame")
        self.path_title = QtWidgets.QLabel(self.path_frame)
        self.path_title.setGeometry(QtCore.QRect(8, 8, 41, 27))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.path_title.setFont(font)
        self.path_title.setObjectName("path_title")
        self.scrollArea = QtWidgets.QScrollArea(self.path_frame)
        self.scrollArea.setGeometry(QtCore.QRect(8, 41, 789, 51))
        self.scrollArea.setMinimumSize(QtCore.QSize(200, 15))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.path_scroll = QtWidgets.QWidget()
        self.path_scroll.setGeometry(QtCore.QRect(0, 0, 785, 47))
        self.path_scroll.setObjectName("path_scroll")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.path_scroll)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.path_result = QtWidgets.QLabel(self.path_scroll)
        self.path_result.setMinimumSize(QtCore.QSize(100, 14))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.path_result.setFont(font)
        self.path_result.setText("")
        self.path_result.setObjectName("path_result")
        self.verticalLayout_8.addWidget(self.path_result)
        self.scrollArea.setWidget(self.path_scroll)
        self.horizontalLayout.addWidget(self.path_frame)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.frame_result)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.input_check = False
        self.path_result.setWordWrap(True)

        self.input_mode.hide()
        self.show_graph.hide()
        self.clear_map_button.hide()
        self.type_fram.hide()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.input_mode.setText(_translate("MainWindow", "Input From Map"))
        self.file_title.setText(_translate("MainWindow", "Choose File"))
        self.pushButton.setText(_translate("MainWindow", "Open File"))
        self.nodes_title.setText(_translate("MainWindow", "Choose Nodes"))
        self.nodes_title_s.setText(_translate("MainWindow", "Source"))
        self.nodes_title_d.setText(_translate("MainWindow", "Destination"))
        self.algo_title.setText(_translate("MainWindow", "Choose Algorithm"))
        self.search_alg.setItemText(0, _translate("MainWindow", "UCS"))
        self.search_alg.setItemText(1, _translate("MainWindow", "A*"))
        self.search_botton.setText(_translate("MainWindow", "Search"))
        self.show_graph.setText(_translate("MainWindow", "Display Graph"))
        self.clear_map_button.setText(_translate("MainWindow", "Clear Map"))
        self.distance_title.setText(_translate("MainWindow", "Distance"))
        self.path_title.setText(_translate("MainWindow", "Path"))

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
    
    def clear_input(self):
        self.input_check = False
        self.clear_nodes()
        self.clear_result()
        self.file_name.setText("")

    
    def warning(self, message):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setText(message)
        msg.setWindowTitle("Warning")
        msg.exec_()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
