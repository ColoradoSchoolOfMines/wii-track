#! /usr/bin/env python3
import boto3
import json
import decimal
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from boto3.dynamodb.conditions import Key, Attr, Between


# Helper class to convert a DynamoDB item to JSON.
# class DecimalEncoder(json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o, decimal.Decimal):
#             return str(o)
#         return super(DecimalEncoder, self).default(o)




query_id = 0



class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'wii-track'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 700
        self.initUI()

        self.dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
        self.table = self.dynamodb.Table('InventoryTracking')

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.textbox = QLineEdit(self)
        self.textbox.move((self.width / 2) - 200, 25)
        self.textbox.resize(80, 30)
        # self.textbox.setAlignment(Qt.AlignCenter)

        self.label = QLabel(self)
        self.label.resize(140, 40)
        self.label.move(5, 20)
        self.label.setText("Enter ID To Lookup: ")

        self.label = QLabel(self)
        self.label.resize(640, 480)
        self.label.move(5, 400)

        self.start_button = QPushButton(self)
        self.start_button.resize(100, 30)
        self.start_button.move((self.width / 2) - 95, 25)
        self.start_button.setText("Lookup")
        self.start_button.clicked.connect(self.on_click)

        self.data_view = QTreeWidget(self)
        self.data_view.resize(400, 400)
        self.data_view.move((self.width / 2) - 200, 100)
        self.data_view.setColumnCount(2)
        self.data_view.setColumnWidth(0, 150)
        self.data_view.header().close()

        self.show()

    @pyqtSlot()
    def on_click(self):

        query_id = self.textbox.text()

        self.results = self.table.query(
            KeyConditionExpression=Key('id').eq(int(query_id)),
        )

        # print(self.results)
        self.root_tree = QTreeWidgetItem(['id', str(int(self.results['Items'][0]['id']))])
        self.data_view.addTopLevelItem(self.root_tree)
        self.root_tree.setExpanded(True)

        for k, v in self.results['Items'][0]['info'].items():
            print(k, v)
            if k == 'probabilities':
                self.child_element = QTreeWidgetItem(['probabilities'])
                for x, y in v.items():
                    self.child_element_a = QTreeWidgetItem([str(x), str(y)])
                    self.child_element.addChild(self.child_element_a)
                self.root_tree.addChild(self.child_element)
                self.child_element.setExpanded(True)
            # else if: k == 'color_data':
            else:
                self.child_element = QTreeWidgetItem([str(k), str(v)])
                self.root_tree.addChild(self.child_element) 

        # for element in self.results:
        #     self.root_tree = QtWidgets.QTreeWidgetItem([self.root['name'], str(self.root['channel_id']), 'channel'])
        #     self.root_tree = QtWidgets.QtreeWidgetItem([])


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
