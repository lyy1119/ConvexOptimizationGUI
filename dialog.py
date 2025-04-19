from lyy19Lib.convexOptimization import MethodType , OnedimensionOptimization , MultidimensionOptimization, ConstraintOptimization
from lyy19Lib.mathFunction import FractionFunction
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout , QLabel, QPushButton, QLineEdit, QMessageBox , QDialog , QRadioButton , QGridLayout , QTextEdit , QButtonGroup, QMainWindow, QMenuBar, QGroupBox, QSizePolicy
from PyQt6.QtGui import QAction
from enum import Enum
from PyQt6.QtCore import Qt, QThread, pyqtSignal

class ProblemType(Enum):
    oneDimension = 0
    multiDimension = 1
    constrainted = 2
    mutiTarget = 4

class ProblemSwitch(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.create_layout()
        self.result = ProblemType.oneDimension

    def create_layout(self):
        self.setWindowTitle('选择优化模型类型')
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        # 创建布局
        layout = QVBoxLayout(self)
        # 一个单选框加按钮
        group_box = QGroupBox("优化模型类型")
        group_layout = QVBoxLayout()
        # 创建单选框
        radio1 = QRadioButton("一维无约束凸优化（指定方向的优化）")
        radio2 = QRadioButton("多维无约束凸优化")
        radio3 = QRadioButton("多维约束优化")
        radio4 = QRadioButton("多目标多维约束优化")
        # 默认选项
        self.radios = {
            radio1:ProblemType.oneDimension,
            radio2:ProblemType.multiDimension,
            radio3:ProblemType.constrainted, 
            radio4:ProblemType.mutiTarget
            }
        radio1.setChecked(True)
        group_layout.addWidget(radio1)
        group_layout.addWidget(radio2)
        group_layout.addWidget(radio3)
        group_layout.addWidget(radio4)

        group_box.setLayout(group_layout)
        layout.addWidget(group_box)
        # 确认与取消按钮
        buttonLayout = QHBoxLayout()
        layout.addLayout(buttonLayout)
        ok = QPushButton("确认")
        cancel = QPushButton("取消")
        buttonLayout.addWidget(ok)
        buttonLayout.addWidget(cancel)
        ok.clicked.connect(self.accept)
        cancel.clicked.connect(self.reject)

    def accept(self):
        for key, value in self.radios.items():
            if key.isChecked():
                self.result = value
        return super().accept()
