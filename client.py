from opcua import Client
import sys
from PyQt5.QtWidgets import (QWidget, QLabel,
    QLineEdit, QApplication, QPushButton, QDesktopWidget, QGridLayout, QSizePolicy)

url = "opc.tcp://192.168.0.8:4840"


class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.client = None
        self.initUI()

    # Пользовательский интерфейс
    def initUI(self):

        # Подписи над новыми и старыми значениями, хранящимися на сервере
        self.newValues = QLabel('New values from client')
        self.monitoredValues = QLabel('Monitor values')

        # Строки ввода для новых значений
        self.newValuesEdit1 = QLineEdit()
        self.newValuesEdit2 = QLineEdit()
        self.newValuesEdit3 = QLineEdit()

        # Строки для отображения текущих значений на сервере
        self.monitoredValuesEdit1 = QLineEdit()
        self.monitoredValuesEdit2 = QLineEdit()
        self.monitoredValuesEdit3 = QLineEdit()
        self.monitoredValuesEdit1.setReadOnly(True)
        self.monitoredValuesEdit2.setReadOnly(True)
        self.monitoredValuesEdit3.setReadOnly(True)

        # Строка для ввода адреса сервера
        self.serverAddressEdit = QLineEdit()

        # Кнопка для отправки новых значений
        self.sendDataButton = QPushButton("send data", self)
        self.sendDataButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.sendDataButton.clicked.connect(lambda: self.sendDataClicked())

        # Кнопка для подключения к серверу
        self.connectButton = QPushButton("connect", self)
        self.connectButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.connectButton.clicked.connect(lambda: self.connectClicked())

        # Сеточный макет для UI
        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        self.grid.addWidget(self.serverAddressEdit, 1, 0)
        self.grid.addWidget(self.connectButton, 1, 1)

        self.grid.addWidget(self.newValues, 2, 0)
        self.grid.addWidget(self.newValuesEdit1, 3, 0)
        self.grid.addWidget(self.newValuesEdit2, 4, 0)
        self.grid.addWidget(self.newValuesEdit3, 5, 0)
        self.grid.addWidget(self.sendDataButton, 6, 0)

        self.grid.addWidget(self.monitoredValues, 2, 1)
        self.grid.addWidget(self.monitoredValuesEdit1, 3, 1)
        self.grid.addWidget(self.monitoredValuesEdit2, 4, 1)
        self.grid.addWidget(self.monitoredValuesEdit3, 5, 1)

        self.setLayout(self.grid)
        self.resize(800, 500)
        self.center()
        self.setWindowTitle('Client')
        self.show()

    # Выравнивание окна по центру экрана
    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # При нажатии на кнопку "connect" происходит подключение к серверу
    def connectClicked(self):
        self.client = Client(self.serverAddressEdit.text())
        self.client.connect()
        self.setValues()

    # Значения, принимаемые с сервера
    def setValues(self):
        node1 = self.client.get_node("ns=2;i=2")
        tag1 = node1.get_value()
        node2 = self.client.get_node("ns=2;i=3")
        tag2 = node2.get_value()
        node3 = self.client.get_node("ns=2;i=4")
        tag3 = node3.get_value()
        self.monitoredValuesEdit1.setText(str(tag1))
        self.monitoredValuesEdit2.setText(str(tag2))
        self.monitoredValuesEdit3.setText(str(tag3))

    # Отправка новых значений на сервер
    def sendDataClicked(self):
        node1 = self.client.get_node("ns=2;i=2")
        node1.set_value(int(self.newValuesEdit1.text()))
        node2 = self.client.get_node("ns=2;i=3")
        node2.set_value(int(self.newValuesEdit2.text()))
        node3 = self.client.get_node("ns=2;i=4")
        node3.set_value(int(self.newValuesEdit3.text()))
        self.setValues()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    wind = Window()

    sys.exit(app.exec_())
