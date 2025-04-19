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

class oneDimensionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.create_layout()
        self.result = None

    def create_layout(self):
        # 填写一维优化所需参数
        layout = QVBoxLayout(self)

        # 输入参数
        parameter = QGroupBox("输出参数")
        parameterLayout = QGridLayout(parameter)

        # 函数
        functionLable = QLabel("函数")
        parameterLayout.addWidget(functionLable , 0 , 0)
        self.function = QLineEdit(self)
        self.function.setPlaceholderText("字符串")
        parameterLayout.addWidget(self.function , 0 , 1)

        # x0
        x0Lable = QLabel("起始点X0")
        parameterLayout.addWidget(x0Lable , 1 , 0)
        self.x0 = QLineEdit(self)
        self.x0.setPlaceholderText("空格分隔  1.0 1.0")
        parameterLayout.addWidget(self.x0 , 1 , 1)

        # epslionx
        epXLable = QLabel("epsilon x")
        parameterLayout.addWidget(epXLable , 2 , 0)
        self.epsilonx = QLineEdit(self)
        self.epsilonx.setPlaceholderText("0.01")
        parameterLayout.addWidget(self.epsilonx , 2 , 1)

        # epsilonf
        epFLable = QLabel("epsilon f")
        parameterLayout.addWidget(epFLable , 3 , 0)
        self.epsilonf = QLineEdit(self)
        self.epsilonf.setPlaceholderText("0.01")
        parameterLayout.addWidget(self.epsilonf , 3 , 1)

        # 搜索方向
        sLable = QLabel("搜索方向S")
        parameterLayout.addWidget(sLable , 4 , 0)
        self.sInputTextbox = QLineEdit(self)
        self.sInputTextbox.setPlaceholderText("空格分隔 1.2 1.2")
        parameterLayout.addWidget(self.sInputTextbox , 4 , 1)

        # 最大步长
        maxStepLable = QLabel("最大迭代次数")
        parameterLayout.addWidget(maxStepLable , 5 , 0)
        self.maxStep = QLineEdit(self)
        self.maxStep.setPlaceholderText("默认1000")
        self.maxStep.setText("1000")
        parameterLayout.addWidget(self.maxStep , 5 , 1)

        layout.addWidget(parameter)

        # 方法选择
        method = QGroupBox("优化方法")
        methodLayout = QVBoxLayout(method)
        # 一维优化方法
        onedimensonMethodGroup = QButtonGroup(self)
        self.goldenSection = QRadioButton("黄金分割法")
        onedimensonMethodGroup.addButton(self.goldenSection)
        self.quadraticInterpolation = QRadioButton("二次插值法")
        onedimensonMethodGroup.addButton(self.quadraticInterpolation)
        self.oneDimensionButton = {
            self.goldenSection:MethodType.goldenSection,
            self.quadraticInterpolation:MethodType.quadraticInterpolation
            }
        for i in self.oneDimensionButton.keys():
            methodLayout.addWidget(i)
        self.goldenSection.setChecked(True)
        layout.addWidget(method)

        # 确定与取消
        buttonLayout = QHBoxLayout()
        ok = QPushButton("确认")
        ok.clicked.connect(self.accept)
        cancel = QPushButton("取消")
        cancel.clicked.connect(self.reject)
        buttonLayout.addWidget(ok)
        buttonLayout.addWidget(cancel)
        layout.addLayout(buttonLayout)

    def accept(self):
        self.result = {}
        # 验证函数
        try:
            f = FractionFunction(self.function.text())
        except:
            QMessageBox.warning(self, "输入错误", "输入的函数无法解析，请检查函数")
            return
        self.result["function"] = f
        # 验证初始点
        dimension = f.dimension
        if len(self.x0.text().split()) != dimension:
            QMessageBox.warning(self,  "输入错误", "输入的初始点和函数维度不符")
            return
        self.result["x0"] = list(self.x0.text().split())
        # 验证epsilonx
        try:
            epsilonx = float(self.epsilonx.text())
            if epsilonx < 0:
                raise ValueError()
        except:
            QMessageBox.warning(self,  "输入错误", "输入的epsilonx不是正实数")
            return
        self.result["epsilonx"] = epsilonx
        # 验证epsilonf
        try:
            epsilonx = float(self.epsilonx.text())
            if epsilonx < 0:
                raise ValueError()
        except:
            QMessageBox.warning(self,  "输入错误", "输入的epsilonx不是正实数")
            return
        self.result["epsilonx"] = epsilonx
        # 验证S
        dimension = f.dimension
        if len(self.sInputTextbox.text().split()) != dimension:
            QMessageBox.warning(self,  "输入错误", "输入的搜索方向S和函数维度不符")
            return
        self.result["s"] = list(self.sInputTextbox.text().split())
        # 优化方法
        for i, j in self.oneDimensionButton.items():
            if i.isChecked():
                self.result["method"] = j
        return super().accept()



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
